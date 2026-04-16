import json
from database.db_manager import DnDDatabase
from api.dnd_api import DnDApiClient


def sync_all_races():
    db = DnDDatabase()
    client = DnDApiClient()
    indices = client.get_all_races()
    for i, api_index in enumerate(indices, start=1):
        race = client.get_race(api_index)
        race_name = race["name"]
        speed = race["speed"]
        size = race["size"]
        desc = race.get("desc", [])
        description = "\n\n".join(desc) if desc else None
        db.add_race(api_index, race_name, speed, size, description)
        print(f"[{i}|{len(indices)}] {race_name}")
    db.close_connection()

if __name__ == "__main__":
    sync_all_races()
