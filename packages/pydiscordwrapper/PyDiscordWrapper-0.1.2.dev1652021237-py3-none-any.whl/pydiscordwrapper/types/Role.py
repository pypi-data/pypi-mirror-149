from pydantic import BaseModel


class Role(BaseModel):
    id: str
    name: str
    color: int
    hoist: bool
    position: int
    permissions: str
    managed: bool
    mentionable: bool
