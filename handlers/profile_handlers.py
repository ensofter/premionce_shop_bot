import logging

from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from aiogram.fsm.state import StatesGroup, State, default_state
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder

router = Router()

logger = logging.getLogger()


def debug_message(msg: Message):
    print(msg.model_dump_json(exclude_none=True, indent=2))


class FSMFillProfile(StatesGroup):
    fill_fio = State()
    fill_phone = State()
    fill_address = State()


@router.callback_query(F.data == 'cancel_fill_profile', StateFilter(default_state))
async def process_clbck_cancel_fill_profile_pressed(callback: CallbackQuery):
    await callback.message.edit_text(
        text='Вы не заполняете профиль. Вы вне машины состояний'
    )


@router.callback_query(F.data == 'cancel_fill_profile', ~StateFilter(default_state))
async def process_clbck_cancel_fill_profile_pressed_in_state(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(
        text='Вы отменили заполнение профиля'
    )
    await state.clear()


@router.callback_query(F.data == 'fill_profile', StateFilter(default_state))
async def handle_clbck_button_fill_profile_pressed(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(
        text='📚 Введите ваше ФИО\n\n'
             '<i>Эти данные в будущем можно будет изменить</i>'
    )
    await state.set_state(FSMFillProfile.fill_fio)


@router.message(StateFilter(FSMFillProfile.fill_fio),
                lambda x: len(x.text.strip().split()) == 3 and all(word.isalpha() for word in x.text.strip().split()))
async def handle_fio_sent(message: Message, state: FSMContext):
    await state.update_data(fio=message.text.strip())

    reply_phone_kb = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Отправить номер 📞", request_contact=True)]
        ],
        resize_keyboard=True
    )
    await message.answer(
        text='Спасибо!\n\nТеперь введите ваш номер телефона в формате <b>7xxxxxxxxxx</b> '
             'или отправьте его нажатием на кнопку ниже',
        reply_markup=reply_phone_kb
    )

    await state.set_state(FSMFillProfile.fill_phone)


@router.message(StateFilter(FSMFillProfile.fill_fio))
async def warning_not_fio(message: Message):
    await message.answer(
        text='❌ То, что вы отправили не похоже на ФИО\n\n'
             'Пожалуйста, введите ваше ФИО\n\n'
    )


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
    logger.info(f'!!! {debug_message(message)}')
    phone = message.text if message.text else message.contact.phone_number
    await state.update_data(phone=phone)


@router.message(StateFilter(FSMFillProfile.fill_phone))
async def warning_not_phone(message: Message):
    await message.answer(
        text='❌ То, что вы отправили не похоже на номер телефона\n\n'
             'Пожалуйста, введите ваш номер телефона в формате\n\n'
             '<b>7xxxxxxxxxx</b>\n\n'
             'начинает с 7 и содержит 11 цифр'
    )








