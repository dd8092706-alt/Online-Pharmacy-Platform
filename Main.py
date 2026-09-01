from nicegui import ui
import sqlite3
import hashlib
DB = "pharmacy.db"
def db():
    return sqlite3.connect(DB)
def setup():
    con = db()
    cur = con.cursor()
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
            stock INTEGER,
            image TEXT
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

    admin = cur.execute(
        "SELECT id FROM users WHERE email=?",
        ("admin@pharmacy.com",)
    ).fetchone()
    if admin is None:
        cur.execute(
            """
            INSERT INTO users
            (name,email,password,role)
            VALUES (?,?,?,?)
            """,
            (
                "Admin",
                "admin@pharmacy.com",
                hashlib.sha256("admin123".encode()).hexdigest(),
                "admin"
            )
        )
    count = cur.execute(
        "SELECT COUNT(*) FROM medicines"
    ).fetchone()[0]
    if count == 0:
        products = [
            (
                "Paracetamol 500mg",
                "Pain Relief",
                25,
                100,
                "https://images.unsplash.com/photo-1584308666744-24d5c474f2ae"
            ),
            (
                "Vitamin C",
                "Vitamins",
                120,
                80,
                "https://images.unsplash.com/photo-1550572017-edd951aa8ca2"
            ),
            (
                "Cetirizine",
                "Allergy",
                45,
                70,
                "https://images.unsplash.com/photo-1587854692152-cbe660dbde88"
            ),
            (
                "Cough Syrup",
                "Cold and Cough",
                95,
                60,
                "https://images.unsplash.com/photo-1603398938378-e54eab446dde"
            ),
            (
                "Multivitamin",
                "Vitamins",
                180,
                50,
                "https://images.unsplash.com/photo-1550572017-edd951aa8ca2"
            ),
            (
                "First Aid Cream",
                "First Aid",
                85,
                40,
                "https://images.unsplash.com/photo-1603398938378-e54eab446dde"
            )
        ]
        cur.executemany(
            """
            INSERT INTO medicines
            (name,category,price,stock,image)
            VALUES (?,?,?,?,?)
            """,
            products
        )
    con.commit()
    con.close()
def password_hash(password):
    return hashlib.sha256(
        password.encode()
    ).hexdigest()
def login_user(email, password):
    con = db()
    user = con.execute(
        """
        SELECT id,name,email,role
        FROM users
        WHERE email=? AND password=?
        """,
        (
            email.lower(),
            password_hash(password)
        )
    ).fetchone()
    con.close()
    return user
def register_user(name, email, password):
    try:
        con = db()
        con.execute(
            """
            INSERT INTO users
            (name,email,password,role)
            VALUES (?,?,?,?)
            """,
            (
                name,
                email.lower(),
                password_hash(password),
                "customer"
            )
        )
        con.commit()
        con.close()
        return True
    except sqlite3.IntegrityError:
        return False
setup()
@ui.page("/")
def home():
    login_page()
@ui.page("/register")
def register_page():
    with ui.column().classes(
        "w-full min-h-screen items-center justify-center bg-blue-50"
    ):
        with ui.card().classes("w-96 p-8 shadow-xl"):
            ui.label(
                "MediCare Pharmacy"
            ).classes(
                "text-3xl font-bold text-blue-700"
            )
            ui.label(
                "Create Customer Account"
            ).classes("text-xl")
            name = ui.input(
                "Full Name"
            ).classes("w-full")
            email = ui.input(
                "Email"
            ).classes("w-full")
            password = ui.input(
                "Password",
                password=True
            ).classes("w-full")
            def create_account():
                if register_user(
                    name.value,
                    email.value,
                    password.value
                ):
                    ui.notify(
                        "Account created successfully"
                    )
                    ui.navigate.to("/")
                else:
                    ui.notify(
                        "Email already exists",
                        type="negative"
                    )
            ui.button(
                "Register",
                on_click=create_account
            ).classes(
                "w-full bg-blue-700 text-white"
            )
            ui.button(
                "Back to Login",
                on_click=lambda: ui.navigate.to("/")
            ).classes("w-full")
def login_page():
    with ui.column().classes(
        "w-full min-h-screen items-center justify-center bg-blue-50"
    ):
        with ui.card().classes(
            "w-96 p-8 shadow-xl"
        ):
            ui.label(
                "MediCare Pharmacy"
            ).classes(
                "text-4xl font-bold text-blue-700"
            )
            ui.label(
                "Online Pharmacy Platform"
            ).classes(
                "text-lg text-gray-600"
            )
            email = ui.input(
                "Email"
            ).classes("w-full")
            password = ui.input(
                "Password",
                password=True
            ).classes("w-full")
            def do_login():
                user = login_user(
                    email.value,
                    password.value
                )
                if user:
                    if user[3] == "admin":
                        ui.navigate.to("/admin")
                    else:
                        ui.navigate.to("/customer")
                else:
                    ui.notify(
                        "Invalid email or password",
                        type="negative"
                    )
            ui.button(
                "LOGIN",
                on_click=do_login
            ).classes(
                "w-full bg-blue-700 text-white"
            )
            ui.button(
                "CREATE ACCOUNT",
                on_click=lambda: ui.navigate.to(
                    "/register"
                )
            ).classes("w-full")
            ui.separator()
            ui.label("Admin Login").classes(
                "font-bold"
            )
            ui.label("admin@pharmacy.com")
            ui.label("Password: admin123")
@ui.page("/customer")
def customer_page():
    with ui.column().classes(
        "w-full min-h-screen bg-gray-100 p-8"
    ):
        ui.label(
            "MediCare Pharmacy"
        ).classes(
            "text-4xl font-bold text-blue-700"
        )
        ui.label(
            "Customer Dashboard"
        ).classes(
            "text-2xl font-bold"
        )
        with ui.row().classes("gap-6 mt-8"):
            with ui.card().classes("w-72 p-6"):
                ui.label(
                    "Medicine Store"
                ).classes(
                    "text-xl font-bold"
                )
                ui.label(
                    "Search and purchase medicines."
                )
                ui.button(
                    "Browse Medicines",
                    on_click=lambda: ui.navigate.to(
                        "/medicines"
                    )
                )
            with ui.card().classes("w-72 p-6"):
                ui.label(
                    "My Orders"
                ).classes(
                    "text-xl font-bold"
                )
                ui.button(
                    "View Orders",
                    on_click=lambda: ui.navigate.to(
                        "/orders"
                    )
                )
@ui.page("/medicines")
def medicines_page():
    with ui.column().classes(
        "w-full min-h-screen bg-gray-100 p-8"
    ):
        ui.label(
            "Medicine Store"
        ).classes(
            "text-4xl font-bold text-blue-700"
        )
        search = ui.input(
            "Search medicine or category"
        ).classes("w-full max-w-xl")

        products = ui.row().classes(
            "w-full flex-wrap gap-6 mt-6"
        )
        def show_products():
            products.clear()
            con = db()
            if search.value:
                rows = con.execute(
                    """
                    SELECT * FROM medicines
                    WHERE name LIKE ?
                    OR category LIKE ?
                    """,
                    (
                        "%" + search.value + "%",
                        "%" + search.value + "%"
                    )
                ).fetchall()
            else:
                rows = con.execute(
                    "SELECT * FROM medicines"
                ).fetchall()
            con.close()
            with products:
                for product in rows:
                    with ui.card().classes(
                        "w-72 p-4 shadow-xl"
                    ):
                        ui.image(
                            product[5]
                        ).classes(
                            "w-full h-40 object-cover rounded-lg"
                        )

                        ui.label(
                            product[1]
                        ).classes(
                            "text-xl font-bold"
                        )
                        ui.label(
                            product[2]
                        ).classes(
                            "text-blue-600"
                        )
                        ui.label(
                            "₹" + str(product[3])
                        ).classes(
                            "text-xl font-bold text-green-700"
                        )
                        ui.label(
                            "Stock: " + str(product[4])
                        )
                        ui.button(
                            "Add to Cart"
                        ).classes(
                            "w-full bg-blue-700 text-white"
                        )
        ui.button(
            "SEARCH",
            on_click=show_products
        )
        show_products()
        ui.button(
            "Back",
            on_click=lambda: ui.navigate.to(
                "/customer"
            )
        )
@ui.page("/orders")
def orders_page():
    with ui.column().classes(
        "w-full min-h-screen bg-gray-100 p-8"
    ):
        ui.label(
            "My Orders"
        ).classes(
            "text-3xl font-bold text-blue-700"
        )
        ui.label(
            "No orders placed yet."
        ).classes(
            "text-xl text-gray-600"
        )
        ui.button(
            "Browse Medicines",
            on_click=lambda: ui.navigate.to(
                "/medicines"
            )
        )
@ui.page("/admin")
def admin_page():
    with ui.column().classes(
        "w-full min-h-screen bg-gray-100 p-8"
    ):
        ui.label(
            "MediCare Admin Dashboard"
        ).classes(
            "text-4xl font-bold text-blue-700"
        )
        ui.label(
            "Administrator Panel"
        ).classes("text-xl")
        with ui.row().classes("gap-6 mt-8"):
            with ui.card().classes("w-72 p-6"):
                ui.label(
                    "Medicine Management"
                ).classes(
                    "text-xl font-bold"
                )
                ui.button(
                    "Manage Medicines",
                    on_click=lambda: ui.navigate.to(
                        "/admin/medicines"
                    )
                )
            with ui.card().classes("w-72 p-6"):
                ui.label(
                    "Customer Orders"
                ).classes(
                    "text-xl font-bold"
                )
                ui.button(
                    "View Orders",
                    on_click=lambda: ui.navigate.to(
                        "/admin/orders"
                    )
                )
@ui.page("/admin/medicines")
def admin_medicines():
    with ui.column().classes(
        "w-full min-h-screen bg-gray-100 p-8"
    ):
        ui.label(
            "Medicine Management"
        ).classes(
            "text-3xl font-bold text-blue-700"
        )
        name = ui.input(
            "Medicine Name"
        )
        category = ui.input(
            "Category"
        )
        price = ui.number(
            "Price"
        )
        stock = ui.number(
            "Stock"
        )
        image = ui.input(
            "Product Image URL"
        )
        def save():
            con = db()
            con.execute(
                """
                INSERT INTO medicines
                (name,category,price,stock,image)
                VALUES (?,?,?,?,?)
                """,
                (
                    name.value,
                    category.value,
                    price.value,
                    stock.value,
                    image.value
                )
            )
            con.commit()
            con.close()
            ui.notify(
                "Medicine added successfully"
            )
        ui.button(
            "ADD MEDICINE",
            on_click=save
        )
        ui.label(
            "Existing Products"
        ).classes(
            "text-2xl font-bold mt-8"
        )
        con = db()
        rows = con.execute(
            "SELECT name,category,price,stock FROM medicines"
        ).fetchall()
        con.close()
        for product in rows:
            ui.label(
                product[0] +
                " | " +
                product[1] +
                " | ₹" +
                str(product[2]) +
                " | Stock: " +
                str(product[3])
            )
@ui.page("/admin/orders")
def admin_orders():
    with ui.column().classes(
        "w-full min-h-screen bg-gray-100 p-8"
    ):
        ui.label(
            "Customer Orders"
        ).classes(
            "text-3xl font-bold text-blue-700"
        )
        con = db()
        rows = con.execute(
            "SELECT * FROM orders"
        ).fetchall()
        con.close()
        if not rows:
            ui.label(
                "No customer orders yet."
            )
ui.run(
    host="127.0.0.1",
    port=8081,
    title="MediCare Online Pharmacy",
    reload=False
)
