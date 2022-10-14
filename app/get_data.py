from asyncio import sleep
from random import randint


async def get_data() -> {}:
    await sleep(randint(1, 3))  # seconds
    i = randint(0, 42)
    return {'id': i, 'val': f'Message#{i}'}
