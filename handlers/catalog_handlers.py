import logging
import re

from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.utils.keyboard import InlineKeyboardBuilder

from database.database import user_db, CartItem
from keyboards.inline_kb import create_inline_kb
from keyboards.product_card_kb import create_product_keyboard
from lexicon.lexicon_catalog import LEXICON_CATEGORIES_INFO, LEXICON_ITEMS, LEXICON_CATALOG

router = Router()

logger = logging.getLogger(__name__)


def debug_message(msg: Message | CallbackQuery):
    logger.info(f'!!! {msg.model_dump_json(exclude_none=True, indent=2)}')


@router.callback_query(F.data.in_(LEXICON_CATEGORIES_INFO.keys()))
async def handle_category_button_pressed(callback: CallbackQuery):
    user_id = callback.from_user.id
    category = callback.data
    category_info = LEXICON_CATEGORIES_INFO[category]
    logger.info(f'Пользователь {user_id} перешел в категорию товара {category_info}')
    inline_kb = create_inline_kb(
        1,
        category_info['items'],
        *category_info['items'].keys(),
    )
    await callback.message.delete()
    await callback.message.answer(
        text=category_info['description'],
        reply_markup=inline_kb.as_markup()
    )


@router.callback_query(F.data.in_(LEXICON_ITEMS.keys()))
async def handle_item_pressed(callback: CallbackQuery):
    user_id = callback.from_user.id
    item_info = LEXICON_ITEMS[callback.data]
    item_id = item_info['item_id']
    category = item_info['category_name']
    logger.info(f'Пользователь {user_id} выбрал товар {item_info}')
    cart = user_db[user_id].cart
    item_in_cart = cart.has_item(item_id)
    quantity = cart.get_item(item_id).quantity if item_in_cart else 1
    inline_kb = create_product_keyboard(
        quantity=quantity,
        price=item_info["price"],
        back_category=category,
        item_id=item_id,
        in_cart=item_in_cart,
        cart_items_count=cart.total_uniq_items(),
        url=item_info['more_url']
    )
    await callback.message.delete()
    await callback.message.answer_photo(
        photo=item_info['image_url'],
        caption=LEXICON_CATALOG['item_info'](
            item_info["description"],
            item_info["dosage"],
            item_info["quantity"],
            item_info["price"]),
        reply_markup=inline_kb

    )


@router.callback_query(F.data.in_(["plus_quantity", "minus_quantity"]))
async def handle_quantity_buttons_pressed(callback: CallbackQuery):
    user_id = callback.from_user.id
    keyboard = callback.message.reply_markup.inline_keyboard
    item_id = int(keyboard[0][1].callback_data)
    if in_cart := user_db[user_id].cart.has_item(item_id):
        quantity = user_db[user_id].cart.get_item(item_id).quantity
        if callback.data == "plus_quantity":
            new_quantity = quantity + 1
        else:
            new_quantity = max(1, quantity - 1)
        user_db[user_id].cart.get_item(item_id).quantity = new_quantity
    else:
        quantity_btn = keyboard[0][1]
        match = re.search(r'(\d+)\s*шт\.\s×\s(\d+)₽', quantity_btn.text)
        quantity = int(match.group(1))
        if callback.data == "plus_quantity":
            new_quantity = quantity + 1
        else:
            new_quantity = max(1, quantity - 1)
    item_info = next((item for item in LEXICON_ITEMS.values() if item["item_id"] == item_id), None)
    back_btn = keyboard[3][0].callback_data
    price_per_item = item_info['price']
    cart_items_count = user_db[user_id].cart.total_uniq_items()

    inline_kb = create_product_keyboard(
        quantity=new_quantity,
        price=price_per_item,
        back_category=back_btn,
        item_id=item_id,
        in_cart=in_cart,
        cart_items_count=cart_items_count,
        url=item_info['more_url']
    )

    await callback.message.edit_reply_markup(reply_markup=inline_kb)
    await callback.answer()


# Хэндлер для добавления в корзину
@router.callback_query(F.data == "add_to_cart")
async def handle_add_to_cart(callback: CallbackQuery):
    user_id = callback.from_user.id
    keyboard = callback.message.reply_markup.inline_keyboard
    item_id = int(keyboard[0][1].callback_data)
    item_info = next((item for item in LEXICON_ITEMS.values() if item["item_id"] == item_id), None)
    quantity_btn = keyboard[0][1]
    match = re.search(r'(\d+)\s*шт\.\s×\s(\d+)₽', quantity_btn.text)
    quantity = int(match.group(1))
    item = CartItem(
        item_id=item_id,
        name=item_info['name'],
        price_per_unit=item_info['price'],
        quantity=quantity
    )
    user_db[user_id].cart.add_item(item)
    in_cart = user_db[user_id].cart.has_item(item_id)
    back_btn = keyboard[3][0].callback_data
    price_per_item = item_info['price']
    cart_items_count = user_db[user_id].cart.total_uniq_items()

    new_keyboard = create_product_keyboard(
        quantity=quantity,
        price=price_per_item,
        back_category=back_btn,
        item_id=item_id,
        in_cart=in_cart,
        cart_items_count=cart_items_count,
        url=item_info['more_url']
    )
    await callback.message.edit_reply_markup(reply_markup=new_keyboard)
    await callback.answer("Товар добавлен в корзину")


# Хэндлер для удаления из корзины
@router.callback_query(F.data == "remove_from_cart")
async def handle_remove_from_cart(callback: CallbackQuery):
    user_id = callback.from_user.id
    keyboard = callback.message.reply_markup.inline_keyboard
    item_id = int(keyboard[0][1].callback_data)
    item_info = next((item for item in LEXICON_ITEMS.values() if item["item_id"] == item_id), None)
    quantity_btn = keyboard[0][1]
    match = re.search(r'(\d+)\s*шт\.\s×\s(\d+)₽', quantity_btn.text)
    quantity = int(match.group(1))

    user_db[user_id].cart.remove_item(item_id, quantity)
    in_cart = user_db[user_id].cart.has_item(item_id)
    back_btn = keyboard[3][0].callback_data
    price_per_item = item_info['price']
    cart_items_count = user_db[user_id].cart.total_uniq_items()

    new_keyboard = create_product_keyboard(
        quantity=1,
        price=price_per_item,
        back_category=back_btn,
        item_id=item_id,
        in_cart=in_cart,
        cart_items_count=cart_items_count,
        url=item_info['more_url']
    )
    await callback.message.edit_reply_markup(reply_markup=new_keyboard)
    await callback.answer("Товар удален из корзины")
