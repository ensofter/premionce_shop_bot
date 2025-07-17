import logging
import re

from aiogram import Router, F
from aiogram.types import CallbackQuery, Message

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

    inline_kb = create_product_keyboard(
        price=item_info["price"],
        back_category='antidepressanti'
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
    item_info = LEXICON_ITEMS[callback.data]

    inline_kb = create_product_keyboard(
        price=item_info["price"],
        back_category='metabolicheskie'
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
    debug_message(callback)
    quantity_and_price_in_button_text = callback.message.reply_markup.inline_keyboard[1][0].text
    product_description_text = callback.message.text
    product_category = callback.message.reply_markup.inline_keyboard[4][0].callback_data

    # re для поиска кол-во товара и его стоимости
    match_actual_quantity = re.search(r'Кол-во:\s*(\d+)\s*шт\.\s*(\d+)₽', quantity_and_price_in_button_text)
    match_product_price = re.search(r'(\d+)₽', product_description_text)

    quantity = int(match_actual_quantity.group(1))  # Актуальное кол-во товара
    price = int(match_product_price.group(1))  # Цена товара

    if callback.data == "increase_quantity":
        new_quantity = quantity + 1
        new_price = new_quantity * price
    elif callback.data == 'decrease_quantity':
        if quantity == 1:
            new_quantity = 1
            new_price = price
            await callback.answer()
        else:
            new_quantity = quantity - 1
            new_price = new_quantity * price

    keyboard = create_product_keyboard(quantity=new_quantity, price=new_price, back_category=product_category)
    await callback.message.edit_reply_markup(reply_markup=keyboard)
    await callback.answer()
