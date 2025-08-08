import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage

from confing.config import Config
from handlers.about_handlers import router as about_router
from handlers.cmd_handlers import router as cmd_router
from handlers.main_menu_handlers import router as main_menu_router
from handlers.other_handlers import router as other_router
from handlers.profile_handlers import router as profile_router
from handlers.referral_handlers import router as referral_router
from keyboards.set_bot_menu import set_main_menu
from handlers.catalog_handlers import router as catalog_router
from handlers.cart_handlers import router as cart_router

conf = Config.load_config()
logger = logging.getLogger()


async def main():
    logging.basicConfig(level=logging.DEBUG, format='[%(asctime)s - %(levelname)-8s] %(filename)s:%(lineno)d'
                                                    ' %(name)s - %(message)s')

    storage = MemoryStorage()

    bot = Bot(token=conf.tg_conf.bot_token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = Dispatcher(storage=storage)

    dp.include_routers(
        cmd_router,
        main_menu_router,
        cart_router,
        catalog_router,
        profile_router,
        referral_router,
        about_router,
        other_router
    )

    await set_main_menu(bot)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
