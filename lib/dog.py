import sqlite3

CONN = sqlite3.connect('lib/dogs.db')
CURSOR = CONN.cursor()

class Dog:
    def __init__(self, name, breed):
        self.name = name
        self.breed = breed
        self.id = None

    def save(self):
        # Check if the dog already exists in the database.
        if self.id is None:
            # If not, insert a new record.
            with CONN:
                CURSOR.execute("INSERT INTO dogs (name, breed) VALUES (?, ?)", (self.name, self.breed))
                # Set the id attribute based on the last inserted row (the new dog's ID).
                self.id = CURSOR.lastrowid
        else:
            # If the dog exists, update its record.
            self.update()

    def update(self):
        # Check if the dog already exists in the database (by checking its ID).
        if self.id is not None:
            with CONN:
                CURSOR.execute("UPDATE dogs SET name = ?, breed = ? WHERE id = ?", (self.name, self.breed, self.id))

    @classmethod
    def create_table(cls):
        with CONN:
            CURSOR.execute('''
                CREATE TABLE IF NOT EXISTS dogs (
                    id INTEGER PRIMARY KEY,
                    name TEXT NOT NULL,
                    breed TEXT NOT NULL
                )
            ''')

    @classmethod
    def drop_table(cls):
        with CONN:
            CURSOR.execute("DROP TABLE IF EXISTS dogs")

    @classmethod
    def create(cls, name, breed):
        dog = cls(name, breed)
        dog.save()
        return dog

    @classmethod
    def new_from_db(cls, db_row):
        id, name, breed = db_row
        dog = cls(name, breed)
        dog.id = id
        return dog

    @classmethod
    def get_all(cls):
        with CONN:
            CURSOR.execute("SELECT * FROM dogs")
            rows = CURSOR.fetchall()
        return [cls.new_from_db(row) for row in rows]

    @classmethod
    def find_by_name(cls, name):
        with CONN:
            CURSOR.execute("SELECT * FROM dogs WHERE name = ?", (name,))
            row = CURSOR.fetchone()
        if row:
            return cls.new_from_db(row)
        return None

    @classmethod
    def find_by_id(cls, id):
        with CONN:
            CURSOR.execute("SELECT * FROM dogs WHERE id = ?", (id,))
            row = CURSOR.fetchone()
        if row:
            return cls.new_from_db(row)
        return None

    @classmethod
    def find_or_create_by(cls, name, breed):
        # Check if a dog with the given name and breed already exists.
        existing_dog = cls.find_by_name(name)
        if existing_dog:
            return existing_dog
        # If the dog doesn't exist, create a new one and return it.
        return cls.create(name, breed)

