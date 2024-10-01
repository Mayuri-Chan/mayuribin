import uuid

from aiohttp import web
from mayuribin.routes import Route
from time import time

class SaveDocument:
    @Route.swagger_post('/api/documents')
    async def save_document(self, request):
        """
        Optional route description
        ---
        summary: Save a document to the bin
        requestBody:
            required: true
            content:
                application/json:
                    schema:
                        type: object
                        properties:
                            content:
                                type: string
                                description: The content of the document
        responses:
            "200":
                description: successful operation
                content:
                    application/json:
                        schema:
                            type: object
                            properties:
                                ok:
                                    type: boolean
                                result:
                                    type: object
                                    properties:
                                        key:
                                            type: string
                                        url:
                                            type: string
                                        date:
                                            type: integer
                                        length:
                                            type: integer
                                        content:
                                            type: string
            "400":
                description: Invalid input
                content:
                    application/json:
                        schema:
                            type: object
                            properties:
                                ok:
                                    type: boolean
                                    example: false
                                description:
                                    type: string
                                    example: Invalid input
        """
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
