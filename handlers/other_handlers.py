from copy import deepcopy

from aiogram import F
from aiogram import Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, PhotoSize

from database.database import user_db, user_dict_template
from keyboards.main_menu_kb import create_main_menu_reply_kb
from lexicon.lexicon_cmd import LEXICON_CMD

router = Router()


@router.message(CommandStart())
async def handle_cmd_start(message: Message):
    user_id = message.from_user.id
    if user_id not in user_db:
        user_db[user_id] = deepcopy(user_dict_template)

    await message.answer_photo(
        photo=LEXICON_CMD['welcome_photo_id'],
        caption=LEXICON_CMD['/start'],
        reply_markup=create_main_menu_reply_kb(
            3, 'catalog', 'promotions', 'cart', 'orders', 'profile', 'referral', 'about'
        )
    )


@router.message(Command(commands='help'))
async def handle_cmd_help(message: Message):
    await message.answer(
        text=LEXICON_CMD['/help']
    )


@router.message(F.photo[-1].as_('largest_photo'))
async def handle_img(message: Message, largest_photo: PhotoSize):
    print('!!!', largest_photo.file_unique_id)
    print('!!!', largest_photo.file_id)


@router.message()
async def handle_every_message(message: Message):
    await message.answer(text='Любой текст')
