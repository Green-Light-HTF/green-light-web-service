from pydantic import BaseModel


class AmbulanceSchema(BaseModel):
    id: int
    lat: str
    long: str

    class Config:
        orm_mode = True
        schema_extra = {
        }
