from sqlalchemy.orm import Session
#
# import crud
# from models import AmbulanceData, User
from models import AmbulanceData, User
#
# def vaildate_event_id(db: Session, event_id):
#     try:
#         pass
#     except Exception as e:
#         raise e
#
#
# def fetch_columns(db: Session, event_id):
#     try:
#         column_data = db.query(ColumnMaster) \
#             .filter(ColumnMaster.event_master_id == event_id)
#
#         return column_data
#     except Exception as e:
#         raise e
#
#
# def create_event_analysis_log(db, event_analysis_dict):
#     try:
#
#         event_analysis_id = crud.AmbulanceCurd.create(db=db, obj_in=event_analysis_dict)
#         return event_analysis_id
#     except Exception as e:
#         raise e
#
#
# def add_meta_data(db, meta_data):
#     try:
#
#         meta = crud.MetaDataCurd.create_multi(db=db,obj_in=meta_data)
#     except Exception as e:
#         raise e
#
#
# def get_events_by_module(db, module_id):
#     try:
#
#         events = db.query(EventMaster).filter(EventMaster.module_id == module_id)
#         return events
#     except Exception as e:
#         raise e
#
#
# def get_event_data_based_on_from_to_datetime(db, from_date_time, to_date_time, event_ids):
#     try:
#         event_data = db.query(EventAnalysisDetails.event_master_id,
#                               EventAnalysisDetails.start_time,
#                               EventAnalysisDetails.end_time,
#                               EventAnalysisDetails.unique_value_1,
#                               EventAnalysisDetails.unique_value_2) \
#             .filter(EventAnalysisDetails.start_time >= from_date_time,
#                     EventAnalysisDetails.end_time <= to_date_time)
#         if event_ids != ['all']:
#             event_data = event_data.filter(EventAnalysisDetails.event_master_id.in_(event_ids))
#         return event_data
#     except Exception as e:
#         raise e
#
#
# def get_event_data_based_on_pack_ids(db, pack_ids, event_ids):
#     try:
#         # pack_ids = str(pack_ids)[1:-1]
#         event_data = db.query(EventAnalysisDetails.event_master_id,
#                               EventAnalysisDetails.start_time,
#                               EventAnalysisDetails.end_time,
#                               EventAnalysisDetails.unique_value_1,
#                               EventAnalysisDetails.unique_value_2)
#         event_data = event_data.filter(EventAnalysisDetails.unique_value_2.in_(pack_ids))
#         if event_ids != ['all']:
#             event_data = event_data.filter(EventAnalysisDetails.event_master_id.in_(event_ids))
#         return event_data
#     except Exception as e:
#         raise e
#
#
# def get_event_name_based_on_event_id(db: Session, event_ids) -> list:
#     try:
#         event_data = db.query(EventMaster.event_name,
#                               EventMaster.id) \
#             .filter(EventMaster.id.in_(event_ids))
#         return event_data
#     except Exception as e:
#         raise e
#
#
# def get_event_data_based_on_event_ids(db: Session, event_ids, from_date_time, to_date_time, bar_chart_flag=False):
#     try:
#         if bar_chart_flag == "True":
#             event_ids1 = event_ids.copy()
#             event_ids1.append("27")
#         else:
#             event_ids1 = event_ids.copy()
#         event_data = db.query(EventAnalysisDetails.event_master_id,
#                               EventAnalysisDetails.start_time,
#                               EventAnalysisDetails.end_time,
#                               EventAnalysisDetails.unique_value_1,
#                               EventAnalysisDetails.unique_value_2).filter(
#             EventAnalysisDetails.start_time >= from_date_time,
#             EventAnalysisDetails.end_time <= to_date_time)
#         if event_ids != ['all']:
#             event_data = event_data.filter(EventAnalysisDetails.event_master_id.in_(event_ids1))
#         return event_data
#     except Exception as e:
#         raise e
import math


def nearest_amb(db: Session, lat, lng):
    try:

        radius_items = {}
        query = db.query(AmbulanceData.id, AmbulanceData.lat, AmbulanceData.long, AmbulanceData.status)
        for item in query:
            lat_dist = float(lat) - item.lat
            lng_dist = float(lng) - item.long
            act_dist = math.sqrt((lat_dist * lat_dist) + (lng_dist * lng_dist))
            radius_items[act_dist] = item.id

        nearest = list(radius_items.keys()).sort()
        return nearest[0]
    except Exception as e:
        raise e