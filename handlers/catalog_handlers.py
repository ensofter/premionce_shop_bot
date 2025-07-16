import logging

from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder

from keyboards.inline_kb import create_inline_kb
from keyboards.product_card_kb import create_product_keyboard
from lexicon.lexicon_catalog import LEXICON_CATEGORIES_INFO, LEXICON_ITEMS
import re


router = Router()

logger = logging.getLogger(__name__)


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
    item = callback.data
    item_info = LEXICON_ITEMS[item]
    text = f'<b>Описание</b>: {item_info["description"]}\n\n' \
           f'<b>Дозировка</b>: {item_info["dosage"]}\n\n' \
           f'<b>Кол-во</b>: {item_info["quantity"]}\n\n' \
           f'<b>Стоимость</b>: {item_info["coast"]}\n\n'

    # quantity = 1
    # builder = InlineKeyboardBuilder()
    #
    # builder.button(text="➖", callback_data="decrease_quantity")
    # builder.button(text=f"Кол-во: {quantity} шт. {quantity * item_info['coast']}", callback_data="show_quantity")
    # builder.button(text="➕", callback_data="increase_quantity")
    #
    # builder.button(text="🛒 Добавить в корзину", callback_data="add_to_cart")
    #
    # builder.button(text="👁️‍🗨️ Подробное описание", callback_data="product_details")
    #
    # builder.button(text="🔙 Назад", callback_data="racetami")
    #
    # builder.adjust(3, 1, 1, 1)

    inline_kb = create_product_keyboard(coast=item_info["coast"])

    await callback.message.edit_text(
        text=text,
        reply_markup=inline_kb
    )

@router.callback_query(F.data.in_(LEXICON_CATEGORIES_INFO['holinergetiki']['items'].keys()))
async def handle_clbck_holinergetiki_item_button_pressed(callback: CallbackQuery):
    item = callback.data
    item_info = LEXICON_ITEMS[item]
    text = f'<b>Описание</b>: {item_info["description"]}\n\n' \
           f'<b>Дозировка</b>: {item_info["dosage"]}\n\n' \
           f'<b>Кол-во</b>: {item_info["quantity"]}\n\n' \
           f'<b>Стоимость</b>: {item_info["coast"]}\n\n'

    inline_kb = create_inline_kb(
        1,
        'minus',
        'price_by_quantity'
        'plus',
        'add_to_cart'
        'full_description',
        'back_to_racetami'
    )

    await callback.message.edit_text(
        text=text
    )

@router.callback_query(F.data.in_(LEXICON_CATEGORIES_INFO['stimulators']['items'].keys()))
async def handle_clbck_stimulators_item_button_pressed(callback: CallbackQuery):
    item = callback.data
    item_info = LEXICON_ITEMS[item]
    text = f'<b>Описание</b>: {item_info["description"]}\n\n' \
           f'<b>Дозировка</b>: {item_info["dosage"]}\n\n' \
           f'<b>Кол-во</b>: {item_info["quantity"]}\n\n' \
           f'<b>Стоимость</b>: {item_info["coast"]}\n\n'

    inline_kb = create_inline_kb(
        1,
        'minus',
        'price_by_quantity'
        'plus',
        'add_to_cart'
        'full_description',
        'back_to_racetami'
    )

    await callback.message.edit_text(
        text=text
    )

@router.callback_query(F.data.in_(LEXICON_CATEGORIES_INFO['neiroprotectors']['items'].keys()))
async def handle_clbck_neiroprotectors_item_button_pressed(callback: CallbackQuery):
    item = callback.data
    item_info = LEXICON_ITEMS[item]
    text = f'<b>Описание</b>: {item_info["description"]}\n\n' \
           f'<b>Дозировка</b>: {item_info["dosage"]}\n\n' \
           f'<b>Кол-во</b>: {item_info["quantity"]}\n\n' \
           f'<b>Стоимость</b>: {item_info["coast"]}\n\n'

    inline_kb = create_inline_kb(
        1,
        'minus',
        'price_by_quantity'
        'plus',
        'add_to_cart'
        'full_description',
        'back_to_racetami'
    )

    await callback.message.edit_text(
        text=text
    )

@router.callback_query(F.data.in_(LEXICON_CATEGORIES_INFO['adaptogeni']['items'].keys()))
async def handle_clbck_adaptogeni_item_button_pressed(callback: CallbackQuery):
    item = callback.data
    item_info = LEXICON_ITEMS[item]
    text = f'<b>Описание</b>: {item_info["description"]}\n\n' \
           f'<b>Дозировка</b>: {item_info["dosage"]}\n\n' \
           f'<b>Кол-во</b>: {item_info["quantity"]}\n\n' \
           f'<b>Стоимость</b>: {item_info["coast"]}\n\n'

    inline_kb = create_inline_kb(
        1,
        'minus',
        'price_by_quantity'
        'plus',
        'add_to_cart'
        'full_description',
        'back_to_racetami'
    )

    await callback.message.edit_text(
        text=text
    )


@router.callback_query(F.data.in_(LEXICON_CATEGORIES_INFO['antidepressanti']['items'].keys()))
async def handle_clbck_antidepressanti_item_button_pressed(callback: CallbackQuery):
    item = callback.data
    item_info = LEXICON_ITEMS[item]
    text = f'<b>Описание</b>: {item_info["description"]}\n\n' \
           f'<b>Дозировка</b>: {item_info["dosage"]}\n\n' \
           f'<b>Кол-во</b>: {item_info["quantity"]}\n\n' \
           f'<b>Стоимость</b>: {item_info["coast"]}\n\n'

    inline_kb = create_inline_kb(
        1,
        'minus',
        'price_by_quantity'
        'plus',
        'add_to_cart'
        'full_description',
        'back_to_racetami'
    )

    await callback.message.edit_text(
        text=text
    )

@router.callback_query(F.data.in_(LEXICON_CATEGORIES_INFO['metabolicheskie']['items'].keys()))
async def handle_clbck_metabolicheskie_item_button_pressed(callback: CallbackQuery):
    item = callback.data
    item_info = LEXICON_ITEMS[item]
    text = f'<b>Описание</b>: {item_info["description"]}\n\n' \
           f'<b>Дозировка</b>: {item_info["dosage"]}\n\n' \
           f'<b>Кол-во</b>: {item_info["quantity"]}\n\n' \
           f'<b>Стоимость</b>: {item_info["coast"]}\n\n'

    inline_kb = create_inline_kb(
        1,
        'minus',
        'price_by_quantity'
        'plus',
        'add_to_cart'
        'full_description',
        'back_to_racetami'
    )

    await callback.message.edit_text(
        text=text
    )


@router.callback_query(F.data.in_(["increase_quantity", "decrease_quantity"]))
async def handle_quantity_buttons_pressed(callback: CallbackQuery):
    current_text = callback.message.reply_markup.inline_keyboard[0][1].text
    logger.info(f'??? {current_text}')
    match = re.search(r'Кол-во:\s*(\d{1,2})\s*шт\.', current_text)
    current_quantity = int(match.group(1))

    if callback.data == "increase_quantity":
        new_quantity = current_quantity + 1
    elif callback.data == 'decrease_quantity':
        new_quantity = current_quantity - 1

    keyboard = create_product_keyboard(quantity=new_quantity)
    await callback.message.edit_reply_markup(reply_markup=keyboard)
    await callback.answer()
