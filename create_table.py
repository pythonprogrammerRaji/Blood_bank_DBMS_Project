import sqlite3

# Connect to the database file
conn = sqlite3.connect('database.db')
cursor = conn.cursor()

# Drop old table if it exists (cleans old structure)
cursor.execute("DROP TABLE IF EXISTS donor")

# Create new donor table with correct structure
cursor.execute('''
CREATE TABLE donor (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    age INTEGER NOT NULL,
    gender TEXT NOT NULL,
    blood_group TEXT NOT NULL,
    weight INTEGER NOT NULL,
    last_donation TEXT,
    phone TEXT NOT NULL,
    address TEXT NOT NULL
)
''')

# Insert one sample donor
cursor.execute('''
INSERT INTO donor (name, age, gender, blood_group, weight, last_donation, phone, address)
VALUES (?, ?, ?, ?, ?, ?, ?, ?)
''', ("Rajeshwari", 22, "Female", "A+", 55, "2025-06-01", "9876543210", "Bangalore"))

conn.commit()
conn.close()

print("✅ Donor table created with ID and sample donor added.")