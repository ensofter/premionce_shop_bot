from typing import Dict

from aiogram.utils.keyboard import InlineKeyboardBuilder

from database.database import CartItem
from lexicon.lexicon_cart import LEXICON_CART
from lexicon.lexicon_main_menu import LEXICON_MM


def create_cart_keyboard(items: Dict[int, CartItem]):
    builder = InlineKeyboardBuilder()

    # Добавляем кнопки для каждого товара в корзине (по 4 в ряд)
    for item_id, item in items.items():
        builder.button(text=f"{item.name}", callback_data=f"price_{item_id}")
        builder.button(text="➖", callback_data=f"decrease_{item_id}")
        builder.button(text=f"{item.quantity}", callback_data=f"quantity_{item_id}")
        builder.button(text="➕", callback_data=f"increase_{item_id}")

    # Добавляем остальные кнопки
    builder.button(text=LEXICON_MM['catalog'], callback_data="back_to_catalog")
    builder.button(text=LEXICON_CART['clear_cart'], callback_data="clear_cart")
    builder.button(text=LEXICON_CART['buy'], callback_data="buy")
    builder.button(text="🔙 Назад", callback_data='back_to_catalog')

    # Настраиваем расположение кнопок:
    # - сначала все товарные строки по 4 кнопки
    # - затем каталог и очистка (2 кнопки в ряд)
    # - затем оформить заказ (1 кнопка)
    # - затем назад (1 кнопка)
    builder.adjust(*[4] * len(items), 2, 1, 1)

    return builder.as_markup()