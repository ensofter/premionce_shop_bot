from aiogram import Router
from logging import getLogger

from aiogram.types import Message, CallbackQuery

router = Router()
logger = getLogger(__name__)


def debug_message(msg: Message | CallbackQuery):
    logger.info(f'!!! {msg.model_dump_json(exclude_none=True, indent=2)}')

# @router.callback_query