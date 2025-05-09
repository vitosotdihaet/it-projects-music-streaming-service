from typing import Optional

from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from repositories.interfaces import IUserActivityRepository
from dto.user_activity import UserActivityDTO, UserActivityPostDTO
from models.user_activity import EventModel, UserActivityModel


class UserActivityRepository(IUserActivityRepository):
    session: AsyncSession

    def __init__(
        self, session
    ) -> None:
        self.session = session

    async def add(self, user_activity: UserActivityPostDTO) -> None:
        event_id = await self.session.scalar(select(EventModel.id).where(EventModel.name == user_activity.event))

        if not event_id:
            raise ValueError(
                f'Event type "{user_activity.event}" not found.'
            )

        db_model = UserActivityModel(
            user_id=user_activity.user_id,
            track_id=user_activity.track_id,
            event_type_id=event_id,
        )

        self.session.add(db_model)
        await self.session.commit()

    async def get(self, id: int) -> Optional[UserActivityDTO]:
        db_model = (await self.session.execute(
            select(UserActivityModel)
            .where(UserActivityModel.id == id)
            .options(selectinload(UserActivityModel.event))
        )).scalar_one_or_none()

        if not db_model:
            return None

        return UserActivityDTO.model_validate({
            **db_model.__dict__,
            'event': db_model.event.name
        })

    async def list(
        self,
        user_ids: Optional[list[int]] = None,
        track_ids: Optional[list[int]] = None,
        offset: Optional[int] = None,
        limit: Optional[int] = None,
    ) -> list[UserActivityDTO]:
        query = select(UserActivityModel)

        if user_ids:
            query = query.where(UserActivityModel.user_id.in_(user_ids))
        if track_ids:
            query = query.where(UserActivityModel.track_id.in_(track_ids))

        if offset is not None:
            query = query.offset(offset)
        if limit is not None:
            query = query.limit(limit)

        result = await self.session.execute(query.options(selectinload(UserActivityModel.event)))
        return [UserActivityDTO.model_validate({
            **db_model.__dict__,
            'event': db_model.event.name
        }) for db_model in result.scalars().all()]

    async def delete(self, id: int) -> None:
        instance = await self.session.get(UserActivityModel, id)

        if not instance:
            return

        await self.session.delete(instance)
        await self.session.commit()
