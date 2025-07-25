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
async def handle_clbck_category_button_pressed(callback: CallbackQuery):
    category = callback.data
    category_info = LEXICON_CATEGORIES_INFO[category]

    inline_kb = create_inline_kb(
        1,
        category_info['items'],
        *category_info['items'].keys(),
    )

    await callback.message.edit_text(
        text=category_info['description'],
        reply_markup=inline_kb.as_markup()
    )


@router.callback_query(F.data.in_(LEXICON_CATEGORIES_INFO['racetami']['items'].keys()))
async def handle_clbck_racetami_item_button_pressed(callback: CallbackQuery):
    item_info = LEXICON_ITEMS[callback.data]

    inline_kb = create_product_keyboard(
        price=item_info["price"],
        back_category='racetami'
    )

    await callback.message.edit_text(
        text=LEXICON_CATALOG['item_info'](
            item_info["description"],
            item_info["dosage"],
            item_info["quantity"],
            item_info["price"]),
        reply_markup=inline_kb
    )


@router.callback_query(F.data.in_(LEXICON_CATEGORIES_INFO['holinergetiki']['items'].keys()))
async def handle_clbck_holinergetiki_item_button_pressed(callback: CallbackQuery):
    item_info = LEXICON_ITEMS[callback.data]

    inline_kb = create_product_keyboard(
        price=item_info["price"],
        back_category='holinergetiki'
    )

    await callback.message.edit_text(
        text=LEXICON_CATALOG['item_info'](
            item_info["description"],
            item_info["dosage"],
            item_info["quantity"],
            item_info["price"]),
        reply_markup=inline_kb
    )


@router.callback_query(F.data.in_(LEXICON_CATEGORIES_INFO['stimulators']['items'].keys()))
async def handle_clbck_stimulators_item_button_pressed(callback: CallbackQuery):
    item_info = LEXICON_ITEMS[callback.data]

    inline_kb = create_product_keyboard(
        price=item_info["price"],
        back_category='stimulators'
    )

    await callback.message.edit_text(
        text=LEXICON_CATALOG['item_info'](
            item_info["description"],
            item_info["dosage"],
            item_info["quantity"],
            item_info["price"]),
        reply_markup=inline_kb
    )


@router.callback_query(F.data.in_(LEXICON_CATEGORIES_INFO['neiroprotectors']['items'].keys()))
async def handle_clbck_neiroprotectors_item_button_pressed(callback: CallbackQuery):
    item_info = LEXICON_ITEMS[callback.data]

    inline_kb = create_product_keyboard(
        price=item_info["price"],
        back_category='neiroprotectors'
    )

    await callback.message.edit_text(
        text=LEXICON_CATALOG['item_info'](
            item_info["description"],
            item_info["dosage"],
            item_info["quantity"],
            item_info["price"]),
        reply_markup=inline_kb
    )


@router.callback_query(F.data.in_(LEXICON_CATEGORIES_INFO['adaptogeni']['items'].keys()))
async def handle_clbck_adaptogeni_item_button_pressed(callback: CallbackQuery):
    item_info = LEXICON_ITEMS[callback.data]

    inline_kb = create_product_keyboard(
        price=item_info["price"],
        back_category='adaptogeni'
    )

    await callback.message.edit_text(
        text=LEXICON_CATALOG['item_info'](
            item_info["description"],
            item_info["dosage"],
            item_info["quantity"],
            item_info["price"]),
        reply_markup=inline_kb
    )


@router.callback_query(F.data.in_(LEXICON_CATEGORIES_INFO['antidepressanti']['items'].keys()))
async def handle_clbck_antidepressanti_item_button_pressed(callback: CallbackQuery):
    item_info = LEXICON_ITEMS[callback.data]
    logger.info(f'!!! {item_info}')
    inline_kb = create_product_keyboard(
        price=item_info["price"],
        back_category='antidepressanti',
    )

    await callback.message.edit_text(
        text=LEXICON_CATALOG['item_info'](
            item_info["description"],
            item_info["dosage"],
            item_info["quantity"],
            item_info["price"]),
        reply_markup=inline_kb
    )


@router.callback_query(F.data.in_(LEXICON_CATEGORIES_INFO['metabolicheskie']['items'].keys()))
async def handle_clbck_metabolicheskie_item_button_pressed(callback: CallbackQuery):
    user_id = callback.from_user.id
    item_info = LEXICON_ITEMS[callback.data]
    item_id = item_info['item_id']
    if in_cart := user_db[user_id].cart.has_item(item_id):
        quantity = user_db[user_id].cart.get_item(item_id).quantity
    else:
        quantity = 1
    cart_items_count = user_db[user_id].cart.total_uniq_items()
    inline_kb = create_product_keyboard(
        quantity=quantity,
        price=item_info["price"],
        back_category=LEXICON_CATEGORIES_INFO['metabolicheskie']['category_name'],
        item_id=item_info['item_id'],
        in_cart=in_cart,
        cart_items_count=cart_items_count
    )

    await callback.message.edit_text(
        text=LEXICON_CATALOG['item_info'](
            item_info["description"],
            item_info["dosage"],
            item_info["quantity"],
            item_info["price"]),
        reply_markup=inline_kb
    )


@router.callback_query(F.data.in_(["increase_quantity", "decrease_quantity"]))
async def handle_quantity_buttons_pressed(callback: CallbackQuery):
    user_id = callback.from_user.id
    keyboard = callback.message.reply_markup.inline_keyboard
    item_id = int(keyboard[0][1].callback_data)
    if in_cart := user_db[user_id].cart.has_item(item_id):
        quantity = user_db[user_id].cart.get_item(item_id).quantity
        if callback.data == "increase_quantity":
            new_quantity = quantity + 1
        else:
            new_quantity = max(1, quantity - 1)
        user_db[user_id].cart.get_item(item_id).quantity = new_quantity
    else:
        quantity_btn = keyboard[0][1]
        match = re.search(r'(\d+)\s*шт\.\s×\s(\d+)₽', quantity_btn.text)
        quantity = int(match.group(1))
        if callback.data == "increase_quantity":
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
        cart_items_count=cart_items_count
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
        cart_items_count=cart_items_count
    )

    await callback.message.edit_reply_markup(reply_markup=new_keyboard)
    await callback.answer("Товар добавлен в корзину")


# Хэндлер для удаления из корзины
@router.callback_query(F.data == "remove_from_cart")
async def handle_remove_from_cart(callback: CallbackQuery):
    # Здесь должна быть логика удаления из корзины

    # Получаем текущие данные из сообщения
    keyboard = callback.message.reply_markup.inline_keyboard
    quantity_text = keyboard[0][1].text
    back_button_data = keyboard[3][0].callback_data
    back_category = back_button_data.split(":")[1] if "back_to:" in back_button_data else 'racetami'

    # Парсим количество и цену
    match = re.search(r'(\d+)\s*шт\.\s×\s(\d+)₽', quantity_text)
    if not match:
        await callback.answer("Ошибка обработки количества")
        return

    quantity = int(match.group(1))
    price_per_item = int(match.group(2))

    # Здесь должна быть логика удаления товара из корзины
    # user_db[callback.from_user.id].cart.remove_item(...)

    # После удаления получаем обновленное количество товаров в корзине
    cart_items_count = 0  # Здесь должно быть user_db[callback.from_user.id].cart.total_uniq_items()

    # Обновляем клавиатуру (теперь товара нет в корзине)
    new_keyboard = create_product_keyboard(
        quantity=quantity,
        price=price_per_item,
        back_category=back_category,
        in_cart=False,
        cart_items_count=cart_items_count
    )

    await callback.message.edit_reply_markup(reply_markup=new_keyboard)
    await callback.answer("Товар удалён из корзины")


# Хэндлер для просмотра корзины
@router.callback_query(F.data == "view_cart")
async def handle_view_cart(callback: CallbackQuery):
    # Здесь должна быть логика отображения корзины
    await callback.answer("Переход в корзину")

