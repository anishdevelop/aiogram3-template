from typing import Dict, Any, Awaitable, Callable

from aiogram import BaseMiddleware
from aiogram.types import Update, User
from fluentogram import TranslatorHub


class TranslatorRunnerMiddleware(BaseMiddleware):
    def __init__(self, translator_hub: TranslatorHub):
        super().__init__()
        self.translator_hub = translator_hub

    async def __call__(
        self,
        handler: Callable[[Update, Dict[str, Any]], Awaitable[Any]],
        event: Update,
        data: Dict[str, Any],
    ) -> Any:
        user: User = data["event_from_user"]
        data["i18n"] = self.translator_hub.get_translator_by_locale(user.language_code)
        return await handler(event, data)
