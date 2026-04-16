import sqlite3
import os
import json


class DnDDatabase:
    def __init__(self):
        db_path = os.path.join(os.path.dirname(__file__), "..", "dnd.db")
        self.connection = sqlite3.connect(db_path)
        self.connection.row_factory = sqlite3.Row
        self.cursor = self.connection.cursor()
        self.cursor.execute("PRAGMA foreign_keys = ON")
        self.create_tables()

    def create_tables(self):
        """ Creates all tables if they don't exist """
        self.cursor.execute(
            """ 
            CREATE TABLE IF NOT EXISTS characters (
                char_id INTEGER PRIMARY KEY AUTOINCREMENT,
                char_name TEXT NOT NULL,
                char_class TEXT,
                char_race TEXT,
                char_level INTEGER DEFAULT 1,
                max_hp INTEGER,
                
                -- Ability Scores
                strength INTEGER DEFAULT 10,
                dexterity INTEGER DEFAULT 10,
                constitution INTEGER DEFAULT 10,
                intelligence INTEGER DEFAULT 10,
                wisdom INTEGER DEFAULT 10,
                charisma INTEGER DEFAULT 10,
                
                -- Fight
                current_hp INTEGER,
                armor_class INTEGER,
                speed INTEGER DEFAULT 30,
                proficiency_bonus INTEGER DEFAULT 2
            )
            """
        )
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS spells (
                spell_id INTEGER PRIMARY KEY AUTOINCREMENT,
                api_index TEXT UNIQUE NOT NULL,
                spell_name TEXT NOT NULL,
                spell_level INTEGER,
                spell_school TEXT,
                description TEXT
            )
            """
        )
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS character_spells (
                char_id INTEGER NOT NULL,
                spell_id INTEGER NOT NULL,
                PRIMARY KEY (char_id, spell_id),
                FOREIGN KEY (char_id) REFERENCES characters(char_id) ON DELETE CASCADE,
                FOREIGN KEY (spell_id) REFERENCES spells(spell_id) ON DELETE CASCADE
            )
            """
        )
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS items (
                item_id INTEGER PRIMARY KEY AUTOINCREMENT,
                api_index TEXT UNIQUE NOT NULL,
                item_name TEXT NOT NULL,
                item_cost TEXT,
                item_weight INTEGER,
                description TEXT
            )
            """
        )
        self.cursor.execute(
            """ 
            CREATE TABLE IF NOT EXISTS character_inventory (
                char_id INTEGER NOT NULL,
                item_id INTEGER NOT NULL,
                item_quantity INTEGER DEFAULT 1,
                PRIMARY KEY (char_id, item_id),
                FOREIGN KEY (char_id) REFERENCES characters(char_id) ON DELETE CASCADE,
                FOREIGN KEY (item_id) REFERENCES items(item_id) ON DELETE CASCADE
                )
            """
        )
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS monsters (
                monster_id INTEGER PRIMARY KEY AUTOINCREMENT,
                api_index TEXT UNIQUE NOT NULL,
                monster_name TEXT NOT NULL,
                max_hp INTEGER,
                monster_size TEXT,
                monster_type TEXT,
                armor_class INTEGER,
                challenge_rating REAL,
                raw_json TEXT
            )
            """
        )
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS classes (
                class_id INTEGER PRIMARY KEY AUTOINCREMENT,
                api_index TEXT UNIQUE NOT NULL,
                class_name TEXT NOT NULL,
                hit_die INTEGER,
                description TEXT
            )
            """
        )
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS races (
                race_id INTEGER PRIMARY KEY AUTOINCREMENT,
                api_index TEXT UNIQUE NOT NULL,
                race_name TEXT NOT NULL,
                speed INTEGER,
                size TEXT,
                description TEXT
            )
            """
        )
        self.connection.commit()


    def add_character(self, char_name, char_class, char_race, char_level=1, max_hp=None, armor_class=None):
        """ Adds a character to the database """
        self.cursor.execute(
            "INSERT INTO characters (char_name, char_class, char_race, char_level, max_hp, armor_class) VALUES (?, ?, ?, ?, ?, ?)",
            (char_name, char_class, char_race, char_level, max_hp, armor_class)
        )
        self.connection.commit()
        return self.cursor.lastrowid

    def get_all_characters(self):
        """ Returns all characters """
        self.cursor.execute("SELECT * FROM characters")
        return self.cursor.fetchall()

    def get_character(self, char_id):
        """ Returns a character by its id """
        self.cursor.execute("SELECT * FROM characters WHERE char_id = ?", (char_id,))
        return self.cursor.fetchone()

    def update_character(self, char_id, char_name, char_class, char_race, char_level, max_hp, armor_class):
        """ Updates a character by its id """
        self.cursor.execute(
            """ UPDATE characters SET char_name = ?, char_class = ?, char_race = ?,
            char_level = ?, max_hp = ?, armor_class = ? WHERE char_id = ?""",
            (char_name, char_class, char_race, char_level, max_hp, armor_class, char_id)
        )
        self.connection.commit()

    def delete_character(self, char_id):
        """ Removes a character by its id """
        self.cursor.execute("DELETE FROM characters WHERE char_id = ?", (char_id,))
        self.connection.commit()

    def close_connection(self):
        """ Closes the database connection """
        self.connection.close()

    def add_spell(self, api_index, spell_name, spell_level, spell_school, description):
        """ Adds a spell to the database """
        self.cursor.execute(
            """ INSERT OR REPLACE INTO spells (api_index, spell_name, spell_level, spell_school, description)
            Values (?, ?, ?, ?, ?)""",
            (api_index, spell_name, spell_level, spell_school, description)
        )
        self.connection.commit()
        return self.cursor.lastrowid

    def learn_spell(self, char_id, spell_id):
        """ Adds a spell to a character """
        self.cursor.execute(
            """ INSERT OR IGNORE INTO character_spells (char_id, spell_id) VALUES (?, ?)""",
            (char_id, spell_id)
        )
        self.connection.commit()

    def get_character_spells(self, char_id):
        """ Returns all spells a character knows """
        self.cursor.execute(
            """
            SELECT spells.* FROM spells
            JOIN character_spells ON spells.spell_id = character_spells.spell_id
            WHERE character_spells.char_id = ?""",
            (char_id,)
        )
        return self.cursor.fetchall()

    def add_item(self, api_index, item_name, item_cost, item_weight, description):
        """ Adds an item to the database """
        self.cursor.execute(
            """ INSERT OR REPLACE INTO items (api_index, item_name, item_cost, item_weight, description)
            VALUES (?, ?, ?, ?, ?) """,
            (api_index, item_name, item_cost, item_weight, description)
        )
        self.connection.commit()
        return self.cursor.lastrowid

    def obtain_item(self, char_id, item_id, item_quantity):
        """ Adds an item to a character """
        self.cursor.execute(
            """ INSERT OR REPLACE INTO character_inventory (char_id, item_id, item_quantity) VALUES (?, ?, ?)""",
            (char_id, item_id, item_quantity)
        )
        self.connection.commit()

    def get_character_items(self, char_id):
        """ Returns all items a character knows """
        self.cursor.execute(
            """
                SELECT items.*, character_inventory.item_quantity FROM items
                JOIN character_inventory ON items.item_id = character_inventory.item_id
                WHERE character_inventory.char_id = ?
            """,
            (char_id,)
        )
        return self.cursor.fetchall()


    def add_monster(self, api_index, monster_name, max_hp, monster_size, monster_type, armor_class, challenge_rating, raw_json):
        """ Adds a monster to the database """
        self.cursor.execute(
            """
            INSERT OR REPLACE INTO monsters (api_index, monster_name, max_hp, monster_size, monster_type, armor_class, challenge_rating, raw_json)  
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (api_index, monster_name, max_hp, monster_size, monster_type, armor_class, challenge_rating, raw_json)
        )
        self.connection.commit()


    def add_class(self, api_index, class_name, hit_die, description):
        """ Adds a class to a character """
        self.cursor.execute(
            """
            INSERT OR REPLACE INTO classes(api_index, class_name, hit_die, description) VALUES (?, ?, ?, ?)
            """,
            (api_index, class_name, hit_die, description)
        )
        self.connection.commit()


    def add_race(self, api_index, race_name, speed, size, description):
        """ Adds a race to a character """
        self.cursor.execute(
            """
            INSERT OR IGNORE INTO races(api_index, race_name, speed, size, description)
            VALUES (?, ?, ?, ?, ?)
            """,
            (api_index, race_name, speed, size, description)
        )
        self.connection.commit()




if __name__ == "__main__":
    db = DnDDatabase()
    db.add_character("Gandalf", "Wizard", "Maia", 20)
    db.add_character("Aragorn", "Ranger", "Human", 1, 10, 10)
    db.add_character("Legolas", "Ranger", "Elf", 3)
    db.add_character("Gimli", "Fighter", "Dwarf", 4, 35, 18)
    item = db.cursor.execute("SELECT item_id FROM items WHERE api_index = ?", ("book",)).fetchone()
    db.obtain_item(2, item["item_id"], 2)
    for s in db.get_character_items(2):
        print(f"{s['item_name']} x {s['item_quantity']}")
    spell = db.cursor.execute("SELECT spell_id FROM spells WHERE api_index = ?", ("fireball",)).fetchone()
    db.learn_spell(1, spell["spell_id"])
    print("\nGandalfs Zauber:")
    for s in db.get_character_spells(1):
        print(f" - {s['spell_name']} (Level {s['spell_level']}, {s['spell_school']})")
    for character in db.get_all_characters():
        print(
            f"{character['char_name']} (Level {character['char_level']}) -  {character['char_class']}, {character['char_race']}")
    db.close_connection()
