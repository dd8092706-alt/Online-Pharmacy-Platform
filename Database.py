import sqlite3
def connect():
    return sqlite3.connect("pharmacy.db")
def setup_database():
    db = connect()
    cur = db.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            email TEXT UNIQUE,
            password TEXT,
            role TEXT
        )
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS medicines (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            category TEXT,
            price REAL,
            stock INTEGER
        )
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            total REAL,
            status TEXT
        )
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS order_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_id INTEGER,
            medicine_id INTEGER,
            quantity INTEGER
        )
    """)
