from sqlalchemy import Column, Integer, ForeignKey, Float
from db.base_class import Base
from sqlalchemy.dialects.mysql import DATETIME


class AmbulanceData(Base):

    __tablename__ = "ambulance_data"

    id = Column(Integer, primary_key=True)
    lat = Column(Float(50))
    long = Column(Float(50))
    status = Column(Integer())

