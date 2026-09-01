from nicegui import ui, app
from login import login, register
from pharmacy import (
    medicines,
    get_categories,
    place_order,
    customer_orders,
    all_orders,
    add_medicine
)
def get_user():
    return app.storage.user.get("user")
def logout():
    app.storage.user.clear()
    ui.navigate.to("/")
def login_page():
    with ui.column().classes(
        "w-full min-h-screen items-center justify-center bg-blue-50"
    ):
        with ui.card().classes("w-96 p-8 shadow-xl"):
            ui.label("MediCare Pharmacy").classes(
                "text-3xl font-bold text-blue-700"
            )

            ui.label(
                "Online Pharmacy Platform"
            ).classes("text-gray-600")

            email = ui.input(
                "Email"
            ).classes("w-full")

            password = ui.input(
                "Password",
                password=True
            ).classes("w-full")

            def do_login():
                user = login(
                    email.value,
                    password.value
                )
                if user:
                    app.storage.user["user"] = user
                    app.storage.user["cart"] = {}
                    if user["role"] == "admin":
                        ui.navigate.to("/admin")
                    else:
                        ui.navigate.to("/customer")
                else:
                    ui.notify(
                        "Invalid email or password",
                        type="negative"
                    )
            ui.button(
                "Login",
                on_click=do_login
            ).classes("w-full bg-blue-700 text-white")
            ui.button(
                "Create Account",
                on_click=lambda: ui.navigate.to("/register")
            ).classes("w-full")
            ui.separator()
            ui.label("Admin Login").classes("font-bold")
            ui.label("Email: admin@pharmacy.com")
            ui.label("Password: admin123")
def register_page():
    with ui.column().classes(
        "w-full min-h-screen items-center justify-center bg-gray-100"
    ):
        with ui.card().classes("w-96 p-8 shadow-xl"):
            ui.label(
                "Create Customer Account"
            ).classes(
                "text-2xl font-bold text-blue-700"
            )
            name = ui.input(
                "Name"
            ).classes("w-full")
            email = ui.input(
                "Email"
            ).classes("w-full")
            password = ui.input(
                "Password",
                password=True
            ).classes("w-full")
            def create():
                if register(
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
                on_click=create
            ).classes(
                "w-full bg-blue-700 text-white"
            )
            ui.button(
                "Back",
                on_click=lambda: ui.navigate.to("/")
            ).classes("w-full")
def customer_page():
    user = get_user()
    if not user:
        ui.navigate.to("/")
        return
    with ui.column().classes(
        "w-full min-h-screen bg-gray-100 p-6"
    ):
        with ui.row().classes(
            "w-full justify-between items-center bg-blue-700 text-white p-4 rounded-xl"
        ):
            ui.label(
                "MediCare Pharmacy"
            ).classes("text-2xl font-bold")
            ui.button(
                "Logout",
                on_click=logout
            ).props("flat color=white")
        ui.label(
            "Welcome, " + user["name"]
        ).classes("text-3xl font-bold mt-8")
        ui.label(
            "Your online pharmacy"
        ).classes("text-gray-600")
        with ui.row().classes(
            "gap-6 mt-8 flex-wrap"
        ):
            with ui.card().classes("w-72 p-6"):
                ui.label("Medicine Store").classes(
                    "text-xl font-bold"
                )
                ui.label(
                    "Search and buy medicines."
                )
                ui.button(
                    "Browse Medicines",
                    on_click=lambda: ui.navigate.to(
                        "/medicines"
                    )
                )
            with ui.card().classes("w-72 p-6"):
                ui.label("Shopping Cart").classes(
                    "text-xl font-bold"
                )
                ui.label(
                    "View selected medicines."
                )
                ui.button(
                    "View Cart",
                    on_click=lambda: ui.navigate.to(
                        "/cart"
                    )
                )
            with ui.card().classes("w-72 p-6"):
                ui.label("My Orders").classes(
                    "text-xl font-bold"
                )
                ui.label(
                    "View your previous orders."
                )
                ui.button(
                    "My Orders",
                    on_click=lambda: ui.navigate.to(
                        "/orders"
                    )
                )
def medicine_page():
    if not get_user():
        ui.navigate.to("/")
        return
    cart = app.storage.user.get("cart", {})
    with ui.column().classes(
        "w-full min-h-screen bg-gray-100 p-6"
    ):
        with ui.row().classes(
            "w-full justify-between items-center bg-blue-700 text-white p-4 rounded-xl"
        ):
            ui.label(
                "Medicine Store"
            ).classes("text-2xl font-bold")
            ui.button(
                "Cart",
                on_click=lambda: ui.navigate.to("/cart")
            ).props("flat color=white")
        ui.label(
            "Find Your Medicines"
        ).classes("text-3xl font-bold mt-7")
        with ui.row().classes("w-full"):
            search = ui.input(
                "Search medicine"
            ).classes("flex-grow")
            category = ui.select(
                ["All"] + get_categories(),
                value="All",
                label="Category"
            ).classes("w-48")
        products = ui.grid(
            columns=3
        ).classes("w-full gap-6 mt-6")
        def load():
            products.clear()
            items = medicines(
                search.value or "",
                category.value or "All"
            )
            with products:
                for medicine in items:
                    with ui.card().classes(
                        "w-full p-4 shadow-lg"
                    ):
                        if medicine.get("image"):
                            ui.image(
                                medicine["image"]
                            ).classes(
                                "w-full h-40 object-cover rounded-lg"
                            )
                        ui.label(
                            medicine["name"]
                        ).classes(
                            "text-xl font-bold"
                        )
                        ui.label(
                            medicine["category"]
                        ).classes(
                            "text-blue-600"
                        )
                        ui.label(
                            medicine.get(
                                "description",
                                ""
                            )
                        ).classes(
                            "text-gray-600"
                        )
                        ui.label(
                            "₹" + str(medicine["price"])
                        ).classes(
                            "text-xl font-bold text-green-700"
                        )
                        ui.label(
                            "Stock: " +
                            str(medicine["stock"])
                        )
                        def add(
                            medicine_id=medicine["id"]
                        ):
                            key = str(medicine_id)
                            cart[key] = cart.get(key, 0) + 1
                            app.storage.user["cart"] = cart
                            ui.notify(
                                "Medicine added to cart"
                            )
                        ui.button(
                            "Add to Cart",
                            on_click=add
                        ).classes(
                            "w-full bg-blue-700 text-white"
                        )
                if not items:
                    ui.label(
                        "No medicines found."
                    ).classes(
                        "text-xl text-gray-500"
                    )
        ui.button(
            "Search",
            on_click=load
        )
        load()
def cart_page():
    user = get_user()
    if not user:
        ui.navigate.to("/")
        return
    cart = app.storage.user.get("cart", {})
    with ui.column().classes(
        "w-full min-h-screen bg-gray-100 p-6"
    ):
        ui.label(
            "Shopping Cart"
        ).classes(
            "text-3xl font-bold"
        )
        if not cart:
            ui.label(
                "Your cart is empty."
            ).classes("text-xl")

            ui.button(
                "Browse Medicines",
                on_click=lambda: ui.navigate.to(
                    "/medicines"
                )
            )
            return
        total = 0
        items = medicines()
        for key, quantity in cart.items():
            medicine = next(
                (
                    m for m in items
                    if str(m["id"]) == str(key)
                ),
                None
            )
            if medicine:
                amount = (
                    medicine["price"] *
                    quantity
                )
                total += amount
                ui.label(
                    medicine["name"] +
                    " x " +
                    str(quantity) +
                    " = ₹" +
                    str(amount)
                ).classes(
                    "text-lg"
                )
        ui.label(
            "Total: ₹" + str(total)
        ).classes(
            "text-2xl font-bold"
        )
        def checkout():
            order_cart = {
                int(k): v
                for k, v in cart.items()
            }
            if place_order(
                user["id"],
                order_cart
            ):
                app.storage.user["cart"] = {}
                ui.notify(
                    "Order placed successfully"
                )
                ui.navigate.to("/orders")
            else:
                ui.notify(
                    "Order could not be placed",
                    type="negative"
                )
        ui.button(
            "Place Order",
            on_click=checkout
        ).classes(
            "bg-green-600 text-white"
        )
        ui.button(
            "Continue Shopping",
            on_click=lambda: ui.navigate.to(
                "/medicines"
            )
        )
def orders_page():
    user = get_user()
    if not user:
        ui.navigate.to("/")
        return
    with ui.column().classes(
        "w-full min-h-screen bg-gray-100 p-6"
    ):
        ui.label(
            "My Orders"
        ).classes(
            "text-3xl font-bold"
        )
        orders = customer_orders(
            user["id"]
        )
        if not orders:
            ui.label(
                "No orders found."
            )
        for order in orders:
            with ui.card().classes(
                "w-full max-w-3xl p-5"
            ):
                ui.label(
                    "Order #" +
                    str(order["id"])
                ).classes(
                    "text-xl font-bold"
                )
                ui.label(
                    "Total: ₹" +
                    str(order["total"])
                )
                ui.label(
                    "Status: " +
                    order["status"]
                ).classes(
                    "text-blue-700"
                )
def admin_page():
    user = get_user()
    if not user or user["role"] != "admin":
        ui.navigate.to("/")
        return
    with ui.column().classes(
        "w-full min-h-screen bg-gray-100 p-6"
    ):
        ui.label(
            "Admin Dashboard"
        ).classes(
            "text-3xl font-bold"
        )
        ui.label(
            "Welcome Administrator"
        ).classes("text-gray-600")
        ui.button(
            "Manage Medicines",
            on_click=lambda: ui.navigate.to(
                "/admin/medicines"
            )
        )
        ui.button(
            "Customer Orders",
            on_click=lambda: ui.navigate.to(
                "/admin/orders"
            )
        )
        ui.button(
            "Logout",
            on_click=logout
        )
def admin_medicines_page():
    user = get_user()
    if not user or user["role"] != "admin":
        ui.navigate.to("/")
        return
    with ui.column().classes(
        "w-full min-h-screen bg-gray-100 p-6"
    ):
        ui.label(
            "Medicine Management"
        ).classes(
            "text-3xl font-bold"
        )
        name = ui.input(
            "Medicine Name"
        )
        category = ui.input(
            "Category"
        )
        description = ui.input(
            "Description"
        )
        price = ui.number(
            "Price"
        )
        stock = ui.number(
            "Stock"
        )
        image = ui.input(
            "Image URL"
        )
        def save():
            if add_medicine(
                name.value,
                category.value,
                description.value or "",
                price.value,
                stock.value,
                image.value or ""
            ):
                ui.notify(
                    "Medicine added successfully"
                )
                ui.navigate.to(
                    "/admin/medicines"
                )
            else:
                ui.notify(
                    "Invalid details",
                    type="negative"
                )
        ui.button(
            "Add Medicine",
            on_click=save
        )
        ui.label(
            "Current Medicines"
        ).classes(
            "text-2xl font-bold mt-6"
        )
        for medicine in medicines():
            ui.label(
                str(medicine["id"]) +
                ". " +
                medicine["name"] +
                " | Stock: " +
                str(medicine["stock"])
            )
def admin_orders_page():
    user = get_user()
    if not user or user["role"] != "admin":
        ui.navigate.to("/")
        return
    with ui.column().classes(
        "w-full min-h-screen bg-gray-100 p-6"
    ):
        ui.label(
            "Customer Orders"
        ).classes(
            "text-3xl font-bold"
        )
        orders = all_orders()
        if not orders:
            ui.label(
                "No orders found."
            )
        for order in orders:
            with ui.card().classes(
                "w-full max-w-3xl p-5"
            ):
                ui.label(
                    "Order #" +
                    str(order["id"])
                ).classes(
                    "text-xl font-bold"
                )
                ui.label(
                    "Customer: " +
                    order["name"]
                )
                ui.label(
                    "Email: " +
                    order["email"]
                )
                ui.label(
                    "Total: ₹" +
                    str(order["total"])
                )
                ui.label(
                    "Status: " +
                    order["status"]
                )
