from aiogram.filters import BaseFilter
from aiogram.types import Message

from app.config_parser import Config


class IsAdmin(BaseFilter):
    async def __call__(self, message: Message, config: Config) -> bool:
        return message.from_user.id == config.bot.admin
