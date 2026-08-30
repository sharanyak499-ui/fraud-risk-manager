import sqlite3
import json
from datetime import datetime
from pathlib import Path


DATABASE = Path(__file__).resolve().parents[2] / "fraud_risk.db"


def get_connection():
    return sqlite3.connect(str(DATABASE))


def create_table():

    connection = get_connection()

    connection.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            transaction_id TEXT UNIQUE,
            user_id TEXT,
            amount REAL,
            risk_score INTEGER,
            risk_level TEXT,
            decision TEXT,
            reasons TEXT,
            ml_result TEXT,
            ml_probability REAL,
            created_at TEXT
        )
    """)

    columns = connection.execute(
        "PRAGMA table_info(transactions)"
    ).fetchall()

    column_names = [column[1] for column in columns]

    if "user_id" not in column_names:
        connection.execute(
            "ALTER TABLE transactions ADD COLUMN user_id TEXT"
        )

    if "created_at" not in column_names:
        connection.execute(
            "ALTER TABLE transactions ADD COLUMN created_at TEXT"
        )

    if "ml_result" not in column_names:
        connection.execute(
            "ALTER TABLE transactions ADD COLUMN ml_result TEXT"
        )

    if "ml_probability" not in column_names:
        connection.execute(
            "ALTER TABLE transactions ADD COLUMN ml_probability REAL"
        )

    connection.commit()
    connection.close()


def transaction_exists(transaction_id):

    connection = get_connection()

    cursor = connection.execute("""
        SELECT 1
        FROM transactions
        WHERE transaction_id = ?
        LIMIT 1
    """, (transaction_id,))

    exists = cursor.fetchone() is not None

    connection.close()

    return exists


def save_transaction(transaction):

    if transaction_exists(transaction["transaction_id"]):
        return False

    connection = get_connection()

    connection.execute("""
        INSERT INTO transactions
        (
            transaction_id,
            user_id,
            amount,
            risk_score,
            risk_level,
            decision,
            reasons,
            ml_result,
            ml_probability,
            created_at
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        transaction["transaction_id"],
        transaction["user_id"],
        transaction["amount"],
        transaction["risk_score"],
        transaction["risk_level"],
        transaction["decision"],
        json.dumps(transaction["reasons"]),
        transaction.get("ml_result"),
        transaction.get("ml_probability"),
        datetime.now().isoformat()
    ))

    connection.commit()
    connection.close()

    return True


def get_transactions():

    connection = get_connection()

    cursor = connection.execute("""
        SELECT
            transaction_id,
            user_id,
            amount,
            risk_score,
            risk_level,
            decision,
            reasons,
            ml_result,
            ml_probability,
            created_at
        FROM transactions
        ORDER BY id DESC
    """)

    rows = cursor.fetchall()

    connection.close()

    transactions = []

    for row in rows:

        transactions.append({
            "transaction_id": row[0],
            "user_id": row[1],
            "amount": row[2],
            "risk_score": row[3],
            "risk_level": row[4],
            "decision": row[5],
            "reasons": json.loads(row[6]),
            "ml_result": row[7],
            "ml_probability": row[8],
            "created_at": row[9]
        })

    return transactions


def get_recent_transactions(minutes=5):

    connection = get_connection()

    cursor = connection.execute("""
        SELECT
            transaction_id,
            user_id,
            amount,
            created_at
        FROM transactions
        WHERE created_at IS NOT NULL
        AND datetime(created_at) >= datetime('now', ?)
        ORDER BY id DESC
    """, (f"-{minutes} minutes",))

    rows = cursor.fetchall()

    connection.close()

    recent = []

    for row in rows:

        recent.append({
            "transaction_id": row[0],
            "user_id": row[1],
            "amount": row[2],
            "created_at": row[3]
        })

    return recent


def get_user_transaction_velocity(user_id, minutes=5):

    connection = get_connection()

    cursor = connection.execute("""
        SELECT COUNT(*)
        FROM transactions
        WHERE user_id = ?
        AND created_at IS NOT NULL
        AND datetime(created_at) >= datetime('now', ?)
    """, (user_id, f"-{minutes} minutes"))

    count = cursor.fetchone()[0]

    connection.close()

    return count


def get_user_average_amount(user_id):

    connection = get_connection()

    cursor = connection.execute("""
        SELECT AVG(amount)
        FROM transactions
        WHERE user_id = ?
    """, (user_id,))

    result = cursor.fetchone()[0]

    connection.close()

    if result is None:
        return 0

    return round(result, 2)