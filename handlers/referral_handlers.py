from aiogram import Router, F
from aiogram.types import CallbackQuery, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from lexicon.lexicon_common import LEXICON_COMMON
from lexicon.lexicon_referral import LEXICON_REFERRAL

router = Router()


@router.callback_query(F.data == 'referral_url')
async def handle_clbck_button_referral_url_pressed(callback: CallbackQuery):
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
