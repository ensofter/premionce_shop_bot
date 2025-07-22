from typing import Callable

LEXICON_CART: dict[str, str | Callable] = {
    'cart_is_empty': "👾 К сожалению, ваша корзина пуста",
    'in_your_cart': lambda quantity: (
        f"👾 В вашей корзине {quantity} товаров"
    ),
    'clear_cart': "🧹 Очистить",
    'buy': "💳 Оформить заказ",
    'back_to_catalog': '💊 Каталог'
}