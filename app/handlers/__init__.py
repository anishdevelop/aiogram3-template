from aiogram import Dispatcher

from app.handlers import start


__all__ = [
    start,
]


def register(dp: Dispatcher) -> None:
    for handler in __all__:
        handler.register(dp)
