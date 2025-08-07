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
    fill_fio = State()
    fill_phone = State()
    fill_address = State()


class FSMFillFioProfile(StatesGroup):
    fill_fio = State()


class FSMFillPhoneProfile(StatesGroup):
    fill_phone = State()


class FSMFillAddressProfile(StatesGroup):
    fill_address = State()


# Это хэндлер отработает если нажать кнопку Отмена, но только в том случае, если пользователь не в стейтмашине
@router.callback_query(F.data == 'cancel_fill_profile', StateFilter(default_state))
async def process_clbck_cancel_fill_profile_pressed(callback: CallbackQuery):
    await callback.message.edit_text(
        text='Вы не заполняете профиль. Вы вне машины состояний'
    )


# Это хэндлер отработает если нажать кнопку Отмена, но только в том случае, если пользователь в стейтмашине
@router.callback_query(F.data == 'cancel_fill_profile', ~StateFilter(default_state))
async def process_clbck_cancel_fill_profile_pressed_in_state(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(
        text='Вы отменили заполнение профиля'
    )
    await state.clear()


# Отрабатывает когда нажата кнопка Заполнить профиль
@router.callback_query(F.data.in_({'fill_profile', 'edit_profile_from_scratch'}), StateFilter(default_state))
async def handle_clbck_button_fill_profile_pressed(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(
        text=LEXICON_PROFILE['fill_profile_pressed']
    )
    await state.set_state(FSMFillProfile.fill_fio)


# Отрабатывает когда отправлено ФИО
@router.message(StateFilter(FSMFillProfile.fill_fio),
                lambda x: len(x.text.strip().split()) == 3 and all(word.isalpha() for word in x.text.strip().split()))
async def handle_fio_sent(message: Message, state: FSMContext):
    await state.update_data(fio=message.text.strip())

    reply_phone_kb = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=LEXICON_PROFILE['send_number_button'], request_contact=True)]
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )
    await message.answer(
        text=LEXICON_PROFILE['handle_fio_sent'],
        reply_markup=reply_phone_kb
    )

    await state.set_state(FSMFillProfile.fill_phone)


# Отрабатывает когда что-то не так с ФИО
@router.message(StateFilter(FSMFillProfile.fill_fio))
async def warning_not_fio(message: Message):
    await message.answer(
        text=LEXICON_PROFILE['warning_not_fio']
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
    phone = message.text.strip() if message.text else message.contact.phone_number
    await state.update_data(phone=phone)

    await message.answer(
        text=LEXICON_PROFILE['handle_phone_sent'],
        reply_markup=ReplyKeyboardRemove()
    )
    await state.set_state(FSMFillProfile.fill_address)


# Отрабатывает когда что-то с телефоном не так
@router.message(StateFilter(FSMFillProfile.fill_phone))
async def warning_not_phone(message: Message):
    await message.answer(
        text=LEXICON_PROFILE['warning_not_phone']
    )


# Отрабатывает когда отправлен адрес
@router.message(StateFilter(FSMFillProfile.fill_address), F.text)
async def handle_address_sent(message: Message, state: FSMContext):
    user_id = message.from_user.id
    await state.update_data(address=message.text.strip())

    data = await state.get_data()
    await state.clear()

    user_db[user_id].profile.fio = data['fio']
    user_db[user_id].profile.phone = data['phone']
    user_db[user_id].profile.address = data['address']

    inline_kb = create_inline_kb(
        1,
        LEXICON_PROFILE,
        'edit_profile',
        'back_to_cart',
        'for_what'
    )

    await message.answer(
        text=LEXICON_PROFILE['everything_ok'](
            fio=user_db[user_id].profile.full_name,
            phone=user_db[user_id].profile.phone,
            address=user_db[user_id].profile.address
        ),
        reply_markup=inline_kb.as_markup()
    )


# Отрабатывает когда с адресом что-то не так
@router.message(StateFilter(FSMFillProfile.fill_address))
async def warning_not_address(message: Message):
    await message.answer(
        text=LEXICON_PROFILE['warning_not_address']
    )


# Отрабатывает когда нажимают кнопку Редактировать
@router.callback_query(F.data == 'edit_profile')
async def handle_edit_profile_button_pressed(callback: CallbackQuery):
    reply_kb = create_inline_kb(
        1,
        LEXICON_PROFILE,
        'edit_fio',
        'edit_phone',
        'edit_address',
        'edit_profile_from_scratch',
        'back_to_profile'
    )
    await callback.message.edit_text(
        text=LEXICON_PROFILE['edit_profile_button_pressed'],
        reply_markup=reply_kb.as_markup()
    )


# Отрабатывает, когда нажимают кнопку редактирования ФИО
@router.callback_query(F.data == 'edit_fio', StateFilter(default_state))
async def handle_edit_fio_button_pressed(callback: CallbackQuery, state: FSMContext):
    text = LEXICON_PROFILE['fill_fio_again']
    await callback.message.edit_text(
        text=text
    )

    await state.set_state(FSMFillFioProfile.fill_fio)


# Отрабатывает, когда вводят новое ФИО
@router.message(StateFilter(FSMFillFioProfile.fill_fio),
                lambda x: len(x.text.strip().split()) == 3 and all(word.isalpha() for word in x.text.strip().split()))
async def handle_fio_edit_sent(message: Message, state: FSMContext):
    user_id = message.from_user.id
    await state.update_data(fio=message.text.strip())

    data = await state.get_data()
    await state.clear()

    user_db[user_id].profile.fio = data['fio']

    inline_kb = create_inline_kb(
        1,
        LEXICON_PROFILE,
        'edit_profile',
        'for_what'
    )

    await message.answer(
        text=LEXICON_PROFILE['everything_ok'](
            fio=user_db[user_id].profile.fio,
            phone=user_db[user_id].profile.phone,
            address=user_db[user_id].profile.address
        ),
        reply_markup=inline_kb.as_markup()
    )


# Отрабатывает, когда фильтр на введенное ФИО выше не отработал
@router.message(StateFilter(FSMFillFioProfile.fill_fio))
async def warning_not_fio_again(message: Message):
    await message.answer(
        text=LEXICON_PROFILE['warning_not_fio']
    )


# Отрабатывает, когда нажимают кнопку редактирования Номера Телефона
@router.callback_query(F.data == 'edit_phone', StateFilter(default_state))
async def handle_edit_phone_button_pressed(callback: CallbackQuery, state: FSMContext):
    text = LEXICON_PROFILE['fill_phone_again']
    reply_phone_kb = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=LEXICON_PROFILE['send_number_button'], request_contact=True)]
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )
    await callback.message.delete()

    await callback.message.answer(
        text=text,
        reply_markup=reply_phone_kb
    )
    await state.set_state(FSMFillPhoneProfile.fill_phone)


@router.message(StateFilter(FSMFillPhoneProfile.fill_phone),
                F.text | F.contact,
                lambda x: (
                        (x.text and x.text.isdigit() and len(x.text) == 11 and x.text.startswith('7'))
                        or
                        (x.contact and x.contact.phone_number)
                )
                )
async def handle_phone_edit_sent(message: Message, state: FSMContext):
    user_id = message.from_user.id
    phone = message.text.strip() if message.text else message.contact.phone_number
    await state.update_data(phone=phone)

    data = await state.get_data()
    await state.clear()

    user_db[user_id].profile.phone = data['phone']

    inline_kb = create_inline_kb(
        1,
        LEXICON_PROFILE,
        'edit_profile',
        'for_what'
    )

    await message.answer(
        text=LEXICON_PROFILE['everything_ok'](
            fio=user_db[user_id].profile.fio,
            phone=user_db[user_id].profile.phone,
            address=user_db[user_id].profile.address
        ),
        reply_markup=inline_kb.as_markup()
    )


@router.message(StateFilter(FSMFillPhoneProfile.fill_phone))
async def warning_not_phone_again(message: Message):
    await message.answer(
        text=LEXICON_PROFILE['warning_not_phone']
    )


@router.callback_query(F.data == 'edit_address', StateFilter(default_state))
async def handle_edit_address_button_pressed(callback: CallbackQuery, state: FSMContext):
    text = LEXICON_PROFILE['fill_address_again']
    await callback.message.edit_text(
        text=text
    )

    await state.set_state(FSMFillAddressProfile.fill_address)


@router.message(StateFilter(FSMFillAddressProfile.fill_address), F.text)
async def handle_address_edit_sent(message: Message, state: FSMContext):
    user_id = message.from_user.id
    address = message.text.strip()
    await state.update_data(address=address)

    data = await state.get_data()
    await state.clear()

    user_db[user_id].profile.address = data['address']

    inline_kb = create_inline_kb(
        1,
        LEXICON_PROFILE,
        'edit_profile',
        'for_what'
    )

    await message.answer(
        text=LEXICON_PROFILE['everything_ok'](
            fio=user_db[user_id].profile.fio,
            phone=user_db[user_id].profile.phone,
            address=user_db[user_id].profile.address
        ),
        reply_markup=inline_kb.as_markup()
    )


@router.message(StateFilter(FSMFillAddressProfile.fill_address))
async def warning_not_address_again(message: Message):
    await message.answer(
        text=LEXICON_PROFILE['warning_not_address']
    )


@router.callback_query(F.data == 'for_what')
async def handle_clbck_for_what_button_pressed(callback: CallbackQuery):
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