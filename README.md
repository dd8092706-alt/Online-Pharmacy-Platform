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
    def customer_screen():
    clear()
    title("Customer Dashboard")
    tk.Label(
        root,
        text="Welcome " + current_user["name"],
        font=("Arial", 14)
    ).pack()
    tk.Button(
        root,
        text="Browse Medicines",
        width=25,
        command=medicine_screen
    ).pack(pady=8)
    tk.Button(
        root,
        text="View Cart",
        width=25,
        command=cart_screen
    ).pack(pady=8)
    tk.Button(
        root,
        text="My Orders",
        width=25,
        command=orders_screen
    ).pack(pady=8)
    tk.Button(
        root,
        text="Logout",
        width=25,
        command=login_screen
    ).pack(pady=8)
    def medicine_screen():
    clear()
    title("Available Medicines")
    search = tk.Entry(root, width=30)
    search.pack()
    frame = tk.Frame(root)
    frame.pack(pady=15)
    def load():
        for widget in frame.winfo_children():
            widget.destroy()
        for medicine in medicines(search.get()):
            text = (
                f'{medicine["name"]} | '
                f'{medicine["category"]} | '
                f'₹{medicine["price"]} | '
                f'Stock: {medicine["stock"]}'
            )
            row = tk.Frame(frame)
            row.pack(pady=4)
            tk.Label(
                row,
                text=text,
                width=60,
                anchor="w"
            ).pack(side="left")
            tk.Button(
                row,
                text="Add",
                command=lambda m=medicine:
                    add_cart(m["id"])
            ).pack(side="left")
            tk.Button(
        root,
        text="Search",
        command=load
    ).pack(pady=5)
    load()
    tk.Button(
        root,
        text="Back",
        command=customer_screen
    ).pack(pady=10)
    def add_cart(medicine_id):
    cart[medicine_id] = cart.get(
        medicine_id, 0
    ) + 1
    messagebox.showinfo(
        "Cart",
        "Medicine added to cart"
    )
    def cart_screen():
    clear()
    title("Shopping Cart")
    if not cart:
        tk.Label(
            root,
            text="Cart is empty"
        ).pack()
    else:
        total = 0
        for medicine_id, quantity in cart.items():
            item = medicines()
            for medicine in item:
                if medicine["id"] == medicine_id:
                amount = (
                        medicine["price"] * quantity
                    )
                    total += amount
                    tk.Label(
                        root,
                        text=f'{medicine["name"]}  '
                             f'x {quantity}  '
                             f'= ₹{amount}'
                    ).pack(pady=5)
                    tk.Label(
            root,
            text=f"Total: ₹{total}",
            font=("Arial", 16, "bold")
        ).pack(pady=15)
        def checkout():
            if place_order(
                current_user["id"],
                cart
            ):
                cart.clear()
                messagebox.showinfo(
                    "Order",
                    "Order placed successfully"
                )
                customer_screen()
            else:
                messagebox.showerror(
                    "Order",
                    "Insufficient stock"
                )
        tk.Button(
            root,
            text="Place Order",
            command=checkout
        ).pack()
        tk.Button(
        root,
        text="Back",
        command=customer_screen
    ).pack(pady=15)
def orders_screen():
    clear()
    title("My Orders")
    for order in customer_orders(
        current_user["id"]
    ):
        text = (
            f'Order {order["id"]}   '
            f'Total: ₹{order["total"]}   '
            f'Status: {order["status"]}'
        )
        tk.Label(
            root,
            text=text,
            font=("Arial", 12)
        ).pack(pady=5)
        tk.Button(
        root,
        text="Back",
        command=customer_screen
    ).pack(pady=15)
def admin_screen():
    clear()
    title("Admin Dashboard")
    tk.Button(
        root,
        text="Manage Medicines",
        width=25,
        command=admin_medicines
    ).pack(pady=10)
    tk.Button(
        root,
        text="View Customer Orders",
        width=25,
        command=admin_orders
    ).pack(pady=10)
    tk.Button(
        root,
        text="Logout",
        width=25,
        command=login_screen
    ).pack(pady=10)
def admin_medicines():
    clear()
    title("Medicine Management")
    fields = []
    for text in [
        "Medicine Name",
        "Category",
        "Price",
        "Stock"
    ]:
        tk.Label(root, text=text).pack()
        entry = tk.Entry(root)
        entry.pack(pady=3)
        fields.append(entry)
    def save():
        add_medicine(
            fields[0].get(),
            fields[1].get(),
            float(fields[2].get()),
            int(fields[3].get())
        )
        messagebox.showinfo(
            "Admin",
            "Medicine added"
        )
        admin_medicines()
    tk.Button(
        root,
        text="Add Medicine",
        command=save
    ).pack(pady=10)
    for medicine in medicines():
        tk.Label(
            root,
            text=f'{medicine["id"]}. '
                 f'{medicine["name"]} '
                 f'(Stock: {medicine["stock"]})'
        ).pack()
    tk.Button(
        root,
        text="Back",
        command=admin_screen
    ).pack(pady=15)
def admin_orders():
    clear()
    title("Customer Orders")
    for order in all_orders():
        text = (
            f'Order {order["id"]} | '
            f'{order["name"]} | '
            f'{order["email"]} | '
            f'₹{order["total"]} | '
            f'{order["status"]}'
        )
        tk.Label(
            root,
            text=text
        ).pack(pady=5)
    tk.Button(
        root,
        text="Back",
        command=admin_screen
    ).pack(pady=15)
login_screen()
root.mainloop()
