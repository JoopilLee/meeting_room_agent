from pathlib import Path
from typing import Any, Dict

import yaml


DEFAULT_BUILDINGS_DIR = "data/buildings"


def _load_yml(base_dir: Path, filename: str) -> Any:
    path = base_dir / filename
    if not path.exists():
        raise FileNotFoundError(f"Buildings data not found: {path}")
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def load_building_data(buildings_dir: str = None) -> tuple:
    """(building_ids: name->id, floor_ids: building_id->floor_number->[floor_id, rooms])."""
    if buildings_dir is None:
        base = Path(__file__).resolve().parent.parent.parent / DEFAULT_BUILDINGS_DIR
    else:
        base = Path(buildings_dir)
    raw_building_ids = _load_yml(base, "building_ids.yml")
    raw_floor_ids = _load_yml(base, "floor_ids.yml")

    building_ids = {}
    for k, v in raw_building_ids.items():
        if k.startswith("#"):
            continue
        building_ids[str(k).strip()] = int(v)

    floor_ids = {}
    for bid_key, floors in raw_floor_ids.items():
        if isinstance(floors, dict) and floors:
            bid = int(bid_key) if not isinstance(bid_key, int) else bid_key
            floor_ids[bid] = {}
            for f_key, f_val in floors.items():
                fn = int(f_key) if not isinstance(f_key, int) else f_key
                floor_ids[bid][fn] = f_val

    return building_ids, floor_ids
