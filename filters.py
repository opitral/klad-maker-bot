from aiogram.enums import ChatType
from aiogram.filters import BaseFilter

from aiogram.types import Message

from settings import settings


class IsAdmin(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        if message.chat.type not in {ChatType.PRIVATE}:
            return False

        if message.from_user.id not in settings.ADMINS_TELEGRAM_ID:
            return False

        return True
