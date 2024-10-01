import uuid

from aiohttp import web
from mayuribin.routes import Route
from time import time

class SaveDocument:
    @Route.post('/api/documents')
    async def save_document(self, request):
        if self.config["app"]["ENABLE_API"] is False:
            return web.json_response({'ok': False, 'error': 'API is disabled'}, status=403)
        data = await request.json()
        key = ''.join(str(uuid.uuid4()).split("-"))[:10]
        content = data["content"]
        now = time()
        _ = await self.db.update_one(
            {"key": key},
            {"$set": {"content": content, 'date': now}},
            upsert=True
        )
        response = {
            'ok': True,
            'result': {
                'key': key,
                'title': None,
                'author': None,
                'date': now,
                'views': 0,
                'length': len(content),
                'content': content
            }
        }
        return web.json_response(response)
