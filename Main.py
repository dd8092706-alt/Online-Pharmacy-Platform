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
