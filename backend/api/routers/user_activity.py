from typing import Optional
from fastapi import (
    APIRouter,
    Query,
    HTTPException,
    status,
    Depends,
)

from dto.user_activity import UserActivityDTO, UserActivityPostDTO
from services.user_activity import UserActivityService
from depends import get_user_activity_service

router = APIRouter(prefix='/user_activity', tags=['telemetry'])


@router.get(
    '/{id}',
    response_model=Optional[UserActivityDTO],
    status_code=status.HTTP_200_OK,
)
async def get_user_activity(
    id: int,
    user_activity_service: UserActivityService = Depends(
        get_user_activity_service
    ),
) -> Optional[UserActivityDTO]:
    try:
        user_activity = await user_activity_service.get(id)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=f'you stupid: {e}'
        )

    return user_activity


@router.get(
    '/',
    response_model=list[UserActivityDTO],
    status_code=status.HTTP_200_OK,
)
async def list_user_activities(
    user_ids: Optional[list[int]] = Query(None),
    track_ids: Optional[list[int]] = Query(None),
    limit: Optional[int] = None,
    offset: Optional[int] = None,
    user_activity_service: UserActivityService = Depends(
        get_user_activity_service
    ),
) -> list[UserActivityDTO]:
    try:
        user_activities = await user_activity_service.list(user_ids=user_ids, track_ids=track_ids, offset=offset, limit=limit)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=f'you stupid: {e}'
        )

    return user_activities


@router.post(
    '/',
    response_model=None,
    status_code=status.HTTP_201_CREATED
)
async def add_user_activity(
    user_id: int,
    track_id: int,
    event: str,
    user_activity_service: UserActivityService = Depends(
        get_user_activity_service
    ),
) -> None:
    try:
        user_activity = UserActivityPostDTO(
            user_id=user_id, track_id=track_id, event=event
        )
        await user_activity_service.add(user_activity)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=f'you stupid: {e}'
        )


@router.delete(
    '/{id}',
    status_code=status.HTTP_200_OK
)
async def delete_user_activity(
    id: int,
    user_activity_service: UserActivityService = Depends(
        get_user_activity_service
    ),
):
    try:
        await user_activity_service.delete(id)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=f'you stupid: {e}'
        )
