from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel

from .User import User


class Channel(BaseModel):
    id: str
    type: int
    guild_id: str
    position: int
    permission_overwrites: list
    name: str
    topic: Optional[str]
    nsfw: Optional[bool]
    last_message_id: Optional[str]
    bitrate: Optional[int]
    user_limit: Optional[int]
    rate_limit_per_user: Optional[int]
    recipients: Optional[List[User]]
    icon: Optional[str]
    owner_id: Optional[str]
    application_id: Optional[str]
    parent_id: Optional[str]
    last_pin_timestamp: Optional[datetime]
    rtc_region: Optional[str]
    message_count: Optional[int]
    member_count: Optional[int]
    flags: int
