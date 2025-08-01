import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage

from confing.config import Config
from handlers import about_handlers
from handlers import cmd_handlers
from handlers import main_menu_handlers
from handlers import other_handlers
from handlers import profile_handlers
from handlers import referral_handlers
from keyboards.set_bot_menu import set_main_menu
from handlers import catalog_handlers
from handlers import cart_handlers

conf = Config.load_config()
logger = logging.getLogger()


async def main():
    logging.basicConfig(level=logging.DEBUG, format='[%(asctime)s - %(levelname)-8s] %(filename)s:%(lineno)d'
                                                    ' %(name)s - %(message)s')

    storage = MemoryStorage()

    bot = Bot(token=conf.tg_conf.bot_token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = Dispatcher(storage=storage)

    dp.include_routers(
        cmd_handlers.router,
        main_menu_handlers.router,
        cart_handlers.router,
        catalog_handlers.router,
        profile_handlers.router,
        referral_handlers.router,
        about_handlers.router,
        other_handlers.router
    )

    await set_main_menu(bot)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
