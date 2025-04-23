from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from lexicon.lexicon_common import LEXICON_COMMON


def create_pagination_keyboard(*buttons: str) -> InlineKeyboardBuilder:
    kb_builder = InlineKeyboardBuilder()
    for button in buttons:
        if button:
            b = button.split(':')[0]
            kb_builder.add(
                InlineKeyboardButton(
                    text=LEXICON_COMMON[b] if b in LEXICON_COMMON else b,
                    callback_data=button
                )
            )
        else:
            continue
    return kb_builder
