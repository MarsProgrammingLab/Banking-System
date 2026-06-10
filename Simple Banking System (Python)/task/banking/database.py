import sqlite3

DB_NAME = "card.s3db"

def create_connection():
    # Connect to DB (creates database if missing)
    return sqlite3.connect(DB_NAME)

def create_table():
    # Create cursor object
    conn = create_connection()
    cur = conn.cursor()

    # Executes some SQL query
    cur.execute("""CREATE TABLE IF NOT EXISTS card (
    id INTEGER PRIMARY KEY,
    number TEXT,
    pin TEXT,
    balance INTEGER DEFAULT 0
    )
    """)
    conn.commit()
    conn.close()

def insert_account(card_number, pin):
    conn = create_connection()
    cur = conn.cursor()

    cur.execute("""INSERT INTO card(number, pin, balance)
    VALUES (?, ?, 0)""", (card_number, pin))
    conn.commit()
    conn.close()

def add_money(income, card_number):
    conn = create_connection()
    cur = conn.cursor()

    cur.execute("""UPDATE card
    SET balance = balance + ?
    WHERE number = ?
    """, (income, card_number))

    conn.commit()
    conn.close()

def find_account(card_number, pin):
    conn = create_connection()
    cur = conn.cursor()

    cur.execute("""SELECT * from CARD
    WHERE number = ? and pin = ?""",
                (card_number, pin))

    account = cur.fetchone()
    conn.close()

    return account

def get_card_number(card_number):
    conn = create_connection()
    cur = conn.cursor()

    cur.execute("""SELECT * from CARD
    WHERE number = ?""",
                (card_number,))

    account = cur.fetchone()
    conn.close()

    return account

def get_balance(card_number):
    conn = create_connection()
    cur = conn.cursor()

    cur.execute("""
                SELECT balance
                FROM card
                where number = ?
            """, (card_number,))

    balance = cur.fetchone()
    conn.close()

    return balance[0] if balance else None

def get_all_accounts():
    conn = create_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT id, number, pin, balance
        FROM card
    """)

    accounts = cur.fetchall()
    conn.close()

    return accounts

def delete_account(card_number):
    conn = create_connection()
    cur = conn.cursor()

    cur.execute("""DELETE from card
    where number = ? """, (card_number,))

    conn.commit()
    conn.close()

def delete_all_accounts():
    conn = create_connection()
    cur = conn.cursor()

    cur.execute("""DELETE from card""")

    conn.commit()
    conn.close()

def transfer_balance(from_card, to_card, amount):
    conn = create_connection()

    try:
        # Withdraw from sender
        subtract_money(amount, from_card)

        # Deposit to receiver
        add_money(amount, to_card)

        conn.commit()
    except Exception:
        conn.rollback() # reverse changes made to database if exception occurred
        raise

    finally:
        conn.close()


def subtract_money(income, card_number):
    conn = create_connection()
    cur = conn.cursor()

    cur.execute("""UPDATE card
    SET balance = balance - ?
    WHERE number = ?
    """, (income, card_number))

    conn.commit()
    conn.close()