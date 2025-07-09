from aiogram import Bot
from aiogram.types import BotCommand

from lexicon.lexicon_bot_menu import LEXICON_BOT_COMMANDS_RU


async def set_main_menu(bot: Bot):
    main_menu_commands = [
        BotCommand(
            command=command,
            description=desc
        ) for command, desc in LEXICON_BOT_COMMANDS_RU.items()
    ]
    await bot.set_my_commands(main_menu_commands)
