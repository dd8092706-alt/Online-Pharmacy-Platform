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
