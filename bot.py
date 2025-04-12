import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.client.default import DefaultBotProperties

from confing.config import Config
from aiogram.enums import ParseMode
from handlers import handlers
from handlers import other_handlers

conf = Config.load_config()
logger = logging.getLogger()


async def main():
    logging.basicConfig(level=logging.DEBUG, format='[%(asctime)s - %(levelname)-8s] %(filename)s:%(lineno)d'
                                                    ' %(name)s - %(message)s')

    bot = Bot(token=conf.tg_conf.bot_token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = Dispatcher()

    dp.include_routers(handlers.router, other_handlers.router)

    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
