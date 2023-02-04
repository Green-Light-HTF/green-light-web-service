from sqlalchemy import Column, Integer, ForeignKey, Float, VARCHAR
from db.base_class import Base
from sqlalchemy.dialects.mysql import DATETIME


class AmbulanceData(Base):

    __tablename__ = "ambulance_data"

    id = Column(Integer, primary_key=True)
    lat = Column(VARCHAR(50))
    long = Column(VARCHAR(50))
    status = Column(Integer())

