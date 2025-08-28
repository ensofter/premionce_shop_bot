import logging

from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton

from database.database import user_db
from handlers.profile_handlers import FSMProfileEdit
from keyboards.cart_kb import create_cart_kb
from keyboards.inline_kb import create_inline_kb
from lexicon.lexicon_cart import LEXICON_CART
from lexicon.lexicon_common import LEXICON_COMMON
from lexicon.lexicon_profile import LEXICON_PROFILE
from lexicon.lexicon_promotions import LEXICON_PROMOTIONS
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


# Хэндлер обрабатывающий реплай сообщение catalog или inline кнопку НАЗАД back_to_catalog
@router.message(F.text == LEXICON_MM['catalog'])
@router.callback_query(F.data == 'back_to_catalog')
async def handle_catalog(message_or_callback: Message | CallbackQuery):
    user_id = message_or_callback.from_user.id
    logger.info(f'Пользователь {user_id} запросил каталог товаров')
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


@router.message(F.text == LEXICON_MM['promotions'])
@router.callback_query(F.data == 'back_to_promotions')
async def handle_promotions(message_or_callback: Message | CallbackQuery):
    user_id = message_or_callback.from_user.id
    logger.info(f'Пользователь {user_id} запросил действующие акции')
    if isinstance(message_or_callback, CallbackQuery):
        await message_or_callback.message.edit_text(
            text=LEXICON_PROMOTIONS['welcome_promotion_text']
        )
    else:
        await message_or_callback.answer(
            text=LEXICON_PROMOTIONS['welcome_promotion_text']
        )


# Хэндлер обрабатывающий реплай сообщение cart или inline кнопку НАЗАД back_to_cart
@router.message(F.text == LEXICON_MM['cart'])
@router.callback_query(F.data == 'back_to_cart')
async def handle_cart(message_or_callback: Message | CallbackQuery):
    user_id = message_or_callback.from_user.id
    if user_id in user_db:
        if not user_db[user_id].cart.total_uniq_items():
            await handle_empty_cart(message_or_callback)
        else:
            items_text = [
                f"{i}. {item.name} <code>{item.quantity}шт. × {item.unit_price}₽ = {item.quantity * item.unit_price}₽</code>"
                for i, item in enumerate(user_db[user_id].cart.items.values(), start=1)
            ]
            text = (
                    f"👾 В вашей корзине {len(items_text)} товаров\n\n"
                    + "\n".join(items_text)
                    + f"\n\n{len(items_text)+1}. Доставка почтой России первый класс <code>800₽</code>"
                    + f"\n\n<b>Общая стоимость:</b> <code>{sum(i.unit_price * i.quantity for i in user_db[user_id].cart.items.values()) + 800}₽</code>"
            )
            inline_kb = create_cart_kb(user_db[user_id].cart.items)
            if isinstance(message_or_callback, CallbackQuery):
                await message_or_callback.message.delete()
                await message_or_callback.message.answer(
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


# Хэндлер обрабатывающий реплай сообщение orders или inline кнопку НАЗАД back_to_orders
@router.message(F.text == LEXICON_MM['orders'])
@router.callback_query(F.data == 'back_to_orders')
async def handle_orders(message_or_callback: Message | CallbackQuery):
    user_id = message_or_callback.from_user.id
    logger.info(f'Пользователь {user_id} зашел в меню Заказы')
    if user_id in user_db:
        if isinstance(message_or_callback, CallbackQuery):
            await message_or_callback.message.edit_text(
                text='Тут буду заказы пользователя'
            )
        else:
            await message_or_callback.answer(
                text='Тут буду заказы пользователя'
            )
    else:
        if isinstance(message_or_callback, CallbackQuery):
            await message_or_callback.message.edit_text(
                text='У пользователя нет ни одного заказа'
            )
        else:
            await message_or_callback.answer(
                text='У пользователя нет ни одного заказа'
            )


# Хэндлер обрабатывает случай, когда пользователь начал редактировать профиль, но вдруг передумал и нажал кнопку НАЗАД
@router.callback_query(F.data == 'back_to_profile', StateFilter(FSMProfileEdit.waiting_edit_choice))
async def cancel_editing_profile(callback: CallbackQuery, state: FSMContext):
    user_id = callback.from_user.id
    logger.info(f'Пользователь {user_id} отменил редактирование профиля и нажал кнопку НАЗАД')
    await state.clear()
    await handle_profile(callback)


# Хэндлер обрабатывающий реплай сообщение profile или inline кнопку НАЗАД back_to_profile
@router.message(F.text == LEXICON_MM['profile'])
@router.callback_query(F.data == 'back_to_profile')
async def handle_profile(message_or_callback: Message | CallbackQuery):
    """
    Кривой хэндлер. В начале стоит проверка на то, что есть ли пользак в базке или нет. Надо потом будет убрать!
    :param message_or_callback:
    :return:
    """
    user_id = message_or_callback.from_user.id
    if user_id in user_db:
        if user_db[user_id].profile.is_complete():
            logger.info(f'У пользователь {user_id} заполнен профиль')
            inline_kb = create_inline_kb(
                1,
                LEXICON_PROFILE,
                'edit_profile',
                'for_what',
            )
            text = LEXICON_PROFILE['exist'](
                fullname=user_db[user_id].profile.fullname,
                phone=user_db[user_id].profile.phone,
                address=user_db[user_id].profile.address
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
        else:
            logger.info(f'У пользователь {user_id} НЕ заполнен профиль')
            inline_kb = create_inline_kb(
                1,
                LEXICON_PROFILE,
                'fill_profile',
                'for_what'
            )
            text = LEXICON_PROFILE['does_not_exist']
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
        logger.info(f'Пользователя нет в БД')
        text = LEXICON_COMMON['user_not_exist']
        if isinstance(message_or_callback, CallbackQuery):
            await message_or_callback.message.edit_text(
                text=text
            )
        else:
            await message_or_callback.answer(
                text=text
            )



# Хендлер обрабатывает реплай сообщение referral или inline кнопку НАЗАД back_to_referral
@router.message(F.text == LEXICON_MM['referral'])
@router.callback_query(F.data == 'back_to_referral')
async def handle_referral(message_or_callback: Message | CallbackQuery):
    """
    Довольно кривой хендлер, так как у меня есть захардкоженные значения и проверка на то есть ли пользак в базе или
    нет, тут лишня, потому что изначально конечно у пользователя не будет никаких рефералов. Но позже может и будут.
    :param message_or_callback:
    :return:
    """
    user_id = message_or_callback.from_user.id
    inline_kb = create_inline_kb(
        1,
        LEXICON_REFERRAL,
        'referral_url',
        'referral_what_is_it'
    )
    if user_id in user_db:
        logger.info(f'У пользователь {user_id} есть рефералы')
        text = LEXICON_REFERRAL['user_has_referral'](
            referral_count=user_db[user_id].referral.referral_count,
            referral_income=user_db[user_id].referral.referral_income,
            balance=user_db[user_id].referral.balance
        )
    else:
        logger.info(f'Пользователь {user_id} не участвует в реферальной программе')
        text = LEXICON_REFERRAL['user_hasnt_referral']
    if isinstance(message_or_callback, Message):
        await message_or_callback.answer(
            text=text,
            reply_markup=inline_kb.as_markup()
        )
    else:
        await message_or_callback.message.edit_text(
            text=text,
            reply_markup=inline_kb.as_markup()
        )


# Хендлер обрабатывает реплай команду about и нажатие инлайн кнопок НЗАД back_to_about
@router.message(F.text == LEXICON_MM['about'])
@router.callback_query(F.data == 'back_to_about')
async def handle_about(message_or_callback: Message | CallbackQuery):
    user_id = message_or_callback.from_user.id
    inline_kb = create_inline_kb(
        1,
        LEXICON_ABOUT,
        'faq',
        'offer'
    )
    inline_kb.row(
        InlineKeyboardButton(text='‍💻 Менеджер', url="tg://user?id=82429730"),
        InlineKeyboardButton(text=LEXICON_COMMON['back_to_main_menu'], callback_data='back_to_main_menu'),
        width=1
    )
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
