from crud.base import CRUDBase
from models import User
from schemas.user_schema import UserSchema


class CrudUser(CRUDBase[User, UserSchema, UserSchema]):
    pass


UserCurd = CrudUser(User)
