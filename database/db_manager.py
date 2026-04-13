import sqlite3


class DnDDatabase:
    def __init__(self):
        self.connection = sqlite3.connect("dnd.db")
        self.connection.row_factory = sqlite3.Row
        self.cursor = self.connection.cursor()
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
                char_hp INTEGER,
                char_ac INTEGER
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
        self.connection.commit()


    def add_character(self, char_name, char_class ,char_race, char_level=1, char_hp=None, char_ac=None):
        """ Adds a character to the database """
        self.cursor.execute(
            "INSERT INTO characters (char_name, char_class, char_race, char_level, char_hp, char_ac) VALUES (?, ?, ?, ?, ?, ?)",
            (char_name, char_class, char_race, char_level, char_hp, char_ac)
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

    def update_character(self, char_id, char_name, char_class, char_race, char_level, char_hp, char_ac):
        """ Updates a character by its id """
        self.cursor.execute(
            """ UPDATE characters SET char_name = ?, char_class = ?, char_race = ?,
            char_level = ?, char_hp = ?, char_ac = ? WHERE char_id = ?""",
            (char_name, char_class, char_race, char_level, char_hp, char_ac, char_id)
        )
        self.connection.commit()

    def delete_character(self, char_id):
        """ Removes a character by its id """
        self.cursor.execute("DELETE FROM characters WHERE char_id = ?", (char_id,))
        self.connection.commit()


    def close_connection(self):
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



if __name__ == "__main__":
    db = DnDDatabase()
    """db.add_character("Aragorn", "Ranger", "Human", 1, 10, 10)
    db.add_character("Legolas", "Ranger", "Elf", 3)
    db.add_character("Gimli", "Fighter", "Dwarf", 4, 35, 18)"""
    for character in db.get_all_characters():
        print(f"{character['char_name']} (Level {character['char_level']}) -  {character['char_class']}, {character['char_race']}")
    db.close_connection()