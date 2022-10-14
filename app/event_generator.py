from sse_starlette import EventSourceResponse
from starlette.requests import Request

from app.get_data import get_data


async def sse(request: Request):
    return EventSourceResponse(stream(request))  # , headers={'Access-Control-Allow-Origin': '*'}


async def stream(request: Request):
    while True:
        # If client closes connection, stop sending events
        if await request.is_disconnected():
            break

        #######################
        data = await get_data()
        #######################

        yield {
            "event": "message",
            "id": data['id'],
            "data": data['val']
        }
