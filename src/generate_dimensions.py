import sqlite3
import random
import os

# -------------------------------
# Resolve database path safely
# -------------------------------
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "db", "bank_transactions.db")

# Connect to local SQL database
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# -------------------------------
# 1️⃣ Channel Dimension (Static)
# -------------------------------
channels = [
    (1, "ATM"),
    (2, "Mobile App"),
    (3, "Branch"),
    (4, "Internet Banking")
]

cursor.execute("""
CREATE TABLE IF NOT EXISTS dim_channel (
    channel_id INTEGER PRIMARY KEY,
    channel_name TEXT
)
""")

cursor.executemany("""
INSERT OR IGNORE INTO dim_channel (channel_id, channel_name)
VALUES (?, ?)
""", channels)

# -------------------------------
# 2️⃣ Customer Dimension (Pakistani Names)
# -------------------------------
pakistani_names = [
    "Ali Khan",
    "Fatima Ahmed",
    "Hassan Malik",
    "Ayesha Qureshi",
    "Zain Raza",
    "Sara Siddiqui",
    "Bilal Hussain",
    "Mariam Tariq",
    "Owais Shah",
    "Hina Javed"
]

cursor.execute("""
CREATE TABLE IF NOT EXISTS dim_customer (
    customer_id INTEGER PRIMARY KEY,
    customer_name TEXT,
    customer_segment TEXT
)
""")

customers = []
for i, name in enumerate(pakistani_names, start=1001):
    customers.append(
        (i, name, random.choice(["Retail", "SME", "Corporate"]))
    )

cursor.executemany("""
INSERT OR IGNORE INTO dim_customer (customer_id, customer_name, customer_segment)
VALUES (?, ?, ?)
""", customers)

conn.commit()
conn.close()

print("Dimension tables created successfully!")
