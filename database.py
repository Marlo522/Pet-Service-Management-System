import sqlite3
import random
import os  # Import os module for path handling

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
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS grooming_services (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        pet_name TEXT NOT NULL,
        service_type TEXT NOT NULL,
        service_date TEXT NOT NULL,
        status TEXT DEFAULT 'Pending',
        FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
    );
    """)

    # Create Service History Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS service_history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        pet_name TEXT NOT NULL,
        service_type TEXT NOT NULL,
        date TEXT NOT NULL,
        details TEXT,
        status TEXT DEFAULT 'Pending',
        FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
    );
    """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS admin (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL
    );
    """)

    # Insert Predefined Admin Account if Not Exists
    cursor.execute("SELECT COUNT(*) FROM admin WHERE username = ?", ("admin",))
    if cursor.fetchone()[0] == 0:
        cursor.execute("INSERT INTO admin (username, password) VALUES (?, ?)", ("admin", "admin"))
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

        # Resolve picture_path to an absolute path if provided
        if picture_path:
            picture_path = os.path.abspath(picture_path)

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

def delete_pet(user_id, pet_name):
    """Delete a pet by name for a specific user and remove related records."""
    try:
        conn = sqlite3.connect('Systemdb.db')
        cursor = conn.cursor()

        # Delete related records from service_history
        cursor.execute("DELETE FROM service_history WHERE user_id = ? AND pet_name = ?", (user_id, pet_name))

        # Delete related records from grooming_services
        cursor.execute("DELETE FROM grooming_services WHERE user_id = ? AND pet_name = ?", (user_id, pet_name))

        # Delete the pet itself
        cursor.execute("DELETE FROM pets WHERE user_id = ? AND name = ?", (user_id, pet_name))

        conn.commit()
    except sqlite3.Error as e:
        print(f"Database error: {e}")  # Debugging output
        raise
    finally:
        conn.close()

def edit_pet(user_id, old_name, new_name, new_species, new_age, new_picture_path=None):
    """Edit a pet's details."""
    try:
        conn = sqlite3.connect('Systemdb.db')
        cursor = conn.cursor()

        # Resolve picture_path to an absolute path if provided
        if new_picture_path:
            new_picture_path = os.path.abspath(new_picture_path)

        cursor.execute("""
            UPDATE pets
            SET name = ?, species = ?, age = ?, picture_path = ?
            WHERE user_id = ? AND name = ?
        """, (new_name, new_species, new_age, new_picture_path, user_id, old_name))
        conn.commit()
    finally:
        conn.close()

def delete_user(user_id):
    """Delete a user from the database by user ID."""
    try:
        conn = sqlite3.connect('Systemdb.db')
        cursor = conn.cursor()
        
        # Delete the user from the users table
        cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
        
        # Optionally, you can also delete related pets and services if needed
        cursor.execute("DELETE FROM pets WHERE user_id = ?", (user_id,))
        cursor.execute("DELETE FROM grooming_services WHERE user_id = ?", (user_id,))
        cursor.execute("DELETE FROM service_history WHERE user_id = ?", (user_id,))
        
        conn.commit()
    except sqlite3.Error as e:
        print(f"Database error: {e}")  # Debugging output
        raise
    finally:
        conn.close()
        
def get_all_users():
    """Retrieve all users from the database."""
    try:
        conn = sqlite3.connect('Systemdb.db')
        cursor = conn.cursor()
        cursor.execute("SELECT id, username FROM users")
        users = [{"id": row[0], "username": row[1]} for row in cursor.fetchall()]
        return users
    finally:
        conn.close()

def get_all_pets():
    """Retrieve all pets from the database."""
    try:
        conn = sqlite3.connect('Systemdb.db')
        cursor = conn.cursor()
        cursor.execute("SELECT user_id, name, species FROM pets")
        pets = [{"user_id": row[0], "name": row[1], "species": row[2]} for row in cursor.fetchall()]
        return pets
    finally:
        conn.close()
        
def add_grooming_service(user_id, pet_name, service_type, service_date, status='Pending'):
    """Add a grooming service booking to the database."""
    try:
        conn = sqlite3.connect('Systemdb.db')
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO grooming_services (user_id, pet_name, service_type, service_date, status)
            VALUES (?, ?, ?, ?, ?)
        """, (user_id, pet_name, service_type, service_date, status))
        conn.commit()
    except sqlite3.Error as e:
        print(f"Database error: {e}")  # Debugging output
        raise
    finally:
        conn.close()

def get_grooming_appointments(username, status=None):
    """Retrieve all grooming appointments for a specific user with optional status filter."""
    try:
        conn = sqlite3.connect('Systemdb.db')
        cursor = conn.cursor()

        # Get user ID from username
        cursor.execute("SELECT id FROM users WHERE username = ?", (username,))
        user = cursor.fetchone()
        if not user:
            return []

        user_id = user[0]

        # Fetch grooming appointments for the user
        query = """
            SELECT id, pet_name, service_type, service_date
            FROM grooming_services
            WHERE user_id = ? AND status = 'Pending'
        """
        params = [user_id]
        if status:
            query += " AND status = ?"
            params.append(status)

        cursor.execute(query, params)
        appointments = [
            {"id": row[0], "pet_name": row[1], "service_type": row[2], "service_date": row[3]}
            for row in cursor.fetchall()
        ]
        return appointments
    finally:
        conn.close()

def cancel_grooming_appointment(appointment_id):
    """Cancel a grooming appointment by its ID."""
    try:
        conn = sqlite3.connect('Systemdb.db')
        cursor = conn.cursor()
        cursor.execute("DELETE FROM grooming_services WHERE id = ?", (appointment_id,))
        conn.commit()
    finally:
        conn.close()

def add_service_history(user_id, pet_name, service_type, date, details=None, status='Pending'):
    """Add a record to the service history."""
    try:
        conn = sqlite3.connect('Systemdb.db')
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO service_history (user_id, pet_name, service_type, date, details, status)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (user_id, pet_name, service_type, date, details, status))
        conn.commit()
    finally:
        conn.close()

def get_all_grooming_appointments():
    """Retrieve all grooming appointments for admin view."""
    try:
        conn = sqlite3.connect('Systemdb.db')
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, user_id, pet_name, service_type, service_date, status
            FROM grooming_services
            ORDER BY service_date DESC
        """)
        appointments = [
            {
                "id": row[0],
                "user_id": row[1],
                "pet_name": row[2],
                "service_type": row[3],
                "service_date": row[4],
                "status": row[5]
            }
            for row in cursor.fetchall()
        ]
        return appointments
    finally:
        conn.close()

def get_grooming_services_done(user_id):
    """Retrieve all grooming services with status 'Done' for a specific user."""
    try:
        conn = sqlite3.connect('Systemdb.db')
        cursor = conn.cursor()
        query = """
            SELECT pet_name, service_type, service_date AS date
            FROM grooming_services
            WHERE user_id = ? AND status = 'Done'
            ORDER BY service_date DESC
        """
        cursor.execute(query, (user_id,))
        return [{"pet_name": row[0], "service_type": row[1], "date": row[2]} for row in cursor.fetchall()]
    except sqlite3.Error as e:
        print(f"Database error: {e}")  # Debugging output
        return []
    finally:
        conn.close()
 
def get_daycare_services_done(user_id):
    """Retrieve all daycare services with status 'Done' for a specific user."""
    try:
        conn = sqlite3.connect('Systemdb.db')
        cursor = conn.cursor()
        query = """
            SELECT pet_name, service_type, date, details
            FROM service_history
            WHERE user_id = ? AND service_type = 'Daycare' AND status = 'Done'
            ORDER BY date DESC
        """
        cursor.execute(query, (user_id,))
        return [{"pet_name": row[0], "service_type": row[1], "date": row[2], "details": row[3]} for row in cursor.fetchall()]
    except sqlite3.Error as e:
        print(f"Database error: {e}")  # Debugging output
        return []
    finally:
        conn.close()

def get_service_history(user_id):
    """Retrieve all service history for a specific user."""
    try:
        conn = sqlite3.connect('Systemdb.db')
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, pet_name, service_type, date, details, status
            FROM service_history
            WHERE user_id = ?
            ORDER BY date DESC
        """, (user_id,))
        history = [
            {
                "id": row[0],
                "pet_name": row[1],
                "service_type": row[2],
                "date": row[3],
                "details": row[4],
                "status": row[5]
            }
            for row in cursor.fetchall()
        ]
        return history
    finally:
        conn.close()

def update_service_status(record_id, new_status):
    """Update the status of a service record."""
    try:
        conn = sqlite3.connect('Systemdb.db')
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE service_history
            SET status = ?
            WHERE id = ?
        """, (new_status, record_id))
        conn.commit()
    finally:
        conn.close()

def get_all_service_history():
    """Retrieve all service history for admin view."""
    try:
        conn = sqlite3.connect('Systemdb.db')
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, pet_name, service_type, date, details, status
            FROM service_history
            ORDER BY date DESC
        """)
        history = [
            {
                "id": row[0],
                "pet_name": row[1],
                "service_type": row[2],
                "date": row[3],
                "details": row[4],
                "status": row[5]
            }
            for row in cursor.fetchall()
        ]
        return history
    finally:
        conn.close()
def get_daycare_appointments(username, status=None):
    """Retrieve all daycare appointments for a specific user with optional status filter."""
    try:
        conn = sqlite3.connect('Systemdb.db')
        cursor = conn.cursor()

        # Get user ID from username
        cursor.execute("SELECT id FROM users WHERE username = ?", (username,))
        user = cursor.fetchone()
        if not user:
            return []

        user_id = user[0]

        # Fetch daycare appointments for the user
        query = """
            SELECT id, pet_name, service_type, date, details
            FROM service_history
            WHERE user_id = ? AND service_type = 'Daycare' AND status = 'Pending'
        """
        params = [user_id]
        if status:
            query += " AND status = ?"
            params.append(status)

        cursor.execute(query, params)
        appointments = [
            {"id": row[0], "pet_name": row[1], "service_type": row[2], "date": row[3] , "details": row[4]}
            for row in cursor.fetchall()
        ]
        return appointments
    finally:
        conn.close()


def cancel_daycare_appointment(appointment_id):
    """Cancel a daycare appointment by its ID."""
    try:
        conn = sqlite3.connect('Systemdb.db')
        cursor = conn.cursor()
        cursor.execute("DELETE FROM service_history WHERE id = ?", (appointment_id,))
        conn.commit()
    finally:
        conn.close()
def update_pet_name_in_service_history(user_id, old_name, new_name):
    """Update the pet name in the service history table."""
    try:
        conn = sqlite3.connect('Systemdb.db')
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE service_history
            SET pet_name = ?
            WHERE user_id = ? AND pet_name = ?
        """, (new_name, user_id, old_name))
        conn.commit()
    finally:
        conn.close()
        
def update_pet_name_in_grooming_services(user_id, old_name, new_name):
    """Update the pet name in the grooming services table."""
    try:
        conn = sqlite3.connect('Systemdb.db')
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE grooming_services
            SET pet_name = ?
            WHERE user_id = ? AND pet_name = ?
        """, (new_name, user_id, old_name))
        conn.commit()
    finally:
        conn.close()
        
def update_pet_name_in_daycare_services(user_id, old_name, new_name):
    """Update the pet name in daycare services in the service history table."""
    try:
        conn = sqlite3.connect('Systemdb.db')
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE service_history
            SET pet_name = ?
            WHERE user_id = ? AND pet_name = ? AND service_type = 'Daycare'
        """, (new_name, user_id, old_name))
        conn.commit()
    finally:
        conn.close()
        
def update_grooming_status(appointment_id, new_status):
    """Update the status of a grooming appointment."""
    try:
        conn = sqlite3.connect('Systemdb.db')
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE grooming_services
            SET status = ?
            WHERE id = ?
        """, (new_status, appointment_id))
        conn.commit()
    finally:
        conn.close()

def get_all_daycare_booking():
    """Retrieve all daycare bookings for admin view."""
    try:
        conn = sqlite3.connect('Systemdb.db')
        cursor = conn.cursor()
        cursor.execute("""
            SELECT *
            FROM service_history
            WHERE service_type = 'Daycare'
            ORDER BY date DESC
        """)
        conn.commit()
    finally:
        conn.close()

def get_all_done_services():
    """Retrieve all grooming and daycare services with status 'Done'."""
    try:
        conn = sqlite3.connect('Systemdb.db')
        cursor = conn.cursor()

        # Fetch grooming services with status 'Done'
        cursor.execute("""
            SELECT pet_name, service_type, service_date AS date, NULL AS details
            FROM grooming_services
            WHERE status = 'Done'
        """)
        grooming_services = [
            {"pet_name": row[0], "service_type": row[1], "date": row[2], "details": row[3]}
            for row in cursor.fetchall()
        ]

        # Fetch daycare services with status 'Done'
        cursor.execute("""
            SELECT pet_name, service_type, date, details
            FROM service_history
            WHERE service_type = 'Daycare' AND status = 'Done'
        """)
        daycare_services = [
            {"pet_name": row[0], "service_type": row[1], "date": row[2], "details": row[3]}
            for row in cursor.fetchall()
        ]

        return grooming_services + daycare_services
    finally:
        conn.close()