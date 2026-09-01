import sqlite3
import hashlib
from config import DATABASE, ADMIN_EMAIL, ADMIN_PASSWORD
def connect():
    db = sqlite3.connect(DATABASE)
    db.row_factory = sqlite3.Row
    return db
def hash_password(password):
    return hashlib.sha256(
        password.encode()
    ).hexdigest()
def setup_database():
    db = connect()
    cur = db.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role TEXT NOT NULL DEFAULT 'customer'
        )
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS medicines (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            category TEXT NOT NULL,
            description TEXT,
            price REAL NOT NULL,
            stock INTEGER NOT NULL,
            image TEXT
        )
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            total REAL NOT NULL,
            status TEXT NOT NULL DEFAULT 'Placed',
            order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS order_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_id INTEGER NOT NULL,
            medicine_id INTEGER NOT NULL,
            quantity INTEGER NOT NULL,
            price REAL NOT NULL,
            FOREIGN KEY(order_id) REFERENCES orders(id),
            FOREIGN KEY(medicine_id) REFERENCES medicines(id)
        )
    """)
    admin = cur.execute(
        "SELECT id FROM users WHERE email = ?",
        (ADMIN_EMAIL,)
    ).fetchone()
    if admin is None:
        cur.execute("""
            INSERT INTO users
            (name, email, password, role)
            VALUES (?, ?, ?, ?)
        """, (
            "Pharmacy Administrator",
            ADMIN_EMAIL,
            hash_password(ADMIN_PASSWORD),
            "admin"
        ))
    count = cur.execute(
        "SELECT COUNT(*) FROM medicines"
    ).fetchone()[0]
    if count == 0:
        sample_medicines = [
            (
                "Paracetamol 500mg",
                "Pain Relief",
                "Used for temporary relief of fever and mild pain.",
                25.00,
                100,
                "https://images.unsplash.com/photo-1584308666744-24d5c474f2ae"
            ),
            (
                "Vitamin C Tablets",
                "Vitamins",
                "Vitamin supplement for everyday nutritional support.",
                120.00,
                75,
                "https://images.unsplash.com/photo-1550572017-edd951aa8ca2"
            ),
            (
                "Cetirizine",
                "Allergy",
                "Commonly used for allergy symptom relief.",
                45.00,
                80,
                "https://images.unsplash.com/photo-1587854692152-cbe660dbde88"
            ),
            (
                "Cough Syrup",
                "Cold & Cough",
                "Cough relief syrup for common cold symptoms.",
                95.00,
                60,
                "https://images.unsplash.com/photo-1603398938378-e54eab446dde"
            ),
            (
                "Antacid Tablets",
                "Digestive Care",
                "Provides relief from occasional acidity and heartburn.",
                55.00,
                70,
                "https://images.unsplash.com/photo-1584308666744-24d5c474f2ae"
            ),
            (
                "First Aid Cream",
                "First Aid",
                "Topical cream for minor skin care and first aid.",
                85.00,
                50,
                "https://images.unsplash.com/photo-1603398938378-e54eab446dde"
            ),
            (
                "Multivitamin Tablets",
                "Vitamins",
                "Daily multivitamin nutritional supplement.",
                180.00,
                45,
                "https://images.unsplash.com/photo-1550572017-edd951aa8ca2"
            ),
            (
                "Digital Thermometer",
                "Health Devices",
                "Digital thermometer for checking body temperature.",
                250.00,
                30,
                "https://images.unsplash.com/photo-1588776814546-daab30f310ce"
            )
        ]
        cur.executemany("""
            INSERT INTO medicines
            (name, category, description, price, stock, image)
            VALUES (?, ?, ?, ?, ?, ?)
        """, sample_medicines)
    db.commit()
    db.close()
