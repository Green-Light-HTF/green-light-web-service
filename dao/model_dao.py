import haversine
from sqlalchemy.orm import Session

import crud
from models import AmbulanceData, User


def create_user(db, user_data):
    try:
        user_id = crud.UserCurd.create(db=db, obj_in=user_data)
        return user_id
    except Exception as e:
        raise e


def get_fl_workers(db: Session):
    try:
        query = db.query(User.phone_no, User.lat, User.long) \
            .filter(User.type == 2)
        return query
    except Exception as e:
        raise e


def get_message_data(db: Session, user_id):
    try:
        query = db.query(User.message) \
            .filter(User.id == int(user_id))
        for r in query:
            return r[0]
        return ""
    except Exception as e:
        raise e


def distance_between_coordinates(coord1, coord2):
    lat1, lon1 = coord1
    lat2, lon2 = coord2
    return haversine.haversine((lat1, lon1), (lat2, lon2)) * 1000


def nearest_amb(db: Session, lat, lng):
    try:

        radius_items = {}
        all_ambulance = {}
        query = db.query(AmbulanceData.id, AmbulanceData.lat, AmbulanceData.long, AmbulanceData.status)
        for item in query:
            all_ambulance[item.id] = (item.lat, item.long)
            dis = distance_between_coordinates((float(lat), float(lng)), (float(item.lat), float(item.long)))
            radius_items[dis] = item.id

        nearest = list(radius_items.keys())
        nearest.sort()
        return radius_items[nearest[0]], all_ambulance[radius_items[nearest[0]]]
    except Exception as e:
        raise e
