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
