from sqlalchemy import Column, ForeignKey, VARCHAR, Integer, Float
from db.base_class import Base


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    ip = Column(VARCHAR(20))
    lat = Column(Float(50))
    long = Column(Float(50))
    phone_no = Column(Integer())
    type = Column(Integer())
    status = Column(Integer(), nullable=True)
