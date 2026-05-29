from fastapi import Request
from fastapi.responses import FileResponse
from mayuribin.route import Route

class Static:
    @Route.get('/favicon.ico', enable_docs=False)
    async def favicon(self, request: Request):
        return FileResponse('mayuribin/assets/images/favicon.ico')

    @Route.get('/static/css/{filename}', enable_docs=False)
    async def css(self, request: Request, filename: str):
        return FileResponse(f'mayuribin/assets/css/{filename}')

    @Route.get('/static/img/{filename}', enable_docs=False)
    async def images(self, request: Request, filename: str):
        return FileResponse(f'mayuribin/assets/images/{filename}')

    @Route.get('/static/js/{filename}', enable_docs=False)
    async def js(self, request: Request, filename: str):
        return FileResponse(f'mayuribin/assets/js/{filename}')
