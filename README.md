#online pharmacy platform
import tkinter as tk
from tkinter import messagebox
from database import setup_database
from login import register, login
from pharmacy import (
    medicines,
    add_medicine,
    delete_medicine,
    place_order,
    customer_orders,
    all_orders
)
