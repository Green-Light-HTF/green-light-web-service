import datetime

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

import schemas
import crud
import dao
from api import deps
from typing import Any
import json

router = APIRouter()


@router.post("/file_sos",
             name="File SOS and ",
             tags=["Events"],
             )
def log_event(*, db: Session = Depends(deps.get_db), args):
    args = json.loads(args)
    #
    # {
    #     lat,
    #     lng,
    #     ip: IPv4,
    # message: emergency,
    # other: information
    # }
    try:
        amb_id = dao.nearest_amb(args["lat"], args["lng"])

        #Inform ambulance about incident
        pass

    except Exception as e:
        raise e
