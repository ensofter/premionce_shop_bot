import logging

from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State, default_state
from aiogram.types import CallbackQuery, Message, ReplyKeyboardMarkup, KeyboardButton, \
    ReplyKeyboardRemove

from database.database import user_db
from keyboards.inline_kb import create_inline_kb
from lexicon.lexicon_profile import LEXICON_PROFILE

router = Router()

logger = logging.getLogger()


def debug_message(msg: Message):
    logger.info(f'!!! {msg.model_dump_json(exclude_none=True, indent=2)}')


class FSMFillProfile(StatesGroup):
    fill_fullname = State()
    fill_phone = State()
    fill_address = State()


class FSMProfileEdit(StatesGroup):
    editing_field = State()
    waiting_edit_choice = State()


# Отрабатывает когда нажата кнопка Заполнить профиль или пользователь решил заполнить профиль заново
@router.callback_query(F.data == 'fill_profile', StateFilter(default_state))
async def handle_button_fill_profile_pressed(callback: CallbackQuery, state: FSMContext):
    user_id = callback.from_user.id
    logger.info(f'Пользователь {user_id} приступил к заполнению профиля')
    await callback.message.edit_text(
        text=LEXICON_PROFILE['fill_profile_pressed']
    )
    await state.set_state(FSMFillProfile.fill_fullname)


# Отрабатывает когда отправлено ФИО
@router.message(StateFilter(FSMFillProfile.fill_fullname),
                lambda x: len(x.text.strip().split()) == 3 and all(word.isalpha() for word in x.text.strip().split()))
async def handle_fullname_sent(message: Message, state: FSMContext):
    user_id = message.from_user.id
    logger.info(f'Пользователь {user_id} ввел свое ФИО {message.text}')
    await state.update_data(fullname=message.text.strip())
    reply_phone_kb = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=LEXICON_PROFILE['send_number_button'], request_contact=True)]
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )
    await message.answer(
        text=LEXICON_PROFILE['handle_fullname_sent'],
        reply_markup=reply_phone_kb
    )
    await state.set_state(FSMFillProfile.fill_phone)


# Отрабатывает когда что-то не так с ФИО
@router.message(StateFilter(FSMFillProfile.fill_fullname))
async def warning_not_fullname(message: Message):
    user_id = message.from_user.id
    logger.info(f"Пользователь {user_id} ввел некорректное значение вместо ФИО {message.text}")
    await message.answer(
        text=LEXICON_PROFILE['warning_not_fullname']
    )


# Отрабатывает когда отправлен телефон через кнопку или через текст
@router.message(
    StateFilter(FSMFillProfile.fill_phone),
    F.text | F.contact,
    lambda x: (
            (x.text and x.text.isdigit() and len(x.text) == 11 and x.text.startswith('7'))
            or
            (x.contact and x.contact.phone_number)
    )
)
async def handle_phone_sent(message: Message, state: FSMContext):
    user_id = message.from_user.id
    phone = message.text.strip() if message.text else message.contact.phone_number
    logger.info(f'Пользователь {user_id} ввел свой номер телефона {phone}')
    await state.update_data(phone=phone)
    await message.answer(
        text=LEXICON_PROFILE['handle_phone_sent'],
        reply_markup=ReplyKeyboardRemove()
    )
    await state.set_state(FSMFillProfile.fill_address)


# Отрабатывает когда что-то с телефоном не так
@router.message(StateFilter(FSMFillProfile.fill_phone))
async def warning_not_phone(message: Message):
    user_id = message.from_user.id
    logger.info(f"Пользователь {user_id} ввел некорректное значение вместо телефона {message.text}")
    await message.answer(
        text=LEXICON_PROFILE['warning_not_phone']
    )


# Отрабатывает когда отправлен адрес
@router.message(StateFilter(FSMFillProfile.fill_address), F.text)
async def handle_address_sent(message: Message, state: FSMContext):
    user_id = message.from_user.id
    logger.info(f'Пользователь {user_id} ввел свой адрес {message.text}')
    await state.update_data(address=message.text.strip())
    data = await state.get_data()
    await state.clear()

    user_db[user_id].profile.fullname = data['fullname']
    user_db[user_id].profile.phone = data['phone']
    user_db[user_id].profile.address = data['address']

    logger.info(f'Сохраняем в БД введенные пользователем значения\n\n'
                f'{user_db[user_id].profile.fullname}'
                f'{user_db[user_id].profile.phone}'
                f'{user_db[user_id].profile.address}')

    inline_kb = create_inline_kb(
        1,
        LEXICON_PROFILE,
        'edit_profile',
        'back_to_cart',
        'for_what',
        'back_to_main_menu'
    )
    await message.answer(
        text=LEXICON_PROFILE['everything_ok'](
            fullname=user_db[user_id].profile.fullname,
            phone=user_db[user_id].profile.phone,
            address=user_db[user_id].profile.address
        ),
        reply_markup=inline_kb.as_markup()
    )


# Отрабатывает когда с адресом что-то не так
@router.message(StateFilter(FSMFillProfile.fill_address))
async def warning_not_address(message: Message):
    user_id = message.from_user.id
    logger.info(f"Пользователь {user_id} ввел некорректное значение вместо адреса {message.text}")
    await message.answer(
        text=LEXICON_PROFILE['warning_not_address']
    )


@router.callback_query(F.data == 'edit_profile', StateFilter(default_state))
async def handle_edit_profile_button_pressed(callback: CallbackQuery, state: FSMContext):
    user_id = callback.from_user.id
    inline_kb = create_inline_kb(
        1,
        LEXICON_PROFILE,
        'edit_fullname',
        'edit_phone',
        'edit_address',
        'edit_profile_from_scratch',
        'back_to_profile'
    )
    await callback.message.edit_text(
        text=LEXICON_PROFILE['edit_profile_button_pressed'],
        reply_markup=inline_kb.as_markup()
    )
    logger.info(f'Пользователь {user_id} начал редактирование профиля и перешел в состояние ожидания поля')
    await state.set_state(FSMProfileEdit.waiting_edit_choice)


@router.callback_query(
    F.data.in_({'edit_fullname', 'edit_phone', 'edit_address'}),
    StateFilter(FSMProfileEdit.waiting_edit_choice)
)
async def handle_select_field_to_edit(callback: CallbackQuery, state: FSMContext):
    user_id = callback.from_user.id
    field = callback.data.split('_')[1]
    await state.update_data(editing_field=field)
    logger.info(f'Пользователь {user_id} выбрал поле {field} для редактирования')
    if field == 'phone':
        inline_kb = ReplyKeyboardMarkup(
            keyboard=[[KeyboardButton(text=LEXICON_PROFILE['send_number_button'], request_contact=True)]],
            resize_keyboard=True
        )
    else:
        inline_kb = ReplyKeyboardRemove()
    text = LEXICON_PROFILE[f'fill_{field}_again']
    await callback.message.answer(text, reply_markup=inline_kb)
    await state.set_state(FSMProfileEdit.editing_field)


@router.message(StateFilter(FSMProfileEdit.editing_field))
async def save_profile_field(message: Message, state: FSMContext):
    user_id = message.from_user.id
    data = await state.get_data()
    field = data['editing_field']
    value = ''
    if field == 'fullname':
        logger.info(f'Пользователь {user_id} редактирует поле fullname')
        if not (len(message.text.split()) == 3 and all(word.isalpha() for word in message.text.split())):
            await message.answer(LEXICON_PROFILE['warning_not_fio'])
            return
        value = message.text.strip()
    elif field == 'phone':
        logger.info(f'Пользователь {user_id} редактирует поле phone')
        phone = message.text if message.text else (message.contact.phone_number if message.contact else None)
        if not (phone and len(phone) == 11 and phone.startswith('7')):
            await message.answer(LEXICON_PROFILE['warning_not_phone'])
            return
        value = phone
    elif field == 'address':
        logger.info(f'Пользователь {user_id} редактирует поле address')
        if not message.text:
            await message.answer(LEXICON_PROFILE['warning_not_address'])
            return
        value = message.text.strip()
    logger.info(f'Пользователь {user_id} редактирует поле {field} и ввел значение {value}')
    setattr(user_db[user_id].profile, field, value)
    await state.clear()
    inline_kb = create_inline_kb(
        1,
        LEXICON_PROFILE,
        'edit_profile',
        'for_what',
        'back_to_main_menu'
    )
    text = LEXICON_PROFILE['everything_ok'](
        fullname=user_db[user_id].profile.fullname,
        phone=user_db[user_id].profile.phone,
        address=user_db[user_id].profile.address
    )
    await message.answer(
        text=text,
        reply_markup=inline_kb.as_markup()
    )


@router.callback_query(F.data == 'edit_profile_from_scratch', StateFilter(FSMProfileEdit.waiting_edit_choice))
async def handle_button_edit_profile_from_scratch_pressed(callback: CallbackQuery, state: FSMContext):
    user_id = callback.from_user.id
    logger.info(f'Пользователь {user_id} заново заполнить профиль')
    await handle_button_fill_profile_pressed(callback, state)


@router.callback_query(F.data == 'for_what')
async def handle_for_what_button_pressed(callback: CallbackQuery):
    user_id = callback.from_user.id
    logger.info(f'Пользователь {user_id} нажал кнопку Зачем эти данные')
    text = LEXICON_PROFILE['for_what_expanded']
    inline_kb = create_inline_kb(
        1,
        LEXICON_PROFILE,
        'back_to_profile'
    )
    await callback.message.edit_text(
        text=text,
        reply_markup=inline_kb.as_markup()
    )
