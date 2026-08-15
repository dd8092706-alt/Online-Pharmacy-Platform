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
    def login_screen():
    clear()
    title("Online Pharmacy")
    tk.Label(root, text="Email").pack()
    email = tk.Entry(root, width=35)
    email.pack(pady=5)
    tk.Label(root, text="Password").pack()
    password = tk.Entry(root, show="*", width=35)
    password.pack(pady=5)
    def do_login():
        global current_user
        user = login(
            email.get(),
            password.get()
        )
        if user:
            current_user = user
            if user["role"] == "admin":
                admin_screen()
            else:
                customer_screen()
        else:
            messagebox.showerror(
                "Login",
                "Invalid email or password"
            )
            tk.Button(
        root,
        text="Login",
        width=20,
        command=do_login
    ).pack(pady=10)
    tk.Button(
        root,
        text="Create Account",
        width=20,
        command=register_screen
    ).pack()
    def register_screen():
    clear()
    title("Create Customer Account")
    labels = ["Name", "Email", "Password"]
    entries = []
    for text in labels:
        tk.Label(root, text=text).pack()
        entry = tk.Entry(root, width=35)
        entry.pack(pady=5)
        entries.append(entry)
        def save():
        if register(
            entries[0].get(),
            entries[1].get(),
            entries[2].get()
        ):
            messagebox.showinfo(
                "Registration",
                "Account created successfully"
            )
            login_screen()
        else:
            messagebox.showerror(
                "Registration",
                "Email already exists"
            )
            tk.Button(
        root,
        text="Register",
        command=save
    ).pack(pady=10)
    tk.Button(
        root,
        text="Back",
        command=login_screen
    ).pack()
