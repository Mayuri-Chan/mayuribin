import asyncpg
import logging
import re

from contextlib import asynccontextmanager
from datetime import datetime
from fastapi import FastAPI, Request, Response
from mayuribin import config
from mayuribin.route import Route
from mayuribin.routes import Routes


@asynccontextmanager
async def prepare_db(app: FastAPI):
    app.pool = await asyncpg.create_pool(app.config['postgresql']['URL'])
    async with app.pool.acquire() as conn:
        await conn.execute('''
            CREATE TABLE IF NOT EXISTS documents (
                key VARCHAR(10) PRIMARY KEY,
                content TEXT,
                date DOUBLE PRECISION
            )
        ''')
    app.db = app.pool
    yield
    await app.pool.close()


class MayuriBin(FastAPI, Route, Routes):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, lifespan=prepare_db, title="Mayuri-bin API", version="1.0.0")
        self.config = config
        self.logger = logging.getLogger("uvicorn.error")
        self.load_routes()
        self.middleware("http")(self.access_log_middleware)

    def get_remote_ip(self, request: Request) -> str:
        remote_ip = request.headers.get('X-Real-IP') or (request.client.host if request.client else "127.0.0.1")
        remote_ip = request.headers.get('cf-connecting-ip', remote_ip)
        return remote_ip

    async def access_log_middleware(self, request: Request, call_next):
        try:
            response: Response = await call_next(request)
            status = response.status_code
        except Exception as ex:
            status = getattr(ex, "status_code", 500)
            raise ex
        finally:
            if not re.search(r'^/static/', request.url.path) and not re.search(r'^/favicon.ico', request.url.path):
                access_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                remote_ip = self.get_remote_ip(request)
                http_version = request.scope.get("http_version", "1.1")

                try:
                    from http import HTTPStatus
                    status_phrase = HTTPStatus(status).phrase
                except ValueError:
                    status_phrase = ""

                if status >= 500:
                    color = "\033[91m"  # Bright Red
                elif status >= 400:
                    color = "\033[31m"  # Red
                elif status >= 300:
                    color = "\033[33m"  # Yellow
                elif status >= 200:
                    color = "\033[32m"  # Green
                else:
                    color = "\033[37m"  # White

                colored_status = f"{color}{status} {status_phrase}\033[0m".strip()

                query = request.url.query
                full_path = f"{request.url.path}?{query}" if query else request.url.path
                log_msg = f'{remote_ip} - "{request.method} {full_path} HTTP/{http_version}" {colored_status} [{access_time}]'
                log_msg = log_msg.replace("  ", " ")

                if status < 400:
                    self.logger.info(log_msg)
                else:
                    self.logger.warning(log_msg)

        return response

mayuribin = MayuriBin()
