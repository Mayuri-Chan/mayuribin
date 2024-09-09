import asyncio
import colorlog
import logging
import re

from aiohttp import web
from async_pymongo import AsyncClient
from datetime import datetime
from mayuribin import config
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

    async def run(self):
        self._setup_log()
        self.middlewares.append(self._access_log_middleware)
        self._log.info("Mayuri-Bin is starting up...")
        self._setup_routes()
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

    def _setup_routes(self):
        self.add_routes(
            [
                web.get('/', self.index_page),
                web.post('/', self.index_page_post),
                web.get('/favicon.ico', self.favicon),
                web.get('/static/css/{filename}', self.css),
                web.get('/static/img/{filename}', self.images),
                web.get('/raw/{key}', self.raw_document),
                web.get('/{key}', self.serve_document)
            ]
        )
        if self.config["app"]["ENABLE_API"]:
            self.add_routes(
                [
                    web.get('/api/documents/{key}', self.get_document),
                    web.post('/api/documents', self.save_document),
                ]
            )

    async def favicon(self, request):
        return web.FileResponse('mayuribin/assets/images/favicon.ico')

    async def css(self, request):
        filename = request.match_info['filename']
        return web.FileResponse(f'mayuribin/assets/css/{filename}')

    async def images(self, request):
        filename = request.match_info['filename']
        return web.FileResponse(f'mayuribin/assets/images/{filename}')

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
                if response.status == 200:
                    self._log.info(
                        '%s "%s %s HTTP/%d.%d" %s [%s]',
                        request.headers.get('X-Real-IP', request.remote),
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
                        request.headers.get('X-Real-IP', request.remote),
                        request.method,
                        request.path,
                        request.version.major,
                        request.version.minor,
                        status,
                        access_time
                    )
        return response
