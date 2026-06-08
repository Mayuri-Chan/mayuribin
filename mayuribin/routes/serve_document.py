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
        
        import base64
        encoded_content = base64.b64encode(code.encode('utf-8')).decode('utf-8')

        if key == "about.md":
            markdown_html = f"""
            <div class="markdown-body" style="padding: 40px; max-width: 800px; margin: 0 auto; color: #f8f8f2; font-family: 'Inter', sans-serif; line-height: 1.6;">
                <div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #44475a; margin-bottom: 20px; padding-bottom: 10px;">
                    <div style="font-size: 0.9em; color: #6272a4;">Document: {{key}}</div>
                </div>
                <div id="md-content"></div>
            </div>
            <script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>
            <script>
                document.getElementById('md-content').innerHTML = marked.parse(decodeURIComponent(escape(window.atob("{encoded_content}"))));
            </script>
            <style>
                .markdown-body h1, .markdown-body h2, .markdown-body h3 {{ color: #bd93f9; margin-top: 24px; margin-bottom: 16px; font-weight: 600; line-height: 1.25; }}
                .markdown-body h1 {{ font-size: 2em; border-bottom: 1px solid #44475a; padding-bottom: .3em; }}
                .markdown-body h2 {{ font-size: 1.5em; border-bottom: 1px solid #44475a; padding-bottom: .3em; }}
                .markdown-body a {{ color: #8be9fd; text-decoration: none; }}
                .markdown-body a:hover {{ text-decoration: underline; }}
                .markdown-body code {{ background-color: rgba(255,255,255,0.1); padding: 0.2em 0.4em; border-radius: 6px; font-family: monospace; font-size: 85%; }}
                .markdown-body pre {{ background-color: #1e1f29; padding: 16px; border-radius: 8px; overflow-x: auto; }}
                .markdown-body pre code {{ background-color: transparent; padding: 0; font-size: 100%; }}
                .markdown-body blockquote {{ border-left: 4px solid #6272a4; padding: 0 1em; color: #f8f8f2; opacity: 0.8; margin: 0 0 16px 0; }}
                .markdown-body ul, .markdown-body ol {{ padding-left: 2em; margin-top: 0; margin-bottom: 16px; }}
                .markdown-body p {{ margin-top: 0; margin-bottom: 16px; }}
                .markdown-body img {{ max-width: 100%; box-sizing: content-box; }}
                .markdown-body kbd {{ display: inline-block; padding: 3px 5px; font-size: 11px; line-height: 10px; color: #282a36; vertical-align: middle; background-color: #f8f8f2; border: solid 1px #bd93f9; border-bottom-color: #bd93f9; border-radius: 3px; box-shadow: inset 0 -1px 0 #bd93f9; }}
            </style>
            """
            text = header + markdown_html + footer
            return HTMLResponse(content=text)

        try:
            lexer = guess_lexer(code)
            language_name = lexer.name
        except ClassNotFound:
            lexer = TextLexer()
            language_name = "Text"
            
        formatter = HtmlFormatter(style="dracula", linenos="table", cssclass="highlight")
        pygments_css = formatter.get_style_defs('.highlight')
        
        highlighted_code = highlight(code, lexer, formatter)
        
        content = f"""
<style>
{pygments_css}
.language-banner-container {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    background-color: #282a36;
    color: #f8f8f2;
    padding: 5px 15px;
    border-bottom: 1px solid #444;
    border-top-left-radius: 5px;
    border-top-right-radius: 5px;
    font-family: monospace;
    font-size: 0.9em;
    margin-bottom: 0;
    position: relative;
    z-index: 10;
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
.highlight {{
    overflow-x: auto;
    border-bottom-left-radius: 5px;
    border-bottom-right-radius: 5px;
    background-color: #282a36;
}}
.highlighttable {{
    width: 100%;
    margin: 0;
    border-spacing: 0;
}}
.highlighttable td.linenos {{
    width: 1%;
    padding-right: 15px;
    text-align: right;
    color: #6272a4;
    user-select: none;
}}
.highlighttable td.code {{
    width: 99%;
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
