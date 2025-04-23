from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton

from keyboards.inline_kb import create_inline_kb
from keyboards.main_menu_kb import create_main_menu_reply_kb
from keyboards.pagination_kb import create_pagination_keyboard
from lexicon.lexicon_cmd import LEXICON_CMD
from lexicon.lexicon_faq import LEXICON_FAQ
from lexicon.lexicon_inline_kb import LEXICON_INLINE_KB
from lexicon.lexicon_main_menu import LEXICON_MM
from aiogram.filters import or_f

router = Router()


@router.message(CommandStart())
async def handle_cmd_start(message: Message):
    await message.answer_photo(
        photo=LEXICON_CMD['welcome_photo_id'],
        caption=LEXICON_CMD['/start'],
        reply_markup=create_main_menu_reply_kb(
            3, 'catalog', 'promotions', 'cart', 'orders', 'profile', 'referral', 'about'
        )
    )


@router.message(F.text == '🍥 О нас')
@router.callback_query(F.data == 'back_to_about')
async def handle_about(message_or_callback: Message | CallbackQuery):
    reply_kb = create_inline_kb(
        1,
        LEXICON_INLINE_KB,
        'faq',
    )
    reply_kb.row(InlineKeyboardButton(text='‍💻 Менеджер', url="tg://user?id=82429730"))

    text = LEXICON_MM['🍥 О нас']

    if isinstance(message_or_callback, CallbackQuery):
        await message_or_callback.message.edit_text(text=text, reply_markup=reply_kb.as_markup())
    else:
        await message_or_callback.answer(text=text, reply_markup=reply_kb.as_markup())


@router.callback_query(F.data.in_(['faq', 'back_to_faq']))
async def handle_clbck_button_faq_pressed(callback: CallbackQuery):
    questions = [i for i in LEXICON_FAQ.keys()]
    reply_kb = create_inline_kb(
        1,
        LEXICON_FAQ,
        *questions
    )
    reply_kb.row(InlineKeyboardButton(text='🔙 Назад', callback_data='back_to_about'))
    await callback.message.edit_text(
        text='👨‍🏫 Выберите вопрос',
        reply_markup=reply_kb.as_markup()
    )


@router.callback_query(F.data.split(':')[0].in_([i for i in LEXICON_FAQ.keys()]))
async def handle_clbck_button_question_pressed(callback: CallbackQuery):
    current_item = callback.data
    reply_kb = create_pagination_keyboard(
        f'backward:{current_item}',
        f'forward:{current_item}'
    )
    reply_kb.row(InlineKeyboardButton(text='🔙 Назад', callback_data='back_to_faq'))
    await callback.message.edit_text(
        text=LEXICON_FAQ[callback.data],
        reply_markup=reply_kb.as_markup()
    )


@router.callback_query(F.data.split(':')[0] == 'backward')
async def handle_clbck_button_backward_pressed(callback: CallbackQuery):
    questions_keys = [i for i in LEXICON_FAQ.keys()]
    current_item = callback.data.split(':')[1]
    current_index = questions_keys.index(current_item)

    prev_key = questions_keys[current_index - 1] if current_index > 0 else None

    if prev_key:
        reply_kb = create_pagination_keyboard(
            f'backward:{prev_key}',
            f'forward:{prev_key}'
        )
        reply_kb.row(InlineKeyboardButton(text='🔙 Назад', callback_data='back_to_faq'))

        await callback.message.edit_text(
            text=LEXICON_FAQ[prev_key],
            reply_markup=reply_kb.as_markup()
        )
    await callback.answer()


@router.callback_query(F.data.split(':')[0] == 'forward')
async def handle_clbck_button_forward_pressed(callback: CallbackQuery):
    questions_keys = [i for i in LEXICON_FAQ.keys()]
    current_item = callback.data.split(':')[1]
    current_index = questions_keys.index(current_item)

    next_key = questions_keys[current_index + 1] if current_index < len(questions_keys) - 1 else None

    if next_key:
        reply_kb = create_pagination_keyboard(
            f'backward:{next_key}',
            f'forward:{next_key}'
        )
        reply_kb.row(InlineKeyboardButton(text='🔙 Назад', callback_data='back_to_faq'))

        await callback.message.edit_text(
            text=LEXICON_FAQ[next_key],
            reply_markup=reply_kb.as_markup()
        )
    await callback.answer()


# @router.callback_query(F.data == 'back_to_about')
# async def handle_clbck_button_back_to_about_pressed(callback: CallbackQuery):
#     """
#     Получается что это полный дубль функции handle_reply_button_about
#     ToDo: нужно придумать как реализовать кнопку назад
#     """
#     reply_kb = create_inline_kb(
#         1,
#         LEXICON_INLINE_KB,
#         'faq',
#     )
#     reply_kb.row(InlineKeyboardButton(text='‍💻 Менеджер', url="tg://user?id=82429730"))
#     await callback.message.edit_text(
#         text=LEXICON_MM['🍥 О нас'],
#         reply_markup=reply_kb.as_markup()
#     )


# @router.callback_query(F.data == 'back_to_faq')
# async def handle_clbck_button_back_to_faq_pressed(callback: CallbackQuery):
#     """
#     Получается что это полный дубль функции handle_clbck_button_faq_pressed
#     ToDo: нужно придумать как реализовать кнопку назад
#     """
#     reply_kb = create_inline_kb(
#         1,
#         LEXICON_FAQ,
#         first='Ваша продукция легальна?',
#         second='Вам можно доверять?',
#         third='Ваши преимущества?',
#     )
#     reply_kb.row(InlineKeyboardButton(text='🔙 Назад', callback_data='back_to_about'))
#     await callback.message.edit_text(
#         text='👨‍🏫 Выберите вопрос',
#         reply_markup=reply_kb.as_markup()
#     )


@router.message(Command(commands='help'))
async def handle_cmd_help(message: Message):
    await message.answer(
        text=LEXICON_CMD['/help']
    )
