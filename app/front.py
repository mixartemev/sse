from starlette.requests import Request
from starlette.responses import HTMLResponse


async def html(request: Request):
    return HTMLResponse('<html><script defer src="/static/sse.js"></script><body><pre id="data"/></body></html>')
