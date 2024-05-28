import sqlite3

def get_db_connection():
    conn = sqlite3.connect('petpulse.db')
    conn.row_factory = sqlite3.Row
    return conn

def create_tables():
    conn = get_db_connection()
    c = conn.cursor()

    # Create the pets table
    c.execute('''CREATE TABLE IF NOT EXISTS pets (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    owner TEXT NOT NULL,
                    vaccination_history TEXT,
                    medical_history TEXT,
                    allergies TEXT,
                    medications TEXT
                )''')

    # Create the reports table
    c.execute('''CREATE TABLE IF NOT EXISTS reports (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    report_name TEXT NOT NULL,
                    report_file TEXT NOT NULL,
                    pet_id INTEGER NOT NULL,
                    date_uploaded TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (pet_id) REFERENCES pets (id)
                )''')

    # Create the appointments table
    c.execute('''CREATE TABLE IF NOT EXISTS appointments (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    pet_id INTEGER NOT NULL,
                    date TIMESTAMP NOT NULL,
                    description TEXT NOT NULL,
                    FOREIGN KEY (pet_id) REFERENCES pets (id)
                )''')

    # Create the emergency_contacts table
    c.execute('''CREATE TABLE IF NOT EXISTS emergency_contacts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    phone TEXT NOT NULL,
                    address TEXT,
                    type TEXT NOT NULL
                )''')

    # Create the insurance_policy table
    c.execute('''CREATE TABLE IF NOT EXISTS insurance_policy (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    description TEXT NOT NULL,
                    coverage TEXT NOT NULL,
                    premium REAL NOT NULL,
                    benefits TEXT NOT NULL
                )''')

    conn.commit()
    conn.close()

def fetch_all_pets():
    conn = get_db_connection()
    pets = conn.execute('SELECT * FROM pets').fetchall()
    conn.close()
    return pets

def fetch_all_policies():
    conn = get_db_connection()
    policies = conn.execute('SELECT * FROM insurance_policy').fetchall()
    conn.close()
    return policies

# Call create_tables() once when you initialize your application
create_tables()
