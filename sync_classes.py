import json
from database.db_manager import DnDDatabase
from api.dnd_api import DnDApiClient


def sync_all_classes():
    db = DnDDatabase()
    client = DnDApiClient()
    indices = client.get_all_classes()
    for i, api_index in enumerate(indices, start=1):
        char_class = client.get_class(api_index)
        class_name = char_class["name"]
        hit_die = char_class["hit_die"]
        desc = char_class.get("desc", [])
        description = "\n\n".join(desc) if desc else None
        db.add_class(api_index,class_name, hit_die, description)
        print(f"[{i}|{len(indices)}] {class_name}")
    db.close_connection()

if __name__ == "__main__":
    sync_all_classes()