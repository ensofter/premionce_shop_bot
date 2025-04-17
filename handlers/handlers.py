from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton
from lexicon.lexicon_cmd import LEXICON_CMD
from lexicon.lexicon_faq import LEXICON_FAQ
from lexicon.lexicon_inline_kb import LEXICON_INLINE_KB
from lexicon.lexicon_main_menu import LEXICON_MM
from keyboards.main_menu_kb import create_main_menu_reply_kb
from keyboards.inline_kb import create_inline_kb

router = Router()


@router.message(CommandStart())
async def handle_cmd_start(message: Message):
    await message.answer_photo(
        photo=LEXICON_CMD['welcome_photo_id'],
        caption=LEXICON_CMD['/start'],
        reply_markup=create_main_menu_reply_kb(
            3, 'catalog', 'promotions', 'cart', 'orders', 'profile', 'referral', 'about'
        )
    )


@router.message(F.text == '🍥 О нас')
async def handle_reply_button_about(message: Message):
    reply_kb = create_inline_kb(
        1,
        LEXICON_INLINE_KB,
        'faq',
    )
    reply_kb.row(InlineKeyboardButton(text='‍💻 Менеджер', url="tg://user?id=82429730"))
    await message.answer(
        text=LEXICON_MM['🍥 О нас'],
        reply_markup=reply_kb.as_markup()
    )


@router.callback_query(F.data == 'faq')
async def handle_clbck_button_faq(callback: CallbackQuery):
    reply_kb = create_inline_kb(
        1,
        LEXICON_FAQ,
        first='Ваша продукция легальна?',
        second='Вам можно доверять?',
        third='Ваши преимущества?',
    )
    reply_kb.row(InlineKeyboardButton(text='🔙 Назад', callback_data='back_to_about'))
    await callback.message.edit_text(
        text='👨‍🏫 Выберите вопрос',
        reply_markup=reply_kb.as_markup()
    )


@router.callback_query(F.data.in_(['first', 'second', 'third']))
async def handle_clbck_button_faq_question(callback: CallbackQuery):
    await callback.message.edit_text(
        text=LEXICON_FAQ[callback.data],
    )


@router.callback_query(F.data == 'back_to_about')
async def handle_clbck_button_faq_back(callback: CallbackQuery):
    reply_kb = create_inline_kb(
        1,
        LEXICON_INLINE_KB,
        'faq',
    )
    reply_kb.row(InlineKeyboardButton(text='‍💻 Менеджер', url="tg://user?id=82429730"))
    await callback.message.edit_text(
        text=LEXICON_MM['🍥 О нас'],
        reply_markup=reply_kb.as_markup()
    )



@router.message(Command(commands='help'))
async def handle_cmd_help(message: Message):
    await message.answer(
        text=LEXICON_CMD['/help']
    )