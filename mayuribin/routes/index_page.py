import uuid

from aiohttp import web
from mayuribin.routes import Route
from time import time

class IndexPage:
    @Route.get('/')
    async def index_page(self, request):
        header = """<!DOCTYPE html>
<html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>Mayuri Bin</title>
        <link rel="stylesheet" href="/static/css/app.css">
        <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.11.2/css/all.min.css" rel="stylesheet"/>
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/styles/default.min.css">
        <link rel="stylesheet" href="static/css/dracula.css" />

        <script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/highlight.min.js"></script>
        <script src="//cdnjs.cloudflare.com/ajax/libs/highlightjs-line-numbers.js/2.8.0/highlightjs-line-numbers.min.js"></script>
    </head>
    <body>
        <header class="unselectable">
            <div class="title">
            <a href="/" style="color: #8A8A8A; text-decoration: none">
                    <span>
                    {<i><span style="color: var(--accent-color)"><b>mayuri</b></span></i>:<i><span
                    style="color: #A8A8A8">bin</span></i>}
                    </span>
            </a>
            </div>

            <div class="hidden" id="url">
              <i class="fas fa-copy"></i>
            </div>
          
            <div class="actions">
              <button class="fas fa-save action" id="save"></button>
              <a id="raw"><button class="fas fa-code action" disabled id="raw"></button></a>
              <a href="/"><button class="fas fa-plus action" id="new"></button></a>
            </div>
        </header>
        <div id="content">
"""
        footer = open("mayuribin/assets/footer.html", "r").read()
        content = """<form action='/' method="post" id='form'>
<textarea name='content' placeholder='Paste code, save and share the link!'></textarea>
</form>
<script>
    btn = document.getElementById('save');
    btn.onclick = function() {
        document.getElementById('form').submit();
    }
</script>
"""
        text = header+content+footer
        return web.Response(text=text, content_type="text/html")

    async def index_page_post(self, request):
        data = await request.post()
        key = ''.join(str(uuid.uuid4()).split("-"))[:10]
        content = data["content"]
        now = time()
        _ = await self.db.update_one(
            {"key": key},
            {"$set": {"content": content, 'date': now}},
            upsert=True
        )
        return web.HTTPFound(f"/{key}")
