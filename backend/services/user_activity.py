from typing import Optional

from repositories.interfaces import IUserActivityRepository
from dto.user_activity import UserActivityDTO, UserActivityPostDTO


class UserActivityService:
    user_activity_repository: IUserActivityRepository

    def __init__(
        self,
        user_activity_repository: IUserActivityRepository,
    ) -> None:
        self.user_activity_repository = user_activity_repository

    async def add(self, user_activity: UserActivityPostDTO) -> None:
        await self.user_activity_repository.add(user_activity)

    async def get(self, id: int) -> Optional[UserActivityDTO]:
        return await self.user_activity_repository.get(id)

    async def list(
        self,
        user_ids: Optional[list[int]] = None,
        track_ids: Optional[list[int]] = None,
        offset: Optional[int] = None,
        limit: Optional[int] = None,
    ) -> list[UserActivityDTO]:
        return await self.user_activity_repository.list(
            user_ids=user_ids, track_ids=track_ids, offset=offset, limit=limit,
        )

    async def delete(self, id: int) -> None:
        return await self.user_activity_repository.delete(id)
