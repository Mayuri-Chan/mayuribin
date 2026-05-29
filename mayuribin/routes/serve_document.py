from fastapi import Request
from fastapi.responses import HTMLResponse, RedirectResponse
from mayuribin.route import Route
from pygments import highlight
from pygments.lexers import guess_lexer, TextLexer
from pygments.formatters import HtmlFormatter
from pygments.util import ClassNotFound
import base64

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
        
        try:
            lexer = guess_lexer(code)
            language_name = lexer.name
        except ClassNotFound:
            lexer = TextLexer()
            language_name = "Text"
            
        formatter = HtmlFormatter(linenos=True, cssclass="source", style="dracula")
        pygments_css = formatter.get_style_defs('.source')
        
        highlighted_code = highlight(code, lexer, formatter)
        
        encoded_content = base64.b64encode(code.encode('utf-8')).decode('utf-8')
        
        content = f"""
<style>
{pygments_css}
/* Add some additional styling for pygments line numbers and language banner */
.source pre {{ margin: 0; }}
.source .linenos {{ color: #888; padding-right: 10px; user-select: none; border-right: 1px solid #444; margin-right: 10px; }}
.language-banner-container {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    background-color: #282a36;
    color: #f8f8f2;
    padding: 5px 15px;
    font-family: monospace;
    font-size: 0.9em;
    border-bottom: 1px solid #444;
}}
.language-name {{
    text-transform: uppercase;
    opacity: 0.8;
}}
.copy-code-btn {{
    background: none;
    border: none;
    color: #f8f8f2;
    cursor: pointer;
    opacity: 0.8;
    font-family: monospace;
    font-size: 1em;
    display: flex;
    align-items: center;
    gap: 5px;
    outline: none;
}}
.copy-code-btn:hover {{
    opacity: 1;
}}
</style>
<div class="language-banner-container">
    <div class="language-name">{{language_name}}</div>
    <button class="copy-code-btn" onclick="copyCode(this)"><i class="fas fa-copy"></i> Copy</button>
</div>
<script>
function copyCode(btn) {{
    const code = decodeURIComponent(escape(window.atob("{encoded_content}")));
    navigator.clipboard.writeText(code).then(() => {{
        const originalHtml = btn.innerHTML;
        btn.innerHTML = '<i class="fas fa-check"></i> Copied!';
        setTimeout(() => {{
            btn.innerHTML = originalHtml;
        }}, 2000);
    }}).catch(err => {{
        console.error('Failed to copy text: ', err);
    }});
}}
</script>
{highlighted_code}
"""
        text = header+content+footer
        return HTMLResponse(content=text)
