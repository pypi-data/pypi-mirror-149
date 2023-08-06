from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel

from .Role import Role
from .Emoji import Emoji
from .Member import Member
from .Channel import Channel

class Guild(BaseModel):
    id: str
    name: str
    icon: Optional[str]
    splash: Optional[str]
    owner: Optional[bool]
    owner_id: Optional[str]
    permissions: Optional[str]
    region: Optional[str]
    afk_channel_id: Optional[str]
    afk_timeout: Optional[int]
    widget_enabled: Optional[bool]
    widget_channel_id: Optional[str]
    verification_level: Optional[int]
    default_message_notifications: Optional[int]
    explicit_content_filter: Optional[int]
    roles: Optional[List[Role]]
    emojis: Optional[List[Emoji]]
    features: List[str]
    mfa_level: Optional[int]
    application_id: Optional[str]
    system_channel_id: Optional[int]
    rules_channel_id: Optional[str]
    joined_at: Optional[datetime]
    large: Optional[bool]
    unavailable: Optional[bool]
    member_count: Optional[int]
    members: Optional[List[Member]]
    channels: Optional[List[Channel]]
    threads: Optional[List[Channel]]
    presences: Optional[list]
    max_presences: Optional[int]
    max_members: Optional[int]
    vanity_url_code: Optional[str]
    description: Optional[str]
    banner: Optional[str]
    premium_tier: Optional[int]
    premium_subscription_count: Optional[int]
    preferred_locale: Optional[str]
    public_updates_channel_id: Optional[str]
    max_video_channel_users: Optional[int]
    approximate_member_count: Optional[int]
    approximate_presence_count: Optional[int]
    nsfw_level: Optional[int]
