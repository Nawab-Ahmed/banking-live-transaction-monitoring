# src/create_fact_table.py
import sqlite3
import os

DB_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "db",
    "bank_transactions.db"
)

def create_fact_table():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS fact_transactions (
            transaction_id INTEGER PRIMARY KEY,
            transaction_ts TEXT NOT NULL,
            amount REAL NOT NULL,
            status TEXT CHECK(status IN ('SUCCESS', 'FAILED')),
            channel_id INTEGER,
            customer_id INTEGER,
            response_time_ms INTEGER,
            FOREIGN KEY(channel_id) REFERENCES dim_channel(channel_id),
            FOREIGN KEY(customer_id) REFERENCES dim_customer(customer_id)
        )
    ''')

    conn.commit()
    conn.close()
    print("✅ Fact table created successfully!")

if __name__ == "__main__":
    create_fact_table()
