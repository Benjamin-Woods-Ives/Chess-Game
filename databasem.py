import sqlite3 as sql


class GameSaves:
    """handles all the saves with sql"""
    def __init__(self):
        """connects to the database"""
        self.connection = sql.connect("Game save data")
        self.cursor = self.connection.cursor()
        self.create_game_saves()

    def create_game_saves(self):
        """creates a database called saves if a database with that name isn't already created"""
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS saves 
        (filename TEXT PRIMARY KEY NOT NULL,
        data BLOB NOT NULL, 
        moves BLOB NOT NULL)""")

    def get_data(self, name):
        """returns the data and moves fields with a given name"""
        self.cursor.execute("""
        SELECT data, moves
        FROM saves
        WHERE filename = (:name)""", {"name": name})
        return self.cursor.fetchone()

    def get_names(self):
        """returns every filename"""
        self.cursor.execute("""
        SELECT filename
        From saves""")
        return self.cursor.fetchall()

    def add_save(self, name, data, moves):
        """adds a save with the given name"""
        with self.connection:
            self.cursor.execute("""
            INSERT INTO saves (filename, data, moves)
            VALUES (:name, :data, :moves)""", {"name": name, "data": data, "moves": moves})

    def check_name(self, name):
        """checks that the given name isnt already in the database"""
        self.cursor.execute("""
        SELECT filename
        FROM saves
        WHERE filename = (:name)""", {"name": name})
        return self.cursor.fetchone() is None


if __name__ == '__main__':
    pass
