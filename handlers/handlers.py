from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message
from lexicon.lexicon_cmd import LEXICON_CMD


router = Router()


@router.message(CommandStart())
async def handle_cmd_start(message: Message):
    await message.answer_photo(
        photo=LEXICON_CMD['welcome_photo_id'],
        caption=LEXICON_CMD['/start']
    )
