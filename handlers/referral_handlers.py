import logging

from aiogram import Router, F
from aiogram.types import CallbackQuery, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from database.database import user_db
from lexicon.lexicon_common import LEXICON_COMMON
from lexicon.lexicon_referral import LEXICON_REFERRAL

router = Router()

logger = logging.getLogger(__name__)


@router.callback_query(F.data == 'referral_url')
async def handle_button_referral_url_pressed(callback: CallbackQuery):
    user_id = callback.from_user.id
    if user_id in user_db:
        if user_id in user_db:
            logger.info(f'Пользователь {user_id} запросил свою реферальную ссылку')
            user_db[user_id].referral.generate_key(user_id)
            referral_key = f"https://t.me/ohta_stringer_bot?start={user_db[user_id].referral.referral_key}"
            kb_builder = InlineKeyboardBuilder(
                [
                    [
                        InlineKeyboardButton(
                            text=LEXICON_REFERRAL['send_referral'],
                            switch_inline_query=referral_key
                        )
                    ],
                    [
                        InlineKeyboardButton(text=LEXICON_COMMON['back'], callback_data='back_to_referral')
                    ]
                ]
            )
            await callback.message.edit_text(
                text=LEXICON_REFERRAL['your_referral_key'](referral_key),
                reply_markup=kb_builder.as_markup()
            )
    else:
        logger.info(f'Пользователя нет в БД')
        await callback.message.edit_text(
            text=LEXICON_COMMON['user_not_exist']
        )


@router.callback_query(F.data == 'referral_what_is_it')
async def handle_clbck_button_send_referral_pressed(callback: CallbackQuery):
    user_id = callback.from_user.id
    logger.info(f'Пользователь {user_id} читает что такое реферальная программа')
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
