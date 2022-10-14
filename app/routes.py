from starlette.routing import Route, Mount
from starlette.staticfiles import StaticFiles

from app.event_generator import sse
from app.front import html

routes = [
    Route('/sse', sse),
    Route("/", endpoint=html),
    Mount("/static", StaticFiles(directory="static"), name="static")
]
