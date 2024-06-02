import sqlite3

def initialize():
    conn = sqlite3.connect('petpulse/petpulse.db')
    c = conn.cursor()

    # Create the insurance_policy table
    c.execute('''CREATE TABLE IF NOT EXISTS insurance_policy
                 (id INTEGER PRIMARY KEY, name TEXT, description TEXT, coverage TEXT, premium REAL, benefits TEXT)''')

    # Insert initial data into the insurance_policy table
    policies = [
        ("Basic Plan", "Basic coverage for accidents and illnesses.", "Accidents, Illnesses", 1500, "Coverage includes up to ₹50,000 per incident, 80% reimbursement after ₹1000 deductible."),
        ("Premium Plan", "Comprehensive coverage with additional benefits.", "Accidents, Illnesses, Wellness", 2500, "Coverage includes up to ₹1,00,000 per incident, 90% reimbursement after ₹500 deductible, annual wellness exam."),
        ("Ultimate Plan", "All-inclusive coverage with maximum benefits.", "Accidents, Illnesses, Wellness, Surgery", 3500, "Coverage includes unlimited incident coverage, 100% reimbursement after ₹0 deductible, annual wellness exam, surgery coverage up to ₹2,00,000."),
        ("Standard Plan", "Standard coverage for common pet health issues.", "Common illnesses, Minor injuries", 2000, "Coverage includes up to ₹70,000 per incident, 85% reimbursement after ₹750 deductible."),
        ("Advanced Plan", "Advanced coverage for major health concerns.", "Major illnesses, Major injuries, Surgery", 3000, "Coverage includes up to ₹1,50,000 per incident, 90% reimbursement after ₹1000 deductible."),
        ("Family Plan", "Coverage for multiple pets in one household.", "Accidents, Illnesses, Routine care", 5000, "Coverage includes up to ₹2,00,000 per incident, 80% reimbursement after ₹1500 deductible, covers up to 3 pets."),
        ("Wellness Plan", "Focuses on preventative care and routine check-ups.", "Routine check-ups, Vaccinations, Wellness exams", 1000, "Coverage includes up to ₹20,000 per year, 100% reimbursement after ₹200 deductible.")
    ]


    c.executemany('INSERT INTO insurance_policy (name, description, coverage, premium, benefits) VALUES (?, ?, ?, ?, ?)', policies)

    # Create the pets table
    c.execute('''CREATE TABLE IF NOT EXISTS pets (
                    id INTEGER PRIMARY KEY,
                    name TEXT NOT NULL,
                    owner TEXT NOT NULL,
                    medical_history TEXT,
                    vaccination_history TEXT,
                    allergies TEXT,
                    medications TEXT
                )''')

    conn.commit()
    conn.close()

if __name__ == "__main__":
    initialize()
