# src/ingestion.py
import requests
import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "db", "bank_transactions.db")
API_URL = "http://127.0.0.1:5000/transactions/latest"

def ingest_transactions():
    try:
        response = requests.get(API_URL)
        response.raise_for_status()
        transactions = response.json()
    except Exception as e:
        print(f"Error fetching transactions: {e}")
        return

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Ensure fact table exists
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS fact_transaction (
            transaction_id INTEGER PRIMARY KEY,
            transaction_ts TEXT,
            amount REAL,
            status TEXT CHECK(status IN ('SUCCESS','FAILED')),
            channel_id INTEGER,
            customer_id INTEGER,
            response_time_ms INTEGER,
            FOREIGN KEY(channel_id) REFERENCES dim_channel(channel_id),
            FOREIGN KEY(customer_id) REFERENCES dim_customer(customer_id)
        )
    ''')

    count = 0
    for txn in transactions:
        if txn["amount"] >= 0 and txn["status"] in ["SUCCESS", "FAILED"]:
            cursor.execute('''
                INSERT OR IGNORE INTO fact_transaction
                (transaction_id, transaction_ts, amount, status, channel_id, customer_id, response_time_ms)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (
                txn["transaction_id"],
                txn["transaction_ts"],
                txn["amount"],
                txn["status"],
                txn["channel_id"],
                txn["customer_id"],
                txn["response_time_ms"]
            ))
            count += 1

    conn.commit()
    conn.close()
    print(f"{count} transactions ingested successfully!")

if __name__ == "__main__":
    ingest_transactions()
