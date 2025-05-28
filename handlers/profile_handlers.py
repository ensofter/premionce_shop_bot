from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from aiogram.fsm.state import StatesGroup, State, default_state

router = Router()


class FSMFillProfile(StatesGroup):
    fill_fio = State()
    fill_phone = State()
    fill_address = State()


@router.callback_query(F.data == 'fill_profile', StateFilter(default_state))
async def handle_clbck_button_fill_profile_pressed(callback: CallbackQuery):
    await callback.message.edit_text(
        text='📚 Введите ваше ФИО'
    )


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



