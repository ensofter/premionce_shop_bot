from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from lexicon.lexicon_main_menu import LEXICON_MM


def create_inline_kb(width: int, lexicon: dict, *args: str, **kwargs: str) -> InlineKeyboardBuilder:
    kb_builder = InlineKeyboardBuilder()

    buttons: list[InlineKeyboardButton] = []

    if args:
        for button in args:
            buttons.append(
                InlineKeyboardButton(
                    text=lexicon[button] if button in lexicon else button,
                    callback_data=button
                )
            )

    if kwargs:
        for button, text in kwargs.items():
            buttons.append(
                InlineKeyboardButton(
                    text=text,
                    callback_data=button
                )
            )

    kb_builder.row(*buttons, width=width)

    return kb_builder
