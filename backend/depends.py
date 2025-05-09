import models
from services.user_activity import UserActivityService
from repositories.user_activity import UserActivityRepository
from configs.database import get_db_connection_user_activity
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request


@asynccontextmanager
async def lifespan(app: FastAPI):
    async for session in get_db_connection_user_activity():
        app.state.user_activity_repository = UserActivityRepository(
            session
        )
    app.state.user_activity_service = UserActivityService(
        app.state.user_activity_repository
    )

    await models.create_tables()

    yield


def get_user_activity_service(request: Request) -> UserActivityService:
    return request.app.state.user_activity_service
