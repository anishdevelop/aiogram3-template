from aiogram import Dispatcher, Router, types
from aiogram.filters import CommandStart
from app.services.fluent import TranslatorRunner


rt = Router()


@rt.message(CommandStart())
async def cmd_start(message: types.Message, i18n: TranslatorRunner) -> None:
    await message.answer(i18n.command.start())


def register(dp: Dispatcher):
    dp.include_router(rt)
