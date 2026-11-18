import sqlite3

from main import hash_password

connection = sqlite3.connect("brightmart.db")

connection.execute("PRAGMA foreign_keys = ON")

cursor = connection.cursor()

cursor.execute("PRAGMA foreign_keys")

foreign_keys = cursor.fetchone()

print("Foreign key enforcement:", foreign_keys[0])

cursor.execute("""
CREATE TABLE IF NOT EXISTS USER (
    UserID INTEGER PRIMARY KEY AUTOINCREMENT,
    FullName TEXT NOT NULL,
    Username TEXT NOT NULL UNIQUE,
    Password TEXT NOT NULL,
    Role TEXT NOT NULL
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS SUPPLIER (
    SupplierID INTEGER PRIMARY KEY AUTOINCREMENT,
    SupplierName TEXT NOT NULL,
    ContactNumber TEXT NOT NULL,
    Email TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS PRODUCT (
    ProductID INTEGER PRIMARY KEY AUTOINCREMENT,
    ProductName TEXT NOT NULL,
    Price REAL NOT NULL,
    Quantity INTEGER NOT NULL,
    ReorderLevel INTEGER NOT NULL,
    SupplierID INTEGER NOT NULL,
    FOREIGN KEY (SupplierID) REFERENCES SUPPLIER(SupplierID)
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS SALE (
    SaleID INTEGER PRIMARY KEY AUTOINCREMENT,
    SaleDate TEXT NOT NULL,
    UserID INTEGER NOT NULL,
    TotalAmount REAL NOT NULL,
    FOREIGN KEY (UserID) REFERENCES USER(UserID)
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS SALE_ITEM (
    SaleItemID INTEGER PRIMARY KEY AUTOINCREMENT,
    SaleID INTEGER NOT NULL,
    ProductID INTEGER NOT NULL,
    Quantity INTEGER NOT NULL,
    UnitPrice REAL NOT NULL,
    SubTotal REAL NOT NULL,
    FOREIGN KEY (SaleID) REFERENCES SALE(SaleID),
    FOREIGN KEY (ProductID) REFERENCES PRODUCT(ProductID)
)
""")

connection.commit()

print("All BrightMart database tables created successfully.")

# Check which tables exist in the database
cursor.execute("""
SELECT name
FROM sqlite_master
WHERE type='table'
""")

tables = cursor.fetchall()

print("Tables in BrightMart database:")
print(tables)

# Add Store Manager
cursor.execute("""
INSERT OR IGNORE INTO USER
(FullName, Username, Password, Role)
VALUES (?, ?, ?, ?)
""", (
    "Junaid Fredericks",
    "junaid",
    hash_password("Test123"),
    "Store Manager"
))

# Add Sales Staff
cursor.execute("""
INSERT OR IGNORE INTO USER
(FullName, Username, Password, Role)
VALUES (?, ?, ?, ?)
""", (
    "Sales User",
    "sales",
    hash_password("Sales123"),
    "Sales Staff"
))

# Add Business Owner
cursor.execute("""
INSERT OR IGNORE INTO USER
(FullName, Username, Password, Role)
VALUES (?, ?, ?, ?)
""", (
    "Business Owner",
    "owner",
    hash_password("Owner123"),
    "Business Owner"
))


# Update the existing users that previously had plain-text passwords
cursor.execute(
    "UPDATE USER SET Password = ? WHERE Username = ?",
    (hash_password("Test123"), "junaid")
)

cursor.execute(
    "UPDATE USER SET Password = ? WHERE Username = ?",
    (hash_password("Sales123"), "sales")
)

cursor.execute(
    "UPDATE USER SET Password = ? WHERE Username = ?",
    (hash_password("Owner123"), "owner")
)


# Save all changes
connection.commit()

connection.commit()

print("Test user added successfully.")


# Read users from the database
cursor.execute("SELECT * FROM USER")

users = cursor.fetchall()

print("Users in database:")

for user in users:
    print(user)

connection.close()