import sqlite3
import json

DATABASE = "fraud_risk.db"


def get_connection():
    return sqlite3.connect(DATABASE)


def create_table():
    connection = get_connection()

    connection.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            transaction_id TEXT,
            amount REAL,
            risk_score INTEGER,
            risk_level TEXT,
            decision TEXT,
            reasons TEXT
        )
    """)

    connection.commit()
    connection.close()


def save_transaction(transaction):
    connection = get_connection()

    connection.execute("""
        INSERT INTO transactions
        (transaction_id, amount, risk_score, risk_level, decision, reasons)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        transaction["transaction_id"],
        transaction["amount"],
        transaction["risk_score"],
        transaction["risk_level"],
        transaction["decision"],
        json.dumps(transaction["reasons"])
    ))

    connection.commit()
    connection.close()


def get_transactions():
    connection = get_connection()

    cursor = connection.execute("""
        SELECT transaction_id, amount, risk_score,
               risk_level, decision, reasons
        FROM transactions
        ORDER BY id DESC
    """)

    rows = cursor.fetchall()
    connection.close()

    transactions = []

    for row in rows:
        transactions.append({
            "transaction_id": row[0],
            "amount": row[1],
            "risk_score": row[2],
            "risk_level": row[3],
            "decision": row[4],
            "reasons": json.loads(row[5])
        })

    return transactions