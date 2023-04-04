from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker

from app.db import Base


async def init_engine(url: str):
    return create_async_engine(url, future=True, echo=True)


async def init_models(engine):
    from app.db import models  # noqa, Надо чтоб блять прогрузить модели

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


def get_async_session_maker(engine):
    return async_sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False, future=True
    )
