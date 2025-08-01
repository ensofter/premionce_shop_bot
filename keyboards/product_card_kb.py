from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


def create_product_keyboard(
        quantity: int = 1,
        price: int = 1,
        back_category: str = 'racetami',
        item_id: int = 0,
        in_cart: bool = False,
        cart_items_count: int = 0,
        url: str = ''
) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    # 1. Строка с кнопками количества
    builder.button(text="➖", callback_data="minus_quantity")
    builder.button(text=f"{quantity} шт. × {price}₽ = {quantity * price}₽", callback_data=f"{item_id}")
    builder.button(text="➕", callback_data="plus_quantity")

    # 2. Строка с кнопками корзины
    if in_cart:
        # Товар в корзине: кнопки "Убрать из корзины" и "Корзина"
        builder.button(text="❌ Убрать из корзины", callback_data="remove_from_cart")
        builder.button(text=f"🛒 Корзина ({cart_items_count})", callback_data="back_to_cart")
    else:
        if cart_items_count > 0:
            # Товар не в корзине, но корзина не пуста: кнопки "Добавить в корзину" и "Корзина"
            builder.button(text="🛍️ Добавить в корзину", callback_data="add_to_cart")
            builder.button(text=f"🛒 Корзина ({cart_items_count})", callback_data="back_to_cart")
        else:
            # Товар не в корзине, корзина пуста: только кнопка "Добавить в корзину"
            builder.button(text="🛍️ Добавить в корзину", callback_data="add_to_cart")

    # 3. Кнопка подробного описания (всегда отдельная строка)
    builder.button(text="📝 Подробное описание", url=url)

    # 4. Кнопка назад (всегда отдельная строка)
    builder.button(text="🔙 Назад", callback_data=f"{back_category}")

    # Настройка расположения кнопок
    if in_cart or cart_items_count > 0:
        builder.adjust(3, 2, 1, 1)  # 3 кнопки (количество), 2 кнопки (корзина), 1 (описогумен, 1 (назад)
    else:
        builder.adjust(3, 1, 1, 1)  # 3 кнопки (количество), 1 кнопка (добавить в корзину), 1 (описание), 1 (назад)

    return builder.as_markup()
