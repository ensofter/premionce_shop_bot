import logging

from aiogram import Router, F
from aiogram.types import CallbackQuery, InlineKeyboardButton

from keyboards.inline_kb import create_inline_kb
from keyboards.pagination_kb import create_pagination_keyboard
from lexicon.lexicon_about import LEXICON_OFFER, LEXICON_ABOUT
from lexicon.lexicon_common import LEXICON_COMMON
from lexicon.lexicon_faq import LEXICON_FAQ_QUESTIONS

router = Router()

logger = logging.getLogger(__name__)


# Хэндлер обрабатывающий нажатие кнопки получения списка FAQ
@router.callback_query(F.data.in_(['faq', 'back_to_faq']))
async def handle_button_faq_pressed(callback: CallbackQuery):
    user_id = callback.from_user.id
    questions = [i for i in LEXICON_FAQ_QUESTIONS.keys()]
    inline_kb = create_inline_kb(
        1,
        LEXICON_FAQ_QUESTIONS,
        *questions
    )
    inline_kb.row(InlineKeyboardButton(text=LEXICON_COMMON['back'], callback_data='back_to_about'))
    logger.info(f'Отдаем пользователю {user_id} список часто задаваемых вопросов FAQ')
    await callback.message.edit_text(
        text='👨‍🏫 Выберите вопрос',
        reply_markup=inline_kb.as_markup()
    )


# Хэндлер обрабатывающий нажатие кнопки вопроса в списке вопросов FAQ
@router.callback_query(F.data.in_([i for i in LEXICON_FAQ_QUESTIONS.keys()]))
async def handle_button_question_pressed(callback: CallbackQuery):
    user_id = callback.from_user.id
    questions_keys = [i for i in LEXICON_FAQ_QUESTIONS.keys()]
    current_item = callback.data
    current_index = questions_keys.index(current_item)

    show_prev = current_index - 1 >= 0
    show_next = current_index + 1 <= len(questions_keys) - 1

    reply_kb = create_pagination_keyboard(
        f'backward:{current_item}' if show_prev else None,
        f'forward:{current_item}' if show_next else None
    )
    reply_kb.row(InlineKeyboardButton(text=LEXICON_COMMON['back'], callback_data='back_to_faq'))
    logger.info(f'Пользователь {user_id} выбрал вопрос {LEXICON_FAQ_QUESTIONS[callback.data]} FAQ для прочтения')
    await callback.message.edit_text(
        text=LEXICON_FAQ_QUESTIONS[callback.data],
        reply_markup=reply_kb.as_markup()
    )


# Хэндлер обрабатывающий нажатие кнопки пагинации НАЗАД в списке вопросов FAQ
@router.callback_query(F.data.split(':')[0] == 'backward')
async def handle_button_backward_pressed(callback: CallbackQuery):
    user_id = callback.from_user.id
    questions_keys = [i for i in LEXICON_FAQ_QUESTIONS.keys()]
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
        logger.info(f'Пользователь {user_id} нажал кнопку получения предыдущего вопроса FAQ')
        await callback.message.edit_text(
            text=LEXICON_FAQ_QUESTIONS[prev_key],
            reply_markup=reply_kb.as_markup()
        )
    await callback.answer()


# Хэндлер обрабатывающий нажатие кнопки пагинации ВПЕРЕД в списке вопросов FAQ
@router.callback_query(F.data.split(':')[0] == 'forward')
async def handle_button_forward_pressed(callback: CallbackQuery):
    user_id = callback.from_user.id
    questions_keys = [i for i in LEXICON_FAQ_QUESTIONS.keys()]
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
        logger.info(f'Пользователь {user_id} нажал кнопку получения следующего вопроса FAQ')
        await callback.message.edit_text(
            text=LEXICON_FAQ_QUESTIONS[next_key],
            reply_markup=reply_kb.as_markup()
        )
    await callback.answer()


# Хэндлер обрабатывающий нажатие кнопки ОФЕРТЫ
@router.callback_query(F.data == 'offer')
async def handle_button_offer_pressed(callback: CallbackQuery):
    user_id = callback.from_user.id
    text = LEXICON_OFFER['offer']
    inline_kb = create_inline_kb(
        1,
        LEXICON_ABOUT,
        'back_to_about'
    )
    logger.info(f'Пользователь {user_id} нажал кнопку получения Оферты')
    await callback.message.edit_text(
        text=text,
        reply_markup=inline_kb.as_markup()
    )
