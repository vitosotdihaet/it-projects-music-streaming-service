import datetime
from pydantic import BaseModel, ConfigDict


class UserActivityPostDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    user_id: int
    track_id: int
    event: str


class UserActivityDTO(UserActivityPostDTO):
    id: int
    time: datetime.datetime
