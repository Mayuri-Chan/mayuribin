from fastapi import Request
from fastapi.responses import HTMLResponse, RedirectResponse
from mayuribin.route import Route

class ServeDocument:
    @Route.get('/{key}', enable_docs=False)
    async def serve_document(self, request: Request, key: str):
        document = await self.db.fetchrow("SELECT content FROM documents WHERE key = $1", key)
        if not document and key != "about.md":
            return RedirectResponse(url="/", status_code=303)
        if key == "about.md":
            code = open("mayuribin/assets/about.md", "r").read()
        else:
            code = document["content"]
        header = open("mayuribin/assets/header.html", "r").read()
        footer = open("mayuribin/assets/footer.html", "r").read()
        content = f"""
<pre><code>{code}
</code></pre>
"""
        text = header+content+footer
        return HTMLResponse(content=text)
