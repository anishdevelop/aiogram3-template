import asyncio
import logging
from typing import Any

from aiogram import Bot, Dispatcher
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from aiohttp.web import Application, Request, Response
from aiohttp.web_runner import AppRunner, TCPSite

from app.config_parser import ConfigWebhook


class SimpleRequestHandlerWithSecret(SimpleRequestHandler):
    def __init__(
        self,
        dispatcher: Dispatcher,
        bot: Bot,
        secret: str,
        handle_in_background: bool = True,
        **data: Any,
    ):
        super().__init__(
            dispatcher, bot, handle_in_background=handle_in_background, **data
        )
        self.secret = secret

    async def handle(self, request: Request) -> Response:
        if (
            self.secret
            and request.headers.get("X-Telegram-Bot-Api-Secret-Token") != self.secret
        ):
            return Response(status=403)

        return await super().handle(request)


async def run_app(app: Application, webhook: ConfigWebhook):
    runner = AppRunner(app)
    await runner.setup()
    site = TCPSite(runner, webhook.host, webhook.port)
    await site.start()

    # Sleep forever
    try:
        await asyncio.Event().wait()
    finally:
        await runner.cleanup()


async def start_webhook(
    webhook: ConfigWebhook, dp: Dispatcher, bot: Bot, close_bot_session: bool = True
):
    app = Application()

    SimpleRequestHandlerWithSecret(
        dp,
        bot,
        webhook.secret.get_secret_value() if webhook.secret else None,
    ).register(app, webhook.path)
    setup_application(app, dp)

    try:
        logging.warning(
            f"Webhook is running on {webhook.host}:{webhook.port}{webhook.path if webhook.path != '/' else ''}"
        )
        await run_app(app, webhook)
    finally:
        logging.warning("Bot webhook is stopped.")
        if close_bot_session:
            await bot.session.close()
