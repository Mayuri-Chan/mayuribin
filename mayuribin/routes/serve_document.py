from aiohttp import web

class ServeDocument:
    async def serve_document(self, request):
        key = request.match_info["key"]
        document = await self.db.find_one({"key": key})
        if not document and key != "about.md":
            return web.HTTPFound("/")
        if key == "about.md":
            code = open("mayuribin/assets/about.md", "r").read()
        else:
            code = document["content"]
        header = open("mayuribin/assets/header.html", "r").read()
        footer = open("mayuribin/assets/footer.html", "r").read()
        content = f"<pre><code>{code}</code></pre>"
        text = header+content+footer
        return web.Response(text=text, content_type="text/html")
