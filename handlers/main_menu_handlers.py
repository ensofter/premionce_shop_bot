import logging

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton

from database.database import user_db
from keyboards.cart_kb import create_cart_kb
from keyboards.inline_kb import create_inline_kb
from lexicon.lexicon_cart import LEXICON_CART
from lexicon.lexicon_common import LEXICON_COMMON
from lexicon.lexicon_profile import LEXICON_PROFILE
from lexicon.lexicon_referral import LEXICON_REFERRAL
from lexicon.lexicon_main_menu import LEXICON_MM
from lexicon.lexicon_about import LEXICON_ABOUT
from lexicon.lexicon_catalog import LEXICON_CATALOG_CATEGORIES, LEXICON_CATALOG

logger = logging.getLogger()

router = Router()


async def handle_empty_cart(message_or_callback: Message | CallbackQuery):
    """
    Данная функция нужна, для того чтобы избавиться от повторяющегося кода
    :param message_or_callback:
    :return:
    """
    inline_kb = create_inline_kb(
        1,
        LEXICON_CART,
        'back_to_catalog'
    )
    text = LEXICON_CART['cart_is_empty']
    if isinstance(message_or_callback, CallbackQuery):
        await message_or_callback.message.edit_text(
            text=text,
            reply_markup=inline_kb.as_markup()
        )
    else:
        await message_or_callback.answer(
            text=text,
            reply_markup=inline_kb.as_markup()
        )


@router.message(F.text == LEXICON_MM['cart'])
@router.callback_query(F.data == 'back_to_cart')
async def handle_cart(message_or_callback: Message | CallbackQuery):
    user_id = message_or_callback.from_user.id
    if user_id in user_db:
        if not user_db[user_id].cart.total_uniq_items():
            await handle_empty_cart(message_or_callback)
        else:
            items_text = [
                f"{i}. {item.name} <code>{item.quantity}шт. × {item.price_per_unit}₽ = {item.quantity * item.price_per_unit}₽</code>"
                for i, item in enumerate(user_db[user_id].cart.items.values(), start=1)
            ]
            text = (
                    f"👾 В вашей корзине {len(items_text)} товаров\n\n"
                    + "\n".join(items_text)
                    + f"\n\n{len(items_text)+1}. Доставка почтой России первый класс <code>800₽</code>"
                    + f"\n\n<b>Общая стоимость:</b> <code>{sum(i.price_per_unit * i.quantity for i in user_db[user_id].cart.items.values()) + 800}₽</code>"
            )
            inline_kb = create_cart_kb(user_db[user_id].cart.items)
            if isinstance(message_or_callback, CallbackQuery):
                await message_or_callback.message.edit_text(
                    text=text,
                    reply_markup=inline_kb
                )
            else:
                await message_or_callback.answer(
                    text=text,
                    reply_markup=inline_kb
                )
    else:
        await handle_empty_cart(message_or_callback)



@router.message(F.text == LEXICON_MM['catalog'])
@router.callback_query(F.data == 'back_to_catalog')
async def handle_catalog(message_or_callback: Message | CallbackQuery):
    inline_kb = create_inline_kb(
        1,
        LEXICON_CATALOG_CATEGORIES,
        *LEXICON_CATALOG_CATEGORIES.keys()
    )
    if isinstance(message_or_callback, CallbackQuery):
        await message_or_callback.message.edit_text(
            text=LEXICON_CATALOG['welcome_text'],
            reply_markup=inline_kb.as_markup()
        )
    else:
        await message_or_callback.answer(
            text=LEXICON_CATALOG['welcome_text'],
            reply_markup=inline_kb.as_markup()
        )


@router.message(F.text == LEXICON_MM['profile'])
@router.callback_query(F.data == 'back_to_profile')
async def handle_profile(message_or_callback: Message | CallbackQuery):
    user_id = message_or_callback.from_user.id
    if user_id in user_db:
        if all([user_db[user_id].profile.fio, user_db[user_id].profile.phone, user_db[user_id].profile.address]):
            text = f'🤓 Ваш профиль\n\n<b>ФИО</b>: <i>{user_db[user_id].profile.fio}</i>\n' \
                   f'<b>Номер телефона</b>: <i>{user_db[user_id].profile.phone}</i>\n' \
                   f'<b>Адрес</b>: <i>{user_db[user_id].profile.address}</i>\n\n' \
                   f'Если вы желаете что-либо изменить, воспользуйтесь кнопками ниже'
            inline_kb = create_inline_kb(
                1,
                LEXICON_PROFILE,
                'edit_profile',
                'for_what',
            )
        else:
            text = LEXICON_PROFILE['does_not_exist']
            inline_kb = create_inline_kb(
                1,
                LEXICON_PROFILE,
                'fill_profile',
                'for_what'
            )
        if isinstance(message_or_callback, CallbackQuery):
            await message_or_callback.message.edit_text(
                text=text,
                reply_markup=inline_kb.as_markup()
            )
        else:
            await message_or_callback.answer(
                text=text,
                reply_markup=inline_kb.as_markup()
            )

# Хендлер обрабатывает реплай сообщение referral или inline кнопку НАЗАД back_to_referral
@router.message(F.text == LEXICON_MM['referral'])
@router.callback_query(F.data == 'back_to_referral')
async def handle_referral(message_or_callback: Message | CallbackQuery):
    user_id = message_or_callback.from_user.id
    reply_kb = create_inline_kb(
        1,
        LEXICON_REFERRAL,
        'referral_url',
        'referral_what_is_it'
    )
    if user_id in user_db:
        text = '🫂 Реферальная программа\n\n' \
               f'Ваших рефералов: {user_db[user_id].referral.referral_count}\n' \
               f'Общий заработок: {user_db[user_id].referral.referral_income} ₽\n' \
               f'Текущий ваш баланс: {user_db[user_id].referral.balance} ₽\n\n' \
               'Рекламируй PREMIONCE shop среди своих знакомых и зарабатывай ₽ с их покупок.'
    else:
        text = 'Вы пока не участвуете в реферальной программе\n\n' \
               f'Ваших рефералов: 0\n' \
               f'Общий заработок: 0 ₽\n' \
               f'Текущий ваш баланс: 0 ₽\n\n' \
               'Рекламируй PREMIONCE shop среди своих знакомых и зарабатывай ₽ с их покупок.'

    if isinstance(message_or_callback, Message):
        await message_or_callback.answer(
            text=text,
            reply_markup=reply_kb.as_markup()
        )
    else:
        await message_or_callback.message.edit_text(
            text=text,
            reply_markup=reply_kb.as_markup()
        )


# Хендлер обрабатывает реплай команду about и нажатие инлайн кнопок НЗАД back_to_about
@router.message(F.text == LEXICON_MM['about'])
@router.callback_query(F.data == 'back_to_about')
async def handle_about(message_or_callback: Message | CallbackQuery):
    user_id = message_or_callback.from_user.id
    if user_id in user_db:
        inline_kb = create_inline_kb(
            1,
            LEXICON_ABOUT,
            'faq',
            'offer'
        )
        inline_kb.row(InlineKeyboardButton(text='‍💻 Менеджер', url="tg://user?id=82429730"))
        text = LEXICON_ABOUT['🍥 О нас']
        logger.info(f'Пользователь {user_id} Запросил пункт меню О нас')
        if isinstance(message_or_callback, CallbackQuery):
            await message_or_callback.message.edit_text(
                text=text,
                reply_markup=inline_kb.as_markup()
            )
        else:
            await message_or_callback.answer(
                text=text,
                reply_markup=inline_kb.as_markup()
            )
    else:
        if isinstance(message_or_callback, CallbackQuery):
            await message_or_callback.message.edit_text(
                text=LEXICON_COMMON['user_not_exist']
            )
        else:
            await message_or_callback.answer(
                text=LEXICON_COMMON['user_not_exist']
            )

