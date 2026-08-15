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
setup_database()
root = tk.Tk()
root.title("Online Pharmacy Platform")
root.geometry("900x600")
current_user = None
cart = {}
def clear():
    for widget in root.winfo_children():
        widget.destroy()
        def title(text):
    tk.Label(
        root,
        text=text,
        font=("Arial", 24, "bold")
    ).pack(pady=20)
