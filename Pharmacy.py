from database import connect
def medicines(search=""):
    db = connect()
    cur = db.cursor()
    if search:
        cur.execute(
            "SELECT * FROM medicines WHERE name LIKE ?",
            ("%" + search + "%",)
        )
    else:
        cur.execute("SELECT * FROM medicines")
    rows = cur.fetchall()
    db.close()
    return [
        {
            "id": r[0],
            "name": r[1],
            "category": r[2],
            "price": r[3],
            "stock": r[4]
        }
        for r in rows
    ]
def add_medicine(name, category, price, stock):
    db = connect()
    db.execute(
        "INSERT INTO medicines (name,category,price,stock) VALUES (?,?,?,?)",
        (name, category, price, stock)
    )
    db.commit()
    db.close()

def place_order(user_id, cart):
    db = connect()
    cur = db.cursor()
    total = 0
    for medicine_id, quantity in cart.items():
        cur.execute(
            "SELECT price,stock FROM medicines WHERE id=?",
            (medicine_id,)
        )
        row = cur.fetchone()
        if not row or row[1] < quantity:
            db.close()
            return False
        total += row[0] * quantity
