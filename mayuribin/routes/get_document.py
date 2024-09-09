from aiohttp import web

class GetDocument:
    async def get_document(self, request):
        key = request.match_info["key"]
        document = await self.db.find_one({"key": key})
        if not document and key != "about.md":
            return web.json_response({'ok': False, 'error': 'Document not found'}, status=404)
        if key == "about.md":
            content = open("mayuribin/assets/about.md", "r").read()
        else:
            content = document['content']
        return web.json_response({'ok': True, 'result': {'key': key, 'content': content}})
