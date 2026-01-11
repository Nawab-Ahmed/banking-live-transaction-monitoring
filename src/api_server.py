# src/api_server.py
from flask import Flask, jsonify
from datetime import datetime
import random
import sqlite3
import os

app = Flask(__name__)

# Load customer and channel IDs from DB
DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "db", "bank_transactions.db")
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()
cursor.execute("SELECT customer_id FROM dim_customer")
CUSTOMER_IDS = [row[0] for row in cursor.fetchall()]
cursor.execute("SELECT channel_id FROM dim_channel")
CHANNEL_IDS = [row[0] for row in cursor.fetchall()]
conn.close()

def generate_transaction():
    return {
        "transaction_id": random.randint(1000000, 9999999),
        "transaction_ts": datetime.now().isoformat(),
        "amount": round(random.uniform(50, 5000), 2),
        "status": random.choices(["SUCCESS", "FAILED"], weights=[90, 10])[0],
        "channel_id": random.choice(CHANNEL_IDS),
        "customer_id": random.choice(CUSTOMER_IDS),
        "response_time_ms": random.randint(100, 500)
    }

@app.route("/transactions/latest", methods=["GET"])
def get_transactions():
    # Generate 10–50 transactions per API call
    transactions = [generate_transaction() for _ in range(random.randint(10, 50))]
    return jsonify(transactions)

if __name__ == "__main__":
    app.run(port=5000)
