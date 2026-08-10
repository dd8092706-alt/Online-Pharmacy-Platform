# Online-Pharmacy-Platform
from flask import Flask
import sqlite3
app = Flask(__name__)
def create_database():
    conn = sqlite3.connect("pharmacy.db")
    conn.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            category TEXT,
            price REAL,
            stock INTEGER
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer TEXT,
            address TEXT,
            total REAL
        )
    """)
    count = conn.execute(
        "SELECT COUNT(*) FROM products"
    ).fetchone()[0]
    if count == 0:
        products = [
            ("Paracetamol", "Pain Relief", 25, 50),
            ("Vitamin C", "Vitamins", 80, 30),
            ("Cough Syrup", "Cold and Cough", 120, 20),
            ("First Aid Kit", "First Aid", 250, 15),
            ("Antiseptic Cream", "First Aid", 65, 25),
            ("Digital Thermometer", "Healthcare Device", 180, 10)
        ]
        conn.executemany(
            """
            INSERT INTO products
            (name, category, price, stock)
            VALUES (?, ?, ?, ?)
            """,
            products
        )
    conn.commit()
    conn.close()
@app.route("/")
def home():
    conn = sqlite3.connect("pharmacy.db")
    conn.row_factory = sqlite3.Row
    products = conn.execute(
        "SELECT * FROM products"
    ).fetchall()
    conn.close()
    html = """
    <html>
    <head>
        <title>Online Pharmacy</title>
        <style>
            body {
                font-family: Arial;
                margin: 0;
                background: #f2f7f8;
            }
            header {
                background: #167d8d;
                color: white;
                padding: 20px;
                text-align: center;
            }
            .container {
                width: 85%;
                margin: 30px auto;
            }
            .products {
                display: grid;
                grid-template-columns:
                repeat(auto-fit, minmax(220px, 1fr));
                gap: 20px;
            }
            .card {
                background: white;
                padding: 20px;
                text-align: center;
                border-radius: 10px;
                box-shadow: 0 2px 8px #bbb;
            }
        </style>
    </head>
    <body>
        <header>
            <h1>Online Pharmacy Ordering Platform</h1>
            <p>Simple and convenient healthcare product ordering</p>
        </header>
        <div class="container">
            <h2>Available Products</h2>
            <div class="products">
    """
    for product in products:
        html += f"""
        <div class="card">
            <h3>{product["name"]}</h3>
            <p>Category: {product["category"]}</p>
            <p>Price: ₹{product["price"]:.2f}</p>
            <p>Stock: {product["stock"]}</p>
        </div>
        """
    html += """
            </div>
        </div>
    </body>
    </html>
    """
    return html
if __name__ == "__main__":
    create_database()
    app.run(debug=True)
@app.route("/checkout", methods=["GET", "POST"])
def checkout():
    cart = session.get("cart", [])
    if not cart:
        return redirect("/")
    conn = sqlite3.connect("pharmacy.db")
    conn.row_factory = sqlite3.Row
    total = 0
    for product_id in cart:
        product = conn.execute(
            "SELECT * FROM products WHERE id = ?",
            (product_id,)
        ).fetchone()
        if product:
            total += product["price"]
    if request.method == "POST":
        customer = request.form["customer"]
        address = request.form["address"]
        conn.execute(
            """
            INSERT INTO orders
            (customer, address, total)
            VALUES (?, ?, ?)
            """,
            (customer, address, total)
        )
        for product_id in cart:
            conn.execute(
                """
                UPDATE products
                SET stock = stock - 1
                WHERE id = ? AND stock > 0
                """,
                (product_id,)
            )
        conn.commit()
        conn.close()
        session["cart"] = []
        return f"""
        <h1>Order Placed Successfully!</h1>
        <h2>Thank you, {customer}</h2>
        <p>Order Total: ₹{total:.2f}</p>
        <a href="/">Back to Home</a>
        <br><br>
        <a href="/orders">View Orders</a>
        """
    conn.close()
    return f"""
    <html>
    <body>
        <h1>Checkout</h1>
        <h2>Total Amount: ₹{total:.2f}</h2>
        <form method="POST">
            <label>Customer Name</label><br>
            <input type="text" name="customer" required>
            <br><br>
            <label>Delivery Address</label><br>
            <textarea name="address" required></textarea>
            <br><br>
            <button type="submit">
                Place Order
            </button>
        </form>
    </body>
    </html>
    """
@app.route("/orders")
def orders():
    conn = sqlite3.connect("pharmacy.db")
    conn.row_factory = sqlite3.Row
    orders = conn.execute(
        "SELECT * FROM orders ORDER BY id DESC"
    ).fetchall()
    conn.close()
    html = """
    <html>
    <body>
        <h1>Order History</h1>
    """
    if orders:
        for order in orders:
            html += f"""
            <div>
                <h2>Order #{order["id"]}</h2>
                <p>Customer: {order["customer"]}</p>
                <p>Address: {order["address"]}</p>
                <p>Total: ₹{order["total"]:.2f}</p>
                <hr>
            </div>
            """
    else:
        html += """
        <p>No orders have been placed yet.</p>
        """
    html += """
        <a href="/">Back to Home</a>
    </body>
    </html>
    """
    return html
@app.route("/checkout", methods=["GET", "POST"])
def checkout():
    cart = session.get("cart", [])
    if not cart:
        return redirect("/")
    conn = sqlite3.connect("pharmacy.db")
    conn.row_factory = sqlite3.Row
    total = 0
    for product_id in cart:
        product = conn.execute(
            "SELECT * FROM products WHERE id = ?",
            (product_id,)
        ).fetchone()
        if product:
            total += product["price"]
    if request.method == "POST":
        customer = request.form["customer"]
        address = request.form["address"]
        conn.execute(
            """
            INSERT INTO orders
            (customer, address, total)
            VALUES (?, ?, ?)
            """,
            (customer, address, total)
        )
        for product_id in cart:
            conn.execute(
                """
                UPDATE products
                SET stock = stock - 1
                WHERE id = ? AND stock > 0
                """,
                (product_id,)
            )
        conn.commit()
        conn.close()
        session["cart"] = []
        return f"""
        <h1>Order Placed Successfully!</h1>
        <h2>Thank you, {customer}</h2>
        <p>Order Total: ₹{total:.2f}</p>
        <a href="/">Back to Home</a>
        <br><br>
        <a href="/orders">View Orders</a>
        """
    conn.close()
    return f"""
    <html>
    <body>
        <h1>Checkout</h1>
        <h2>Total Amount: ₹{total:.2f}</h2>
        <form method="POST">
            <label>Customer Name</label><br>
            <input type="text" name="customer" required>
            <br><br>
            <label>Delivery Address</label><br>
            <textarea name="address" required></textarea>
            <br><br>
            <button type="submit">
                Place Order
            </button>
        </form>
    </body>
    </html>
    """
@app.route("/orders")
def orders():
    conn = sqlite3.connect("pharmacy.db")
    conn.row_factory = sqlite3.Row
    orders = conn.execute(
        "SELECT * FROM orders ORDER BY id DESC"
    ).fetchall()
    conn.close()
    html = """
    <html>
    <body>
        <h1>Order History</h1>
    """
    if orders:
        for order in orders:
            html += f"""
            <div>
                <h2>Order #{order["id"]}</h2>
                <p>Customer: {order["customer"]}</p>
                <p>Address: {order["address"]}</p>
                <p>Total: ₹{order["total"]:.2f}</p>
                <hr>
            </div>
            """
    else:
        html += """
        <p>No orders have been placed yet.</p>
        """
    html += """
        <a href="/">Back to Home</a>
    </body>
    </html>
    """
    return html
