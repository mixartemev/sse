from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from pony.orm import db_session

from app.db.models import User, Cur

# from libs.client import ping
# from libs.db import get_user_by_tg, get_user_by_gmail

form_router = Router()


class Form(StatesGroup):
    gmail = State()
    fiat = State()


@form_router.message(Command(commands=["start"]))
async def command_start(message: Message, state: FSMContext) -> None:
    await state.set_state(Form.gmail)
    await message.answer(f"Hi, {message.from_user.full_name}, input your gmail please")


@form_router.message(F.text.casefold().contains("cancel"))
async def state_clear(message: Message, state: FSMContext) -> None:
    await state.clear()
    await message.answer("Register at binance and come back.\nSee you soon👋🏼", reply_markup=ReplyKeyboardRemove())


@form_router.message(Form.gmail)
async def process_gmail(message: Message, state: FSMContext) -> None:
    res = await state.update_data(gmail=message.text)
    with db_session:
        if user := User.get(gmail=message.text):
            user.set(tg_id=message.from_user.id)
            await state.set_state(Form.fiat)
            await message.answer(
                f"Ok, {message.text}.\nWhich fiat currency are you using?",
                reply_markup=ReplyKeyboardMarkup(
                    keyboard=[
                        [
                            KeyboardButton(text="RUB"),
                            KeyboardButton(text="USD"),
                            KeyboardButton(text="EUR"),
                        ],
                        [
                            KeyboardButton(text="TRY"),
                            KeyboardButton(text="AED"),
                            KeyboardButton(text="KZT"),
                        ]
                    ],
                    resize_keyboard=True
                )
            )
        else:
            await message.answer(
                f"Gmail {message.text} isn't registered.\nWrite correct gmail:",
                reply_markup=ReplyKeyboardMarkup(
                    keyboard=[[KeyboardButton(text="Cancel")]],
                    resize_keyboard=True
                )
            )


@form_router.message(Form.fiat)
async def process_fiat(message: Message, state: FSMContext) -> None:
    if message.text in ('RUB', 'USD', 'EUR', 'AED', 'TRY', 'KZT'):
        # await state.update_data(fiat=message.text)
        # data = await state.get_data()
        await state.clear()
        with db_session:
            if user := User.get(tg_id=message.from_user.id):
                user.set(cur=Cur[message.text], ran=False)
        await message.answer(await _get_prof_msg(message.from_user.id), reply_markup=ReplyKeyboardRemove())
    else:
        await message.answer(f"Fiat currency: {message.text} isn't exist.\nChoose correct option:")


# @form_router.message(commands=["profile"])
# async def command_profile(message: Message) -> None:
#     msg = await _get_prof_msg(message.from_user.id)
#     await message.answer(f"Profile: {message.from_user.full_name}\n{msg}")


async def _get_prof_msg(tg_id: int):
    with db_session:
        if user := User.get(tg_id=tg_id):
            status = True  # await ping(user)
            return f"b_id: {user.uid}\ngmail: {user.gmail}\ncur: {user.cur.name}\nsigned: {'in' if status else 'out'}\n"
        else:
            return f"TG user {tg_id} isn't registered.\n/start"


# @form_router.message(commands=["run"])
# async def run(msg: Message):
#     user = await get_user_by_tg(msg.from_user.id)
#     return users_db.update({'ran': True}, user['key'])
#
#
# @form_router.message(commands=["stop"])
# async def stop(msg: Message):
#     user = await get_user_by_tg(msg.from_user.id)
#     return users_db.update({'ran': False}, user['key'])


@form_router.message()
async def command_profile(message: Message) -> None:
    await message.delete()
