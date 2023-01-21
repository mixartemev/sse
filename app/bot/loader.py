from aiogram import Dispatcher, Bot
from aiogram.fsm.storage.redis import RedisStorage, DefaultKeyBuilder
from dotenv import load_dotenv
from os import getenv as env

load_dotenv()

TG_URL = f'https://api.telegram.org/bot{env("BT")}/'
WH_PATH = "/bot" + env('BT').split(':')[-1]
WH_URL = "https://" + env('WH_HOST') + WH_PATH
storage = RedisStorage.from_url(env('REDIS_DSN'), key_builder=DefaultKeyBuilder(with_destiny=True))

bot = Bot(token=env('BT'))
dp = Dispatcher(storage=storage)

available_updates = (
    "message", "callback_query", "chat_member", "edited_message",
    # "pre_checkout_query", "shipping_query",
    # "inline_query", "chosen_inline_result",
    "my_chat_member",  # "poll_answer", "poll", "channel_post", "edited_channel_post"
)

commands = [
    {'command': 'start', 'description': 'Register binance user in this bot'},
    {'command': 'profile', 'description': 'User info'},
    {'command': 'cancel', 'description': 'Stop any dialog👋🏼'},
    {'command': 'run', 'description': 'Run deals receiving'},
    {'command': 'stop', 'description': 'Stop deals receiving'},
]
