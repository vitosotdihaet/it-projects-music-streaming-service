from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from configs.environment import get_environment_variables


ENV = get_environment_variables()


def get_psql_url(db_name: str) -> str:
    DB_NAME = db_name.upper().replace("-", "_")
    user = getattr(ENV, f'POSTGRESQL_{DB_NAME}_ROOT_USER')
    password = getattr(ENV, f'POSTGRESQL_{DB_NAME}_ROOT_PASSWORD')
    host = f'postgres-{db_name}-service'
    port = getattr(ENV, f'POSTGRESQL_{DB_NAME}_PORT')
    db = getattr(ENV, f'POSTGRESQL_{DB_NAME}_DB')

    return f'postgresql+asyncpg://{user}:{password}@{host}:{port}/{db}'


accounts_engine = create_async_engine(get_psql_url('accounts'), future=True)
user_activity_engine = create_async_engine(
    get_psql_url('user-activity'), future=True
)
music_engine = create_async_engine(get_psql_url('music'), future=True)

db_sessions = {
    'accounts': async_sessionmaker(
        autocommit=False, autoflush=False, bind=accounts_engine
    ),
    'user-activity': async_sessionmaker(
        autocommit=False, autoflush=False, bind=user_activity_engine
    ),
    'music': async_sessionmaker(
        autocommit=False, autoflush=False, bind=music_engine
    )
}


async def get_db_connection(db_name: str) -> AsyncGenerator[AsyncSession, None]:
    async with db_sessions[db_name]() as session:
        yield session


async def get_db_connection_accounts(
) -> AsyncGenerator[AsyncSession, None]:
    async for session in get_db_connection('accounts'):
        yield session


async def get_db_connection_user_activity(
) -> AsyncGenerator[AsyncSession, None]:
    async for session in get_db_connection('user-activity'):
        yield session


async def get_db_connection_music(
) -> AsyncGenerator[AsyncSession, None]:
    async for session in get_db_connection('music'):
        yield session
