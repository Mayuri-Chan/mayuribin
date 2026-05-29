from aiohttp import web
from mayuribin.route import Route

class Static:
    @Route.get('/favicon.ico')
    async def favicon(self, request):
        return web.FileResponse('mayuribin/assets/images/favicon.ico')

    @Route.get('/static/css/{filename}')
    async def css(self, request):
        filename = request.match_info['filename']
        return web.FileResponse(f'mayuribin/assets/css/{filename}')

    @Route.get('/static/img/{filename}')
    async def images(self, request):
        filename = request.match_info['filename']
        return web.FileResponse(f'mayuribin/assets/images/{filename}')

    @Route.get('/static/js/{filename}')
    async def js(self, request):
        filename = request.match_info['filename']
        return web.FileResponse(f'mayuribin/assets/js/{filename}')
