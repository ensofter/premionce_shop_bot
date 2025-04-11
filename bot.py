import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart
from aiogram.types import Message

from confing.config import Config

conf = Config.load_config()
logger = logging.getLogger()


async def main():
    logging.basicConfig(level=logging.DEBUG, format='[%(asctime)s - %(levelname)-8s] %(filename)s:%(lineno)d'
                                                    ' %(name)s - %(message)s')

    bot = Bot(token=conf.tg_conf.bot_token)
    dp = Dispatcher()

    @dp.message(CommandStart())
    async def handle_cmd_start(message: Message):
        await message.answer(text='Hello motherfucker')

    @dp.message()
    async def handle_every_message(message: Message):
        await message.answer(text='Любой текст')

    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
