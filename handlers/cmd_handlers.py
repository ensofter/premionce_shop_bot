import logging
from copy import deepcopy

from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery

from database.database import user_db, user_dict_template
from keyboards.main_menu_kb import create_main_menu_reply_kb
from lexicon.lexicon_cmd import LEXICON_CMD

router = Router()

logger = logging.getLogger(__name__)


# Хендлер обрабатывающий команду /start и возвращающий главное меню, а так же добавляющий пользователя в БД
@router.message(CommandStart())
@router.callback_query(F.data == "back_to_main_menu")
async def handle_cmd_start(message_or_callback: Message | CallbackQuery):
    user_id = message_or_callback.from_user.id
    reply_kb = create_main_menu_reply_kb(
        3,
        'catalog',
        'promotions',
        'cart',
        'orders',
        'profile',
        'referral',
        'about'
    )
    if isinstance(message_or_callback, Message):
        if user_id not in user_db:
            logger.info(f'Инициируем тестовую БД для пользователя {user_id}')
            user_db[user_id] = deepcopy(user_dict_template)

        await message_or_callback.answer_photo(
            photo=LEXICON_CMD['welcome_photo_id'],
            caption=LEXICON_CMD['/start'],
            reply_markup=reply_kb
        )
    else:
        await message_or_callback.message.edit_reply_markup(reply_markup=None)
        await message_or_callback.message.answer(
            text=LEXICON_CMD['/start'],
            reply_markup=reply_kb
        )
        await message_or_callback.answer()


# Хэндел обрабатывающий команду помощи /help
@router.message(Command(commands='help'))
async def handle_cmd_help(message: Message):
    user_id = message.from_user.id
    logger.info(f'Пользователь {user_id} запросил команду помощи /help')
    await message.answer(
        text=LEXICON_CMD['/help']
    )
