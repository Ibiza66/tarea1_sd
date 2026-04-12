from pathlib import Path
import csv
from .zones import ZONES

DATA_PATH = Path(__file__).resolve().parents[2] / "data" / "buildings_sample.csv"


def load_data():
    data_by_zone = {zone_id: [] for zone_id in ZONES.keys()}

    with open(DATA_PATH, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)

        required_cols = {"latitude", "longitude", "area_in_meters", "confidence"}
        if not required_cols.issubset(reader.fieldnames or []):
            missing = required_cols - set(reader.fieldnames or [])
            raise ValueError(f"Faltan columnas requeridas: {missing}")

        for row in reader:
            building = {
                "latitude": float(row["latitude"]),
                "longitude": float(row["longitude"]),
                "area_in_meters": float(row["area_in_meters"]),
                "confidence": float(row["confidence"]),
            }

            for zone_id, zone in ZONES.items():
                if (
                    zone["lat_min"] <= building["latitude"] <= zone["lat_max"]
                    and zone["lon_min"] <= building["longitude"] <= zone["lon_max"]
                ):
                    data_by_zone[zone_id].append(building)

    return data_by_zone