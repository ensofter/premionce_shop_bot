from copy import deepcopy

from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from database.database import user_db, user_dict_template
from keyboards.inline_kb import create_inline_kb
from keyboards.main_menu_kb import create_main_menu_reply_kb
from keyboards.pagination_kb import create_pagination_keyboard
from lexicon.lexicon_cmd import LEXICON_CMD
from lexicon.lexicon_faq import LEXICON_FAQ
from lexicon.lexicon_inline_kb import LEXICON_INLINE_KB
from lexicon.lexicon_main_menu import LEXICON_MM
from lexicon.lexicon_common import LEXICON_COMMON
from lexicon.lexicon_referral import LEXICON_REFERRAL

router = Router()


@router.message(CommandStart())
async def handle_cmd_start(message: Message):
    user_id = message.from_user.id
    if user_id not in user_db:
        user_db[user_id] = deepcopy(user_dict_template)

    await message.answer_photo(
        photo=LEXICON_CMD['welcome_photo_id'],
        caption=LEXICON_CMD['/start'],
        reply_markup=create_main_menu_reply_kb(
            3, 'catalog', 'promotions', 'cart', 'orders', 'profile', 'referral', 'about'
        )
    )


@router.message(F.text == '🩷 Реферальная программа')
@router.callback_query(F.data == 'back_to_referral')
async def handle_referral(message_or_callback: Message | CallbackQuery):
    user_id = message_or_callback.from_user.id

    reply_kb = create_inline_kb(
        1,
        LEXICON_INLINE_KB,
        'referral_url',
        'referral_what_is_it'
    )

    text = '🫂 Реферальная программа\n\n' \
           f'Ваших рефералов: {user_db[user_id]["referral"]["total_referral"]}\n' \
           f'Общий заработок: {user_db[user_id]["referral"]["total_income"]} ₽\n' \
           f'Текущий ваш баланс: {user_db[user_id]["referral"]["balance"]} ₽\n\n' \
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


@router.callback_query(F.data == 'referral_url')
async def handle_clbck_button_referral_url_pressed(callback: CallbackQuery):
    kb_builder = InlineKeyboardBuilder(
        [
            [
                InlineKeyboardButton(
                    text=LEXICON_INLINE_KB['send_referral'],
                    switch_inline_query='https://t.me/Premioncebot?start=ref_12345678'
                )
            ],
            [
                InlineKeyboardButton(text=LEXICON_COMMON['back'], callback_data='back_to_referral')
            ]
        ]
    )
    await callback.message.edit_text(
        text='🧨 Ваша ссылка для приглашения: https://t.me/Premioncebot?start=ref_12345678',
        reply_markup=kb_builder.as_markup()
    )


@router.callback_query(F.data == 'referral_what_is_it')
async def handle_clbck_button_send_referral_pressed(callback: CallbackQuery):
    kb_builder = InlineKeyboardBuilder(
        [
            [
                InlineKeyboardButton(text=LEXICON_COMMON['back'], callback_data='back_to_referral')
            ]
        ]
    )
    await callback.message.edit_text(
        text=LEXICON_REFERRAL['about_referral'],
        reply_markup=kb_builder.as_markup()
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
    reply_kb.row(InlineKeyboardButton(text=LEXICON_COMMON['back'], callback_data='back_to_about'))
    await callback.message.edit_text(
        text='👨‍🏫 Выберите вопрос',
        reply_markup=reply_kb.as_markup()
    )


@router.callback_query(F.data.split(':')[0].in_([i for i in LEXICON_FAQ.keys()]))
async def handle_clbck_button_question_pressed(callback: CallbackQuery):
    questions_keys = [i for i in LEXICON_FAQ.keys()]
    current_item = callback.data
    current_index = questions_keys.index(current_item)

    show_prev = current_index - 1 >= 0
    show_next = current_index + 1 <= len(questions_keys) - 1

    reply_kb = create_pagination_keyboard(
        f'backward:{current_item}' if show_prev else None,
        f'forward:{current_item}' if show_next else None
    )
    reply_kb.row(InlineKeyboardButton(text=LEXICON_COMMON['back'], callback_data='back_to_faq'))
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
        show_prev = current_index - 1 > 0
        reply_kb = create_pagination_keyboard(
            f'backward:{prev_key}' if show_prev else None,
            f'forward:{prev_key}'
        )
        reply_kb.row(InlineKeyboardButton(text=LEXICON_COMMON['back'], callback_data='back_to_faq'))

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
        show_next = current_index + 1 < len(questions_keys) - 1
        reply_kb = create_pagination_keyboard(
            f'backward:{next_key}',
            f'forward:{next_key}' if show_next else None
        )
        reply_kb.row(InlineKeyboardButton(text=LEXICON_COMMON['back'], callback_data='back_to_faq'))

        await callback.message.edit_text(
            text=LEXICON_FAQ[next_key],
            reply_markup=reply_kb.as_markup()
        )
    await callback.answer()


@router.message(Command(commands='help'))
async def handle_cmd_help(message: Message):
    await message.answer(
        text=LEXICON_CMD['/help']
    )
