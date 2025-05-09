from dto.user_activity import UserActivityDTO, UserActivityPostDTO

from typing import Optional, Protocol


class IUserActivityRepository(Protocol):
    async def add(
        self,
        user_activity: UserActivityPostDTO,
    ) -> None: ...

    async def get(
        self,
        id: int,
    ) -> Optional[UserActivityDTO]: ...

    async def list(
        self,
        user_ids: Optional[list[int]],
        track_ids: Optional[list[int]],
        offset: Optional[int],
        limit: Optional[int],
    ) -> list[UserActivityDTO]: ...

    async def delete(
        self,
        id: int
    ) -> None: ...
