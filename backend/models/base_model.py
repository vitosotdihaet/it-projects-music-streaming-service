from sqlalchemy.ext.declarative import declarative_base
from configs.database import accounts_engine, get_db_connection_user_activity, music_engine, user_activity_engine


AccountsModelBase = declarative_base()
MusicModelBase = declarative_base()
UserActivityBase = declarative_base()


async def create_tables():
    async with accounts_engine.begin() as engine:
        await engine.run_sync(AccountsModelBase.metadata.create_all)
    async with music_engine.begin() as engine:
        await engine.run_sync(MusicModelBase.metadata.create_all)
    async with user_activity_engine.begin() as engine:
        await engine.run_sync(UserActivityBase.metadata.create_all)

        from models.user_activity import add_initial_events
        async for session in get_db_connection_user_activity():
            await add_initial_events(session)
