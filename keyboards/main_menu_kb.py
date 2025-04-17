from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from lexicon.lexicon_main_menu import LEXICON_MM


def create_main_menu_reply_kb(width: int, *args: str, **kwargs: str) -> ReplyKeyboardMarkup:
    kb_builder = ReplyKeyboardBuilder()

    buttons: list[KeyboardButton] = []

    if args:
        for button in args:
            buttons.append(
                KeyboardButton(
                    text=LEXICON_MM[button] if button in LEXICON_MM else button,
                )
            )

    if kwargs:
        for button, text in kwargs.items():
            buttons.append(
                KeyboardButton(
                    text=text
                )
            )

    kb_builder.row(*buttons, width=width)

    return kb_builder.as_markup(resize_keyboard=True)
