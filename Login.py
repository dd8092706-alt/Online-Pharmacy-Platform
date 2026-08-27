from database import connect
def register(name, email, password):
    db = connect()
    try:
        db.execute(
            "INSERT INTO users (name,email,password,role) VALUES (?,?,?,?)",
            (name, email, password, "customer")
        )
        db.commit()
        return True
    except:
        return False
    finally:
        db.close()
        def login(email, password):
    db = connect()
    cur = db.cursor()
    cur.execute(
        "SELECT id,name,email,role FROM users WHERE email=? AND password=?",
        (email, password)
    )
    row = cur.fetchone()
    db.close()
    if row:
        return {
            "id": row[0],
            "name": row[1],
            "email": row[2],
            "role": row[3]
        }
    return None
