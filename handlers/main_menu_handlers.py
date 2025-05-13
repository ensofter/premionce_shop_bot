from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton

from database.database import user_db
from keyboards.inline_kb import create_inline_kb
from lexicon.lexicon_inline_kb import LEXICON_INLINE_KB
from lexicon.lexicon_main_menu import LEXICON_MM

router = Router()


@router.message(F.text == '🩷 Реферальная программа')
@router.callback_query(F.data == 'back_to_referral')
async def handle_referral(message_or_callback: Message | CallbackQuery):
    user_id = message_or_callback.from_user.id

    reply_kb = create_inline_kb(
        1,
        LEXICON_INLINE_KB,
        'referral_url',
        'referral_what_is_it'
    )

    text = '🫂 Реферальная программа\n\n' \
           f'Ваших рефералов: {user_db[user_id]["referral"]["total_referral"]}\n' \
           f'Общий заработок: {user_db[user_id]["referral"]["total_income"]} ₽\n' \
           f'Текущий ваш баланс: {user_db[user_id]["referral"]["balance"]} ₽\n\n' \
           'Рекламируй PREMIONCE shop среди своих знакомых и зарабатывай ₽ с их покупок.'

    if isinstance(message_or_callback, Message):
        await message_or_callback.answer(
            text=text,
            reply_markup=reply_kb.as_markup()
        )
    else:
        await message_or_callback.message.edit_text(
            text=text,
            reply_markup=reply_kb.as_markup()
        )


@router.message(F.text == '🍥 О нас')
@router.callback_query(F.data == 'back_to_about')
async def handle_about(message_or_callback: Message | CallbackQuery):
    reply_kb = create_inline_kb(
        1,
        LEXICON_INLINE_KB,
        'faq',
    )
    reply_kb.row(InlineKeyboardButton(text='‍💻 Менеджер', url="tg://user?id=82429730"))

    text = LEXICON_MM['🍥 О нас']

    if isinstance(message_or_callback, CallbackQuery):
        await message_or_callback.message.edit_text(text=text, reply_markup=reply_kb.as_markup())
    else:
        await message_or_callback.answer(text=text, reply_markup=reply_kb.as_markup())
