from typing import Optional

from pydantic import BaseModel


class User(BaseModel):
    id: str
    username: str
    discriminator: str
    avatar: str
    bot: Optional[bool]
    system: Optional[bool]
    mfa_enabled: Optional[bool]
    banner: Optional[str]
    accent_color: Optional[int]
    locale: Optional[str]


class EmailUser(User):
    verified: bool
    email: str


class IdentifyUser(User):
    flags: int
    premium_type: int
    public_flags: int
