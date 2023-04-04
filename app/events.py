from pathlib import Path

from aiogram import Dispatcher

from app.config_parser import Config
from app.db import init_engine, init_models, get_async_session_maker
from app.middlewares.db_session import DBSessionMiddleware
from app.middlewares.translator_runner import TranslatorRunnerMiddleware
from app.services.fluent import generate_hub


async def on_startup(dispatcher: Dispatcher):
    config: Config = dispatcher.workflow_data["config"]

    engine = await init_engine(config.db.url)
    await init_models(engine)
    session_maker = get_async_session_maker(engine)
    dispatcher.update.middleware.register(DBSessionMiddleware(session_maker))

    locales_dir = Path(__file__).parent.joinpath("locales")
    translator_hub = generate_hub(locales_dir, "ru")
    dispatcher.update.middleware.register(TranslatorRunnerMiddleware(translator_hub))

    from app import handlers

    handlers.register(dispatcher)
