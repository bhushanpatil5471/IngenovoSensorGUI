from typing import Optional
from pydantic import BaseModel
from requests.status_codes import _init


class User(BaseModel):
    username: str
    email: Optional[str] = None
    full_name: Optional[str] = None
    disabled: Optional[bool] = None
