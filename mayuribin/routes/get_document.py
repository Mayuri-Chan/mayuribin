from aiohttp import web
from mayuribin.route import Route

class GetDocument:
    @Route.swagger_get('/api/documents')
    async def get_document(self, request):
        """
        Optional route description
        ---
        summary: Get a document from the bin
        parameters:
          - name: key
            in: query
            required: true
            description: The key of the document
            schema:
                type: string
        responses:
            '200':
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
                                            example: abcde12345
                                        content:
                                            type: string
                                            example: Hello, World!
            '400':
                description: Document Key is required
                content:
                    application/json:
                        schema:
                            type: object
                            properties:
                                ok:
                                    type: boolean
                                    example: false
                                error:
                                    type: string
                                    example: Document Key is required
            '404':
                description: Document not found
                content:
                    application/json:
                        schema:
                            type: object
                            properties:
                                ok:
                                    type: boolean
                                    example: false
                                error:
                                    type: string
                                    example: Document not found
        """
        try:
            key = request.rel_url.query['key']
        except Exception:
            return web.json_response({'ok': False, 'error': 'Document Key is required'}, status=400)
        document = await self.db.find_one({"key": key})
        if not document and key != "about.md":
            return web.json_response({'ok': False, 'error': 'Document not found'}, status=404)
        if key == "about.md":
            content = open("mayuribin/assets/about.md", "r").read()
        else:
            content = document['content']
        return web.json_response({'ok': True, 'result': {'key': key, 'content': content}})
