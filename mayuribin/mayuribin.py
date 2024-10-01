import asyncio
import colorlog
import logging
import re

from aiohttp import web
from aiohttp_swagger3 import SwaggerDocs, SwaggerInfo, SwaggerUiSettings
from async_pymongo import AsyncClient
from datetime import datetime
from mayuribin import config
from mayuribin.route import routes_list, swagger_list
from mayuribin.routes import Routes

logging.getLogger().handlers.clear()
log = logging.getLogger("Mayuri-Bin")

class MayuriBin(web.Application, Routes):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.config = config
        self._conn = AsyncClient(self.config['mongodb']['URL'])
        self.db = self._conn["mayuribin"]["documents"]
        self._log = log
        self.swagger = SwaggerDocs(
            self,
            validate=False,
            swagger_ui_settings=SwaggerUiSettings(path="/docs/", layout="BaseLayout"),
            info=SwaggerInfo(
                title="Mayuri-bin API",
                version="1.0.0"
            )
        )

    async def run(self):
        self._setup_log()
        self.middlewares.append(self._access_log_middleware)
        self._log.info("Mayuri-Bin is starting up...")
        self.add_routes(routes_list)
        if self.config["app"]["ENABLE_API"]:
            self.swagger.add_routes(swagger_list)
        runner = web.AppRunner(self)
        await runner.setup()
        site = web.TCPSite(runner, host=self.config["app"]["HOST"], port=self.config["app"]["PORT"])
        await site.start()
        self._log.info("Mayuri-Bin is running on %s:%s", self.config["app"]["HOST"], self.config["app"]["PORT"])
        while True:
            try:
                await asyncio.sleep(3600)
            except asyncio.exceptions.CancelledError:
                await runner.cleanup()
                self._log.info("MayuriBin is shutting down...")
                break

    def _setup_log(self):
        """Configures logging"""
        level = logging.INFO
        logging.root.setLevel(level)

        file_format = "[ %(asctime)s: %(levelname)-8s ] %(name)-15s - %(message)s"
        logfile = logging.FileHandler("MayuriBin.log")
        formatter = logging.Formatter(file_format, datefmt="%H:%M:%S")
        logfile.setFormatter(formatter)
        logfile.setLevel(level)

        formatter = colorlog.ColoredFormatter(
            "  %(log_color)s%(levelname)-8s%(reset)s  |  "
            "%(name)-15s  |  %(log_color)s%(message)s%(reset)s"
        )
        stream = logging.StreamHandler()
        stream.setLevel(level)
        stream.setFormatter(formatter)

        root = logging.getLogger()
        root.setLevel(level)
        root.addHandler(stream)
        root.addHandler(logfile)

        # Logging necessary for selected libs
        logging.getLogger("pymongo").setLevel(logging.WARNING)
        logging.getLogger("aiohttp").setLevel(logging.WARNING)

    @web.middleware
    async def _access_log_middleware(self, request, handler):
        try:
            response = await handler(request)
            status = response.status
        except web.HTTPException as ex:
            response = ex
            status = ex.status
        finally:
            if (
                not re.search(r'^/static/', request.path)
                and not re.search(r'^/favicon.ico', request.path)
            ):
                access_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                remote_ip = request.headers.get('X-Real-IP', request.remote)
                remote_ip = request.headers.get('cf-connecting-ip', remote_ip)
                if response.status == 200:
                    self._log.info(
                        '%s "%s %s HTTP/%d.%d" %s [%s]',
                        remote_ip,
                        request.method,
                        request.path,
                        request.version.major,
                        request.version.minor,
                        status,
                        access_time
                    )
                else:
                    self._log.warning(
                        '%s "%s %s HTTP/%d.%d" %s [%s]',
                        remote_ip,
                        request.method,
                        request.path,
                        request.version.major,
                        request.version.minor,
                        status,
                        access_time
                    )
        return response
