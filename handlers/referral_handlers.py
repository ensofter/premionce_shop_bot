from aiogram import Router, F
from aiogram.types import CallbackQuery, InlineKeyboardButton, Message
from aiogram.utils.keyboard import InlineKeyboardBuilder

from database.database import user_db
from lexicon.lexicon_common import LEXICON_COMMON
from lexicon.lexicon_referral import LEXICON_REFERRAL
from functools import wraps


router = Router()


def ensure_user_exist_in_db(func):
    @wraps(func)
    async def wrapper(message_or_callback: Message | CallbackQuery, *args, **kwargs):
        user_id = message_or_callback.from_user.id
        if user_id not in user_db:
            await message_or_callback.message.edit_text(
                text="Такого пользователя нет в базе данных"
            )
            return
        



@router.callback_query(F.data == 'referral_url')
async def handle_clbck_button_referral_url_pressed(callback: CallbackQuery):
    user_id = callback.from_user.id
    if user_id in user_db:
        if user_id in user_db:
            kb_builder = InlineKeyboardBuilder(
                [
                    [
                        InlineKeyboardButton(
                            text=LEXICON_REFERRAL['send_referral'],
                            switch_inline_query='https://t.me/Premioncebot?start=ref_12345678'
                        )
                    ],
                    [
                        InlineKeyboardButton(text=LEXICON_COMMON['back'], callback_data='back_to_referral')
                    ]
                ]
            )
            await callback.message.edit_text(
                text='🧨 Ваша ссылка для приглашения: https://t.me/Premioncebot?start=ref_12345678',
                reply_markup=kb_builder.as_markup()
            )
    else:
        await callback.message.edit_text(
            text="Тебя тут нет"
        )


@router.callback_query(F.data == 'referral_what_is_it')
async def handle_clbck_button_send_referral_pressed(callback: CallbackQuery):
    kb_builder = InlineKeyboardBuilder(
        [
            [
                InlineKeyboardButton(text=LEXICON_COMMON['back'], callback_data='back_to_referral')
            ]
        ]
    )
    await callback.message.edit_text(
        text=LEXICON_REFERRAL['about_referral'],
        reply_markup=kb_builder.as_markup()
    )
