import logging
from copy import deepcopy

from aiogram import Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message

from database.database import user_db, user_dict_template
from keyboards.main_menu_kb import create_main_menu_reply_kb
from lexicon.lexicon_cmd import LEXICON_CMD
import logging

router = Router()


logger = logging.getLogger(__name__)


# Хендлер обрабатывающий команду /start и возвращающий главное меню, а так же добавляющий пользователя в БД
@router.message(CommandStart())
async def handle_cmd_start(message: Message):
    user_id = message.from_user.id
    if user_id not in user_db:
        logger.info(f'Инициируем тестовую БД для пользователя {user_id}')
        user_db[user_id] = deepcopy(user_dict_template)

    await message.answer_photo(
        photo=LEXICON_CMD['welcome_photo_id'],
        caption=LEXICON_CMD['/start'],
        reply_markup=create_main_menu_reply_kb(
            3,
            'catalog',
            'promotions',
            'cart',
            'orders',
            'profile',
            'referral',
            'about'
        )
    )


# Хэндел обрабатывающий команду помощи /help
@router.message(Command(commands='help'))
async def handle_cmd_help(message: Message):
    user_id = message.from_user.id
    logger.info(f'Пользователь {user_id} запросил команду помощи /help')
    await message.answer(
        text=LEXICON_CMD['/help']
    )
