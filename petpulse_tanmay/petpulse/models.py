import sqlite3

def get_db_connection():
    conn = sqlite3.connect('petpulse_tanmay/petpulse/petpulse.db')
    conn.row_factory = sqlite3.Row
    return conn

def create_tables():
    conn = get_db_connection()
    c = conn.cursor()

    # Create the pets table
    c.execute('''CREATE TABLE IF NOT EXISTS pets (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    animal TEXT NOT NULL,
                    age TEXT,
                    allergies TEXT
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

    # Create the pet_insurance table
    c.execute('''CREATE TABLE IF NOT EXISTS pet_insurance (
                    pet_id INTEGER NOT NULL,
                    policy_id INTEGER NOT NULL,
                    PRIMARY KEY (pet_id, policy_id),
                    FOREIGN KEY (pet_id) REFERENCES pets (id),
                    FOREIGN KEY (policy_id) REFERENCES insurance_policy (id)
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

def add_pet_policy(pet_id, policy_id):
    conn = get_db_connection()
    conn.execute('INSERT INTO pet_insurance (pet_id, policy_id) VALUES (?, ?)', (pet_id, policy_id))
    conn.commit()
    conn.close()

def fetch_appointments():
    conn = get_db_connection()
    appointments = conn.execute('SELECT * FROM appointments ').fetchall()
    conn.close()
    return appointments


def fetch_pet_policies(pet_id):
    conn = get_db_connection()
    policies = conn.execute('''
        SELECT ip.* FROM insurance_policy ip
        JOIN pet_insurance pi ON ip.id = pi.policy_id
        WHERE pi.pet_id = ?
    ''', (pet_id,)).fetchall()
    conn.close()
    return policies

def fetch_pet_insurance():
    conn = get_db_connection()
    pet_ins = conn.execute('SELECT * FROM pet_insurance').fetchall()
    conn.close()
    return pet_ins

def fetch_report():
    conn = get_db_connection()
    report = conn.execute('SELECT * FROM reports').fetchall()
    conn.close()
    return report

# Call create_tables() once when you initialize your application
create_tables()
