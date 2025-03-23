import sqlite3
import random

def connect_db():
    conn = sqlite3.connect('Systemdb.db')
    cursor = conn.cursor()
    cursor.execute("PRAGMA foreign_keys = ON;")

    # Create Users Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL
    );
    """)

    # Create Doctors Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS doctors (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        specialty TEXT NOT NULL,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL
    );
    """)

    # Create Appointments Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS appointments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        appointment_id INTEGER NOT NULL,
        patient_name TEXT NOT NULL,
        doctor TEXT NOT NULL,
        date TEXT NOT NULL,
        time TEXT NOT NULL,
        status TEXT NOT NULL
    );
    """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS pets (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        name TEXT NOT NULL,
        species TEXT NOT NULL,
        age INTEGER,
        picture_path TEXT,
        FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
    );
    """)

    # Insert Predefined Doctor if Not Exists
    cursor.execute("SELECT COUNT(*) FROM doctors WHERE username = ?", ("dr_marlo",))
    if cursor.fetchone()[0] == 0:
        cursor.execute("INSERT INTO doctors (name, specialty, username, password) VALUES (?, ?, ?, ?)",
                       ("Dr. Marlo Veluz", "General Medicine", "dr_marlo", "marlo"))
        conn.commit()

    conn.close()

def insert_user(username, password):
    try:
        conn = sqlite3.connect('Systemdb.db')
        cursor = conn.cursor()

        cursor.execute("SELECT COUNT(*) FROM users WHERE username = ?", (username,))
        if cursor.fetchone()[0] > 0:
            raise ValueError("Username already exists. Please choose a different one.")

        random_id = random.randint(10000, 99999)  # Generates a 5-digit random ID
        cursor.execute("INSERT INTO users (id, username, password) VALUES (?, ?, ?)", (random_id, username, password))
        conn.commit()
        return random_id  # Return generated ID
    except sqlite3.Error:
        raise
    finally:
        conn.close()

def validate_user(username, password):
    try:
        conn = sqlite3.connect('Systemdb.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
        user = cursor.fetchone()
        return bool(user)
    finally:
        conn.close()

def get_user_id(username):
    """Retrieve the user ID for a given username."""
    try:
        conn = sqlite3.connect('Systemdb.db')
        cursor = conn.cursor()

        # Query to get the user ID
        cursor.execute("SELECT id FROM users WHERE username = ?", (username,))
        user = cursor.fetchone()

        # Return the user ID if found, otherwise None
        return user[0] if user else None
    finally:
        conn.close()

def get_user_pets(username):
    try:
        conn = sqlite3.connect('Systemdb.db')
        cursor = conn.cursor()

        # Get user ID from username
        cursor.execute("SELECT id FROM users WHERE username = ?", (username,))
        user = cursor.fetchone()
        if not user:
            return []

        user_id = user[0]

        # Get pets for the user
        cursor.execute("SELECT name, species, age, picture_path FROM pets WHERE user_id = ?", (user_id,))
        pets = [{"name": row[0], "species": row[1], "age": row[2], "picture_path": row[3]} for row in cursor.fetchall()]
        return pets
    finally:
        conn.close()

def add_pet(user_id, name, species, age, picture_path=None):
    try:
        conn = sqlite3.connect('Systemdb.db')
        cursor = conn.cursor()

        # Insert pet details into the pets table
        cursor.execute("""
            INSERT INTO pets (user_id, name, species, age, picture_path)
            VALUES (?, ?, ?, ?, ?)
        """, (user_id, name, species, age, picture_path))

        conn.commit()
    except sqlite3.Error as e:
        print(f"Database error: {e}")  # Debugging output
        raise
    finally:
        conn.close()
