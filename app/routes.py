from starlette.routing import Route, Mount
from starlette.staticfiles import StaticFiles

from app.stream import sse

routes = [
    Route('/sse', sse),
    Mount("/", StaticFiles(directory="app/front/build"), name="front")
]
