# src/create_views.py
import sqlite3
import os

# 1️⃣ Define database path
DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "db", "bank_transactions.db")

# 2️⃣ Connect to database
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# -----------------------------
# 3️⃣ Create Daily KPI View
# Aggregates transactions per day for quick operational insight
# Includes total, average, success rate, failure rate
# -----------------------------
cursor.execute('''
CREATE VIEW IF NOT EXISTS vw_daily_kpis AS
SELECT
    DATE(transaction_ts) AS txn_date,
    COUNT(*) AS total_txns,
    SUM(amount) AS total_amount,
    AVG(amount) AS avg_amount,
    SUM(CASE WHEN status='SUCCESS' THEN 1 ELSE 0 END) * 1.0 / COUNT(*) AS success_rate,
    SUM(CASE WHEN status='FAILED' THEN 1 ELSE 0 END) * 1.0 / COUNT(*) AS failure_rate
FROM fact_transaction
GROUP BY DATE(transaction_ts)
ORDER BY txn_date
''')

# -----------------------------
# 4️⃣ Create Channel Performance View
# Shows channel-wise total transactions, amounts, success/failed counts
# Helps operations understand channel health
# -----------------------------
cursor.execute('''
CREATE VIEW IF NOT EXISTS vw_channel_kpis AS
SELECT
    c.channel_name,
    COUNT(*) AS total_txns,
    SUM(amount) AS total_amount,
    SUM(CASE WHEN status='FAILED' THEN 1 ELSE 0 END) AS failed_txns,
    SUM(CASE WHEN status='SUCCESS' THEN 1 ELSE 0 END) AS success_txns
FROM fact_transaction f
JOIN dim_channel c ON f.channel_id = c.channel_id
GROUP BY c.channel_name
ORDER BY total_txns DESC
''')

# -----------------------------
# 5️⃣ Create Hourly Trend View (Enhanced)
# Shows total, successful, and failed transactions per hour
# This helps to visualize success vs fail per hour
# -----------------------------
cursor.execute('''
CREATE VIEW IF NOT EXISTS vw_hourly_trend AS
SELECT
    STRFTIME('%H', transaction_ts) AS hour,
    COUNT(*) AS total_txns,
    SUM(CASE WHEN status='SUCCESS' THEN 1 ELSE 0 END) AS success_txns,
    SUM(CASE WHEN status='FAILED' THEN 1 ELSE 0 END) AS failed_txns
FROM fact_transaction
GROUP BY STRFTIME('%H', transaction_ts)
ORDER BY hour
''')

# -----------------------------
# 6️⃣ Commit and close
# -----------------------------
conn.commit()
conn.close()

print("✅ All SQL views created successfully!")
