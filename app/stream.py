import json
from time import time

from sse_starlette import EventSourceResponse
from starlette.requests import Request

from app.bc2c.main import cycle


async def sse(request: Request):
    return EventSourceResponse(event_generator(request), headers={'Access-Control-Allow-Origin': '*'})


async def event_generator(request: Request):
    first = True
    while True:
        # If client closes connection, stop sending events
        if await request.is_disconnected():
            break

        #######################
        data = await cycle(first)
        if first:
            first = False
        #######################

        yield {
            "event": "message",
            "id": int(time()),
            "data": json.dumps(data)
        }
