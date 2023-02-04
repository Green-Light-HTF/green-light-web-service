from typing import Generic, TypeVar, Union, List, Dict, Type, Any
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy.exc import InternalError, IntegrityError
from sqlalchemy.orm import Session
from db.base_class import Base

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):

    def __init__(self, model: Type[ModelType]):
        self.model = model

    def get(self, db: Session, id: int) -> List[ModelType]:
        return db.query(self.model).filter(self.model.id == id).all()

    def get_all(self, *, db: Session) -> List[ModelType]:
        return db.query(self.model).all()

    def get_by_pagination(self, db: Session, *, NoOfRecords: int, PageNumber: int) -> List[ModelType]:
        return db.query(self.model).limit(NoOfRecords).offset((PageNumber - 1) * NoOfRecords).all()

    def create(self, db: Session, *, obj_in: CreateSchemaType) -> ModelType:
        try:
            obj_in_data = jsonable_encoder(obj_in)
            db_obj = self.model(**obj_in_data)
            db.add(db_obj)
            db.commit()
            db.refresh(db_obj)
            return db_obj
        except (ValueError, InternalError, IntegrityError) as e:
            raise e

    def update(self, db: Session, *, db_obj: ModelType, obj_in: Union[UpdateSchemaType, Dict[str, Any]]) -> ModelType:
        try:
            obj_data = jsonable_encoder(db_obj)

            db_obj = db_obj[0]

            if isinstance(obj_in, dict):
                update_data = obj_in
            else:
                update_data = obj_in.dict(exclude_unset=True)

            for field in obj_data[0]:
                if field in update_data:
                    setattr(db_obj, field, update_data[field])

            db.add(db_obj)
            db.commit()
            db.refresh(db_obj)
            return db_obj
        except (ValueError, InternalError, IntegrityError) as e:
            raise e

    def delete(self, db: Session, *, id: int) -> ModelType:
        try:
            db_obj = db.query(self.model).get(id)
            if db_obj:
                db.delete(db_obj)
                db.commit()
                return db_obj
            else:
                return "data not found by given id"
        except (ValueError, InternalError, IntegrityError) as e:
            raise e

    def create_multi(self, db: Session, *, obj_in: List[CreateSchemaType]) -> ModelType:
        try:
            obj_in_data = jsonable_encoder(obj_in)

            db_obj = [self.model(**obj) for obj in obj_in_data]
            db.add_all(db_obj)
            db.commit()
            # db.refresh(db_obj)
            return db_obj
        except (ValueError, InternalError, IntegrityError) as e:
            raise e
