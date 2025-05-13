from aiogram import F
from aiogram import Router
from aiogram.types import Message, PhotoSize

router = Router()


@router.message(F.photo[-1].as_('largest_photo'))
async def handle_img(message: Message, largest_photo: PhotoSize):
    print('!!!', largest_photo.file_unique_id)
    print('!!!', largest_photo.file_id)


@router.message()
async def handle_every_message(message: Message):
    await message.answer(text='Любой текст')
