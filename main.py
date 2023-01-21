from starlette.applications import Starlette
from app.routes import routes, on_startup

app = Starlette(
    debug=True,
    routes=routes,
    on_startup=[on_startup],
    # on_shutdown=[some_shutdown_task]
)
