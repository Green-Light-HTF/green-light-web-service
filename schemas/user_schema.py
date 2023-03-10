
from pydantic import BaseModel
from typing import Optional


class UserSchema(BaseModel):
    id: Optional[int]
    ip: str
    lat: str
    long: str
    phone_no: int
    type: int
    message: str
    status: Optional[int]
    assigned_amb: int

    class Config:
        orm_mode = True
        schema_extra = {

        }
