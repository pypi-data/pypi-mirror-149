from datetime import datetime
from typing import List, Optional, Union

from pydantic import BaseModel

from .User import User
from .Role import Role

class Member(BaseModel):
    user : User
    nick : Optional[str]
    avatar : Optional[str]
    roles : Union[List[Role],List[str]]
    joined_at : datetime
    premium_since : Optional[datetime]
    deaf : bool
    mute : bool
    pending : bool
    permissions : Optional[str]
