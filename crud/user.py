from crud.base import CRUDBase
from models import AmbulanceData
from schemas.ambulance_schema import AmbulanceSchema


class CurdAmbulanceData(CRUDBase[AmbulanceData, AmbulanceSchema, AmbulanceSchema]):
    pass


AmbulanceCurd = CurdAmbulanceData(AmbulanceData)
