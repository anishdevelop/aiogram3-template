from aiogram import Bot
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.client.telegram import TelegramAPIServer


def get_bot(botapi: str, bottoken: str):
    session = AiohttpSession(api=TelegramAPIServer.from_base(botapi))
    return Bot(bottoken, parse_mode="HTML", session=session)
