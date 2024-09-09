import uuid

from aiohttp import web
from time import time

class SaveDocument:
    async def save_document(self, request):
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
