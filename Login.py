import sqlite3
from database import connect, hash_password
def register(name, email, password):
    if not name or not email or not password:
        return False
    db = connect()
    try:
        db.execute("""
            INSERT INTO users
            (name, email, password, role)
            VALUES (?, ?, ?, ?)
        """, (
            name.strip(),
            email.strip().lower(),
            hash_password(password),
            "customer"
        ))
        db.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    except Exception:
        return False
    finally:
        db.close()
def login(email, password):
    db = connect()
    row = db.execute("""
        SELECT id, name, email, role
        FROM users
        WHERE email = ?
        AND password = ?
    """, (
        email.strip().lower(),
        hash_password(password)
    )).fetchone()
    db.close()
    if row:
        return dict(row)
    return None
def get_all_users():
    db = connect()
    rows = db.execute("""
        SELECT id, name, email, role
        FROM users
        ORDER BY id DESC
    """).fetchall()
    db.close()
    return [dict(row) for row in rows]
