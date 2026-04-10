from dice.roller import roll_dice
from database.db_manager import DnDDatabase

while True:
    notation = input("Enter your notation: ")
    if notation == "q":
        break
    try:
        result = roll_dice(notation)
        print(f"Rolls: {result['rolls']}")
        print(f"Total: {result['total']}")
    except ValueError as e:
        print(f"Error: {e}")

def main():
    db = DnDDatabase()

    while True
        print("=== D&D Toolkit ===")
        print("[1] Add character")
        print("[2] Show all characters")
        print("[3] Update character")
        print("[4] Delete character")
        print("[q] Exit")
        choice = input("Choose: ").strip().lower()

        if choice == "q"
            db.close_connection()
            break
        elif

