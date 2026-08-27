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
