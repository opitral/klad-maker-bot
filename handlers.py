from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message

from filters import IsAdmin

router = Router()
router.message.filter(IsAdmin())


@router.message(CommandStart())
async def start_command_handler(message: Message):
    await message.answer("Hello, admin! How can I assist you today?")


@router.message(F.photo)
async def photo_handler(message: Message):
    await message.answer("You sent a photo!")
