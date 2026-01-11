import sqlite3
import os

# Correct DB path relative to this script file
DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "db", "bank_transactions.db")

def run_quality_checks():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    print("1️⃣ NULL Check")
    cursor.execute("""
        SELECT COUNT(*) FROM fact_transaction 
        WHERE transaction_id IS NULL 
        OR transaction_ts IS NULL 
        OR amount IS NULL
    """)
    print("NULLs in critical columns:", cursor.fetchone()[0])

    print("\n2️⃣ Negative Amounts")
    cursor.execute("SELECT COUNT(*) FROM fact_transaction WHERE amount < 0")
    print("Negative amounts:", cursor.fetchone()[0])

    print("\n3️⃣ Invalid Status")
    cursor.execute("SELECT COUNT(*) FROM fact_transaction WHERE status NOT IN ('SUCCESS','FAILED')")
    print("Invalid status count:", cursor.fetchone()[0])

    print("\n4️⃣ Duplicate Transaction IDs")
    cursor.execute("""
        SELECT COUNT(*) FROM (
            SELECT transaction_id FROM fact_transaction
            GROUP BY transaction_id
            HAVING COUNT(*) > 1
        )
    """)
    print("Duplicate transaction IDs:", cursor.fetchone()[0])

    print("\n5️⃣ Invalid Foreign Keys")
    cursor.execute("""
        SELECT COUNT(*) FROM fact_transaction
        WHERE channel_id NOT IN (SELECT channel_id FROM dim_channel)
        OR customer_id NOT IN (SELECT customer_id FROM dim_customer)
    """)
    print("Invalid foreign keys:", cursor.fetchone()[0])

    conn.close()
    print("\n✅ Data Quality Check Completed!")

if __name__ == "__main__":
    run_quality_checks()
