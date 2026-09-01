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
