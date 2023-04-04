import asyncio
import logging
import argparse
from pathlib import Path

from aiogram import Bot, Dispatcher, types
from aiogram.fsm.storage.redis import RedisStorage

from app import web
from app.config_parser import Config
from app.bot import get_bot
from app.events import on_startup
from app.db import init_engine, init_models


def parse_arguments():
    parser = argparse.ArgumentParser(description="Process bot configuration.")
    parser.add_argument(
        "--locales",
        "-l",
        type=str,
        help="locales directory",
        default=Path(__file__).parent.parent / "locales",
    )
    parser.add_argument("--set-commands", "-s", action="store_true")

    return parser.parse_args()


async def set_bot_commands(bot: Bot):
    commands = [types.BotCommand(command="start", description="just start")]
    await bot.set_my_commands(commands, scope=types.BotCommandScopeDefault())


async def main() -> None:
    logging.basicConfig(
        level=logging.WARNING,
        format="%(asctime)s|%(levelname)s|%(name)s|%(message)s",
        datefmt="%Y-%m-%d|%H:%M:%S",
    )

    arguments = parse_arguments()
    config = Config()
    bot = get_bot(config.bot.api, config.bot.token.get_secret_value())

    storage = RedisStorage.from_url(config.storage.redis_url)
    dp = Dispatcher(storage=storage)
    dp.workflow_data.update(
        config=config,
    )
    dp.startup.register(on_startup)

    if arguments.set_commands:
        await set_bot_commands(bot)

    if config.webhook:
        return await web.start_webhook(config.webhook, dp, bot)

    try:
        logging.warning("Bot polling is starting...")
        await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
    finally:
        logging.warning("Bot polling is stopped.")


def run():
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logging.error("Bot stopped!")
