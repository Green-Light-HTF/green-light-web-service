import json
import threading
from typing import Dict

import haversine
import requests
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from twilio.rest import Client

import dao
from api import deps

router = APIRouter()


@router.post("/file_sos",
             name="File SOS and "
             )
def file_sos(*, db: Session = Depends(deps.get_db), args: Dict):
    # args = json.loads(args)
    #
    # {
    #     lat,
    #     lng,
    #     ip: IPv4,
    # message: emergency,
    # other: information
    # }
    try:

        amb_id, location = dao.nearest_amb(db, args["lat"], args["lng"])
        user_data = {
            "ip": args['ip'],
            "message": args['message'],
            "lat": args['lat'],
            "long": args['lng'],
            "type": 1,  # user_type
            "status": 0,
            "assigned_amb": amb_id
        }
        # user_id = dao.create_user(db, user_data)

        call_ambulance(amb_id, args["lat"], args["lng"], init_lat=location[0], init_long=location[1])

        # dao.update_ambulance_status(db, amb_id)

        return {
            "amb_id": amb_id,
            "location": location,
            "user_id": 1
        }

    except Exception as e:
        raise e


def call_ambulance(amb_id, lat, long, init_lat, init_long):
    try:

        url = "http://127.0.0.1:8000/set_patient_loc?lat={}&long={}&amb_id={}&init_lat={}&init_long={}".format(lat,
                                                                                                               long,
                                                                                                               amb_id,
                                                                                                               init_lat,
                                                                                                               init_long)

        payload = {}
        headers = {
            'accept': 'application/json'
        }
        threading.Thread(target=request_task, args=(url, payload, headers)).start()

    except Exception as e:
        raise e


def request_task(url, payload, headers):
    response = requests.request("GET", url, headers=headers, data=payload)


def distance_between_coordinates(coord1, coord2):
    lat1, lon1 = coord1
    lat2, lon2 = coord2
    return haversine.haversine((lat1, lon1), (lat2, lon2)) * 1000


def get_location_info(lat, long, api_key):
    url = f"http://dev.virtualearth.net/REST/v1/Locations/{lat},{long}?key={api_key}"
    response = requests.get(url)
    return response.json()


def get_contact_to_notify(db, lat, long):
    print("In get Contact")
    query = dao.get_fl_workers(db)
    radius_items = {}
    all_fl_workers = {}
    for item in query:
        all_fl_workers[item.phone_no] = ((item.lat), item.long)
        dis = distance_between_coordinates((float(lat), float(long)), (item.lat, item.long))

        radius_items[dis] = item.phone_no
        print(dis)

    nearest = list(radius_items.keys())
    nearest.sort()
    if not nearest:
        return []
    # time calculate
    consider_index = []
    threshold = 80
    for i in nearest:
        if i <= threshold:
            consider_index.append(radius_items[i])
    print("Selected Numbers {}".format(consider_index))
    response_list = {k: v for k, v in all_fl_workers.items() if k in consider_index}
    return response_list


@router.get("/track_live_location")
async def track_live_location(*, db: Session = Depends(deps.get_db), user_id, amb_id, lat, long):
    try:

        message = dao.get_message_data(db, user_id)
        api_key = "AjPGihUegNVzAbd_Fe78htn--29QxOLn2i5_EJp2BaJbXvSGC-GzSHceIDm28quR"
        location_info = get_location_info(lat, long, api_key)
        loc_name = location_info["resourceSets"][0]['resources'][0]["name"]
        notification = "Patient met to an accident, Ambulance is on the way to {}. Please take necessary action. Track Ambulance live at " \
                       "http://192.168.50.143:3000/maps/".format(
            loc_name)
        if "heart" in message or "attack" in message:
            notification = "Ambulance carrying critical heart patient, is on the way to {}. " \
                           "Please take necessary action. Track Ambulance live at " \
                           "http://192.168.50.143:3000/maps/".format(
                loc_name)
        if "accident" in message:
            notification = "Patient met to an accident, Ambulance is on the way to {}. Please take necessary action".format(
                loc_name)
        print("In tracking ")
        numbers_to_notify = get_contact_to_notify(db, lat, long)
        for number in numbers_to_notify:
            print("Notify Send")
            account_sid = '***'
            auth_token = '***'
            client = Client(account_sid, auth_token)

            # Twilio Integration
            message = client.messages \
                .create(
                body=notification,
                from_='+14303051265',
                to=number
            )
            print(message.sid)
        response = {
            "numbers_to_notify": numbers_to_notify,
            "message": notification
        }

        return json.dumps(response)
    except Exception as e:
        return {}
