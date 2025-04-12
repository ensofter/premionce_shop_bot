from aiogram import Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from lexicon.lexicon_cmd import LEXICON_CMD


router = Router()


@router.message(CommandStart())
async def handle_cmd_start(message: Message):
    await message.answer_photo(
        photo=LEXICON_CMD['welcome_photo_id'],
        caption=LEXICON_CMD['/start']
    )


@router.message(Command(commands='help'))
async def handle_cmd_help(message: Message):
    await message.answer(
        text=LEXICON_CMD['/help']
    )