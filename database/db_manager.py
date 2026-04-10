import sqlite3


class DnDDatabase:
    def __init__(self):
        self.connection = sqlite3.connect("dnd.db")
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
        self.connection.commit()


    def add_character(self, char_name, char_class ,char_race, char_level=1):
        """ Adds a character to the database """
        self.cursor.execute(
            "INSERT INTO characters (char_name, char_class, char_race, char_level) VALUES (?, ?, ?, ?)",
            (char_name, char_class, char_race, char_level)
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

if __name__ == "__main__":
    db = DnDDatabase()
    db.add_character("Aragorn", "Ranger", "Human", 5)
    print(db.get_all_characters())
    db.close_connection()