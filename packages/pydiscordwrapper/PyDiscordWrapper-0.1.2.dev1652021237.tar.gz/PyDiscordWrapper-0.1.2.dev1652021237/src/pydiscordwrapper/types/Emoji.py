from typing import Optional, List

from pydantic import BaseModel

from .Role import Role
from .User import User


class Emoji(BaseModel):
    id: str
    name: Optional[str]
    roles: List[Role]
    user: Optional[User]
    require_color: Optional[bool]
    managed: bool
    animated: bool
    available: bool
