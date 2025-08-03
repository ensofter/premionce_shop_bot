from logging import getLogger

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery

from database.database import user_db
from handlers.main_menu_handlers import handle_empty_cart
from keyboards.cart_kb import create_cart_kb
from keyboards.inline_kb import create_inline_kb
from lexicon.lexicon_profile import LEXICON_PROFILE

router = Router()
logger = getLogger(__name__)


def debug_message(msg: Message | CallbackQuery):
    logger.info(f'!!! {msg.model_dump_json(exclude_none=True, indent=2)}')


# Хэндлер для уменьшения кол-ва товара в корзине
@router.callback_query(F.data.startswith('decrease_'))
async def handle_decrease_item_quantity_in_cart(callback: CallbackQuery):
    user_id = callback.from_user.id
    item_id = int(callback.data.split("_")[1])
    cart = user_db[user_id].cart
    item = cart.get_item(item_id)

    if not user_db[user_id].cart.has_item(item_id):
        await callback.answer("Товар не найден в корзине!", show_alert=True)
        return

    if item.quantity > 1:
        item.quantity -= 1
        logger.info(f"Пользователь {user_id} уменьшил кол-во товара {item_id} до значения {item.quantity}")
    else:
        cart.remove_item(item_id)
        logger.info(f"Пользователь {user_id} удалил товар {item_id} из корзины")

    if cart.total_uniq_items() == 0:
        await handle_empty_cart(callback)
    else:
        items_text = [
            f"{i}. {item.name} <code>{item.quantity}шт. × {item.price_per_unit}₽ = {item.quantity * item.price_per_unit}₽</code>"
            for i, item in enumerate(cart.items.values(), start=1)
        ]
        text = (
                f"👾 В вашей корзине {len(items_text)} товаров\n\n"
                + "\n".join(items_text)
                + f"\n\n{len(items_text) + 1}. Доставка почтой России первый класс <code>800₽</code>"
                + f"\n\n<b>Общая стоимость:</b> <code>{sum(i.price_per_unit * i.quantity for i in user_db[user_id].cart.items.values()) + 800}₽</code>"
        )
        inline_kb = create_cart_kb(
            items=cart.items
        )
        await callback.message.edit_text(
            text=text,
            reply_markup=inline_kb
        )
    await callback.answer()


# Хэндлер для увеличения кол-ва товара в корзине
@router.callback_query(F.data.startswith('increase_'))
async def handle_increase_item_quantity_in_cart(callback: CallbackQuery):
    user_id = callback.from_user.id
    item_id = int(callback.data.split("_")[1])
    cart = user_db[user_id].cart
    item = cart.get_item(item_id)

    if not user_db[user_id].cart.has_item(item_id):
        await callback.answer("Товар не найден в корзине!", show_alert=True)
        return

    if item.quantity > 9:
        await callback.answer("Максимальное кол-во товара: 10 шт.", show_alert=True)
        return

    item.quantity += 1
    logger.info(f"Пользователь {user_id} увеличил кол-во товара {item_id} до значения {item.quantity}")

    items_text = [
        f"{i}. {item.name} <code>{item.quantity}шт. × {item.price_per_unit}₽ = {item.quantity * item.price_per_unit}₽</code>"
        for i, item in enumerate(cart.items.values(), start=1)
    ]
    text = (
            f"👾 В вашей корзине {len(items_text)} товаров\n\n"
            + "\n".join(items_text)
            + f"\n\n{len(items_text) + 1}. Доставка почтой России первый класс <code>800₽</code>"
            + f"\n\n<b>Общая стоимость:</b> <code>{sum(i.price_per_unit * i.quantity for i in user_db[user_id].cart.items.values()) + 800}₽</code>"
    )

    inline_kb = create_cart_kb(
        items=cart.items
    )
    await callback.message.edit_text(
        text=text,
        reply_markup=inline_kb
    )
    await callback.answer()


@router.callback_query(F.data == 'clear_cart')
async def handle_clear_cart_button_pressed(callback: CallbackQuery):
    user_id = callback.from_user.id
    cart = user_db[user_id].cart

    cart.items.clear()
    logger.info(f"Пользователь {user_id} очистил корзину")

    await handle_empty_cart(callback)


@router.callback_query(F.data == 'buy')
async def handle_buy_cart_button_pressed(callback: CallbackQuery):
    user_id = callback.from_user.id
    cart = user_db[user_id].cart
    profile = user_db[user_id].profile

    if user_id in user_db:
        if all([profile.fio, profile.phone, profile.address]):
            items_text = [
                f"{i}. {item.name} <code>{item.quantity}шт. × {item.price_per_unit}₽ = {item.quantity * item.price_per_unit}₽</code>"
                for i, item in enumerate(cart.items.values(), start=1)
            ]
            text = (
                    f"👾 В вашей корзине {len(items_text)} товаров\n\n"
                    + "\n".join(items_text)
                    + f"\n\n{len(items_text) + 1}. Доставка почтой России первый класс <code>800₽</code>"
                    + f"\n\n<b>Общая стоимость:</b> <code>{sum(i.price_per_unit * i.quantity for i in user_db[user_id].cart.items.values()) + 800}₽</code>"
            )
            await callback.message.edit_text(
                text=text,
            )
        else:
            text = LEXICON_PROFILE['does_not_exist']
            inline_kb = create_inline_kb(
                1,
                LEXICON_PROFILE,
                'fill_profile',
                'for_what'
            )
            await callback.message.edit_text(
                text=text,
                reply_markup=inline_kb.as_markup()
            )

