#Online Pharmacy Platform
#main.py
from nicegui import ui
from database import setup_database
from login import register, login
from pharmacy import (
    medicines,
    add_medicine,
    place_order,
    customer_orders,
    all_orders
)
setup_database()
current_user = None
cart = {}
page = ui.column().classes("w-full items-center")
def clear_page():
    page.clear()
def login_screen():
    clear_page()
    with page:
        ui.label("Online Pharmacy").classes("text-3xl font-bold")
        email = ui.input("Email").classes("w-80")
        password = ui.input("Password", password=True).classes("w-80")
        def do_login():
            global current_user
            user = login(
                email.value,
                password.value
            )
            if user:
                current_user = user
                if user["role"] == "admin":
                    admin_screen()
                else:
                    customer_screen()
            else:
                ui.notify(
                    "Invalid email or password",
                    type="negative"
                )
        ui.button(
            "Login",
            on_click=do_login
        )
        ui.button(
            "Create Account",
            on_click=register_screen
        )
def register_screen():
    clear_page()
    with page:
        ui.label("Create Customer Account").classes(
            "text-3xl font-bold"
        )
        name = ui.input("Name").classes("w-80")
        email = ui.input("Email").classes("w-80")
        password = ui.input(
            "Password",
            password=True
        ).classes("w-80")
        def save():
            if register(
                name.value,
                email.value,
                password.value
            ):
                ui.notify("Account created successfully")
                login_screen()
            else:
                ui.notify(
                    "Email already exists",
                    type="negative"
                )
        ui.button(
            "Register",
            on_click=save
        )
        ui.button(
            "Back",
            on_click=login_screen
        )
def customer_screen():
    clear_page()
    with page:
        ui.label("Customer Dashboard").classes(
            "text-3xl font-bold"
        )
        ui.label(
            "Welcome " + current_user["name"]
        ).classes("text-xl")
        ui.button(
            "Browse Medicines",
            on_click=medicine_screen
        )
        ui.button(
            "View Cart",
            on_click=cart_screen
        )
        ui.button(
            "My Orders",
            on_click=orders_screen
        )
        ui.button(
            "Logout",
            on_click=login_screen
        )
def medicine_screen():
    clear_page()
    with page:
        ui.label("Available Medicines").classes(
            "text-3xl font-bold"
        )
        search = ui.input("Search Medicine")
        medicines_area = ui.column()
        def load_medicines():
            medicines_area.clear()
            with medicines_area:
                for medicine in medicines(search.value or ""):
                    with ui.row().classes("items-center"):
                        ui.label(
                            f'{medicine["name"]} | '
                            f'{medicine["category"]} | '
                            f'₹{medicine["price"]} | '
                            f'Stock: {medicine["stock"]}'
                        )
                        ui.button(
                            "Add",
                            on_click=lambda m=medicine:
                            add_cart(m["id"])
                        )
        ui.button(
            "Search",
            on_click=load_medicines
        )
        load_medicines()
        ui.button(
            "Back",
            on_click=customer_screen
        )
        def add_cart(medicine_id):
    cart[medicine_id] = cart.get(
        medicine_id,
        0
    ) + 1
    ui.notify("Medicine added to cart")
def cart_screen():
    clear_page()
    with page:
        ui.label("Shopping Cart").classes(
            "text-3xl font-bold"
        )
        if not cart:
            ui.label("Cart is empty")
        else:
            total = 0
            for medicine_id, quantity in cart.items():
                for medicine in medicines():
                    if medicine["id"] == medicine_id:
                        amount = (
                            medicine["price"] *
                            quantity
                        )
                        total += amount
                        ui.label(
                            f'{medicine["name"]} x '
                            f'{quantity} = ₹{amount}'
                        )
            ui.label(
                f"Total: ₹{total}"
            ).classes("text-xl font-bold")
            def checkout():
                if place_order(
                    current_user["id"],
                    cart
                ):
                    cart.clear()
                    ui.notify(
                        "Order placed successfully"
                    )
                    customer_screen()
                else:
                    ui.notify(
                        "Insufficient stock",
                        type="negative"
                    )
            ui.button(
                "Place Order",
                on_click=checkout
            )
        ui.button(
            "Back",
            on_click=customer_screen
        )
def orders_screen():
    clear_page()
    with page:
        ui.label("My Orders").classes(
            "text-3xl font-bold"
        )
        orders = customer_orders(
            current_user["id"]
        )
        if not orders:
            ui.label("No orders found")
        for order in orders:
            ui.label(
                f'Order {order["id"]} | '
                f'Total: ₹{order["total"]} | '
                f'Status: {order["status"]}'
            )
        ui.button(
            "Back",
            on_click=customer_screen
        )
def admin_screen():
    clear_page()
    with page:
        ui.label("Admin Dashboard").classes(
            "text-3xl font-bold"
        )
        ui.button(
            "Manage Medicines",
            on_click=admin_medicines
        )
        ui.button(
            "View Customer Orders",
            on_click=admin_orders
        )
        ui.button(
            "Logout",
            on_click=login_screen
        )
def admin_medicines():
    clear_page()
    with page:
        ui.label("Medicine Management").classes(
            "text-3xl font-bold"
        )
        name = ui.input("Medicine Name")
        category = ui.input("Category")
        price = ui.number("Price")
        stock = ui.number("Stock")
        def save():
            add_medicine(
                name.value,
                category.value,
                price.value,
                stock.value
            )
            ui.notify("Medicine added")
            admin_medicines()
        ui.button(
            "Add Medicine",
            on_click=save
        )
        for medicine in medicines():
            ui.label(
                f'{medicine["id"]}. '
                f'{medicine["name"]} '
                f'(Stock: {medicine["stock"]})'
            )
        ui.button(
            "Back",
            on_click=admin_screen
        )
   def admin_orders():
    clear_page()
    with page:
        ui.label("Customer Orders").classes(
            "text-3xl font-bold"
        )
        orders = all_orders()
        if not orders:
            ui.label("No orders found")
        for order in orders:
            ui.label(
                f'Order {order["id"]} | '
                f'{order["name"]} | '
                f'{order["email"]} | '
                f'₹{order["total"]} | '
                f'{order["status"]}'
            )
        ui.button(
            "Back",
            on_click=admin_screen
        )
login_screen()
ui.run(
    host="127.0.0.1",
    port=8080,
    title="Online Pharmacy Platform"
) 
#database.py
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
    cur.execute(
        "SELECT * FROM users WHERE email=?",
        ("admin@gmail.com",)
    )
    if not cur.fetchone():
        cur.execute(
            "INSERT INTO users (name,email,password,role) VALUES (?,?,?,?)",
            ("Admin", "admin@gmail.com", "admin123", "admin")
        )
    db.commit()
    db.close()
    #login.py
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

