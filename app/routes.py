from aiogram import types
from starlette.requests import Request
from starlette.responses import JSONResponse, Response
from starlette.routing import Route, Mount
from starlette.staticfiles import StaticFiles

from app.bot.form import form_router
from app.bot.loader import WH_PATH, WH_URL, bot, dp, commands, available_updates
from app.db.client import user_upd_bc
from app.stream import sse


async def on_startup():
    webhook_info = await bot.get_webhook_info()
    if webhook_info.url != WH_URL:
        await bot.set_webhook(
            url=WH_URL,
            allowed_updates=available_updates
        )
    dp.include_router(form_router)  # hz, @toDo refactor this
    # await assets_upd()
    # pss = await get_pts(user)
    await bot.set_my_commands(commands)


async def bot_webhook(request: Request):
    data = await request.json()
    telegram_update = types.Update(**data)
    res = await dp.feed_webhook_update(bot, telegram_update)
    return JSONResponse({'res': res})


async def user_bnb_upd(request: Request):
    data = await request.json()
    res = user_upd_bc(**data)
    return JSONResponse(res)


routes = [
    Route('/user/bc', user_bnb_upd, methods=["POST"]),
    Route('/sse', sse),
    Route(WH_PATH, bot_webhook, methods=["POST"]),
    Mount("/", StaticFiles(directory="app/front/build"), name="front"),
]
