from typing import Dict

from aiogram.utils.keyboard import InlineKeyboardBuilder

from database.database import CartItem
from lexicon.lexicon_cart import LEXICON_CART
from lexicon.lexicon_main_menu import LEXICON_MM


def create_cart_keyboard(items: Dict[int, CartItem]):
    builder = InlineKeyboardBuilder()

    for i in items.values():
        builder.button(text=f"{i.price_per_unit}", callback_data="1111")
        builder.button(text="➖", callback_data="decrease_quantity")
        builder.button(text=f"{i.quantity}", callback_data="222")
        builder.button(text="➕", callback_data="increase_quantity")


    builder.button(text=LEXICON_MM['catalog'], callback_data="back_to_catalog")
    builder.button(text=LEXICON_CART['clear_cart'], callback_data="clear_cart")

    builder.button(text=LEXICON_CART['buy'], callback_data="buy")

    builder.button(text="🔙 Назад", callback_data='back_to_cart')

    builder.adjust(4, 2, 1, 1)

    return builder.as_markup()
