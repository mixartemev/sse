from starlette.applications import Starlette
from app.routes import routes

app = Starlette(debug=True, routes=routes)
