from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


def create_product_keyboard(quantity: int = 1, show_minus: bool = False, coast: int = 1):
    builder = InlineKeyboardBuilder()

    builder.button(text="➖", callback_data="decrease_quantity")
    builder.button(text=f"Кол-во: {quantity} шт. {quantity * coast}", callback_data="show_quantity")
    builder.button(text="➕", callback_data="increase_quantity")

    builder.button(text="🛒 Добавить в корзину", callback_data="add_to_cart")

    builder.button(text="👁️‍🗨️ Подробное описание", callback_data="product_details")

    builder.button(text="🔙 Назад", callback_data="racetami")

    builder.adjust(3, 1, 1, 1)

    return builder.as_markup()