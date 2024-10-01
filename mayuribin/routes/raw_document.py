from aiohttp import web
from mayuribin.routes import Route

class RawDocument:
    @Route.get('/raw/{key}')
    async def raw_document(self, request):
        key = request.match_info["key"]
        document = await self.db.find_one({"key": key})
        if not document and key != "about.md":
            return web.HTTPFound("/")
        if key == "about.md":
            code = open("mayuribin/assets/about.md", "r").read()
        else:
            code = document["content"]
        return web.Response(text=code, content_type="text/plain")
