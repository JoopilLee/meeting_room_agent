from sqlalchemy import func, select

from app.db.models import Building, Floor, Room
from app.db.session import get_session
from app.utils.building_manager import load_building_data


def seed_if_empty():
    with get_session() as session:
        if session.scalar(select(func.count()).select_from(Building)) > 0:
            return
        building_ids, floor_ids = load_building_data()
        for name, bid in building_ids.items():
            session.add(Building(id=bid, name=name))
        session.flush()
        floor_pk = 1
        room_pk = 1
        for building_id, floors in floor_ids.items():
            for floor_number, (_floor_id_yaml, room_dict) in floors.items():
                session.add(Floor(id=floor_pk, building_id=building_id, floor_number=floor_number))
                for room_name in room_dict.keys():
                    session.add(Room(id=room_pk, floor_id=floor_pk, name=room_name))
                    room_pk += 1
                floor_pk += 1
        session.flush()
