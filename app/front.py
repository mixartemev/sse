from starlette.requests import Request
from starlette.responses import HTMLResponse


async def html(request: Request):
    await request.send_push_promise("/static/sse.js")
    return HTMLResponse('<html><body><pre id="data"/></body><script src="/static/sse.js"></script></html>')
