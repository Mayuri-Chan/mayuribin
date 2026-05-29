from fastapi import Request, Response
from fastapi.responses import RedirectResponse
from mayuribin.route import Route

class RawDocument:
    @Route.get('/raw/{key}', enable_docs=False)
    async def raw_document(self, request: Request, key: str):
        document = await self.db.fetchrow("SELECT content FROM documents WHERE key = $1", key)
        if not document and key != "about.md":
            return RedirectResponse(url="/", status_code=303)
        if key == "about.md":
            code = open("mayuribin/assets/about.md", "r").read()
        else:
            code = document["content"]
        return Response(content=code, media_type="text/plain")
