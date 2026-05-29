import uuid

from aiohttp import web
from mayuribin.route import Route
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
            <a href="/">
                    <span>
                    {<i><span style="color: var(--accent-color)"><b>mayuri</b></span></i>:<i><span
                    class="subtitle">bin</span></i>}
                    </span>
            </a>
            </div>

            <div class="hidden" id="url">
              <i class="fas fa-copy"></i>
            </div>

            <div class="actions">
              <button class="fas fa-save action" id="save_btn" disabled></button>
              <a id="raw_link"><button class="fas fa-code action" disabled id="raw"></button></a>
              <a href="/"><button class="fas fa-plus action" id="new"></button></a>
            </div>
        </header>
        <div id="content">
"""
        footer = open("mayuribin/assets/footer.html", "r").read()
        csrf_token = str(uuid.uuid4())
        content = """<form action='/' method="post" id='form'>
<input type='hidden' name='csrf_token' value='""" + csrf_token + """'>
<textarea name='content' id='content_text' placeholder='Paste code, save and share the link!'></textarea>
<p id="size-warning" style="color: red; display: none;">The content is too large to be saved (limit is 512KB).</p>
</form>
<script>
    const btn = document.getElementById('save_btn');
    const textarea = document.getElementById('content_text');
    const warning = document.getElementById('size-warning');
    const encoder = new TextEncoder();
    const maxLength = 524288; // 512KB
    const toLargeWarningMessage = "The content is too large to be saved (limit is 512KB).";
    const emptyWarningMessage = "Content cannot be empty.";

    textarea.addEventListener('input', function() {
        const text = this.value;
        const byteLength = encoder.encode(text).length;
        const isEmpty = text.trim() === '';
        const isTooLarge = byteLength > maxLength;

        btn.disabled = isTooLarge || isEmpty;
        btn.title = emptyWarningMessage;
        
        if (isTooLarge) {
            btn.title = toLargeWarningMessage;
        } else if (isEmpty) {
            btn.title = emptyWarningMessage;
        } else {
            btn.title = "Save Document";
        }
    });

    btn.onclick = function() {
        document.getElementById('form').submit();
    }
</script>
"""
        text = header+content+footer
        response = web.Response(text=text, content_type="text/html")
        response.set_cookie('csrf_token', csrf_token, httponly=True)
        return response

    async def index_page_post(self, request):
        data = await request.post()
        key = ''.join(str(uuid.uuid4()).split("-"))[:10]
        content = data["content"]
        now = time()
        _ = await self.db.execute(
            "INSERT INTO documents (key, content, date) VALUES ($1, $2, $3) ON CONFLICT (key) DO UPDATE SET content = EXCLUDED.content, date = EXCLUDED.date",
            key, content, now
        )
        return web.HTTPFound(f"/{key}")
