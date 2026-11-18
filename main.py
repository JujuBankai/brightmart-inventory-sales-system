import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import sqlite3
from datetime import datetime
import hashlib
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def open_suppliers(full_name, role):
    # Clear current screen
    for widget in root.winfo_children():
        widget.destroy()

    # Heading
    title_label = tk.Label(
        root,
        text="Supplier Management",
        font=("Arial", 22, "bold")
    )
    title_label.pack(pady=30)

    # Supplier Name
    supplier_name_label = tk.Label(root, text="Supplier Name")
    supplier_name_label.pack()

    supplier_name_entry = tk.Entry(root, width=30)
    supplier_name_entry.pack(pady=5)

    # Contact Number
    contact_label = tk.Label(root, text="Contact Number")
    contact_label.pack()

    contact_entry = tk.Entry(root, width=30)
    contact_entry.pack(pady=5)

    # Email
    email_label = tk.Label(root, text="Email")
    email_label.pack()

    email_entry = tk.Entry(root, width=30)
    email_entry.pack(pady=5)

    # Function to save supplier
    def add_supplier():
        supplier_name = supplier_name_entry.get().strip()
        contact_number = contact_entry.get().strip()
        email = email_entry.get().strip()

        if supplier_name == "" or contact_number == "":
            messagebox.showerror(
                "Missing Information",
                "Supplier name and contact number are required."
            )
            return

        connection = sqlite3.connect("brightmart.db")
        cursor = connection.cursor()

        cursor.execute("""
        INSERT INTO SUPPLIER
        (SupplierName, ContactNumber, Email)
        VALUES (?, ?, ?)
        """, (supplier_name, contact_number, email))

        connection.commit()
        connection.close()

        messagebox.showinfo(
            "Supplier Added",
            "Supplier added successfully."
        )

        supplier_name_entry.delete(0, tk.END)
        contact_entry.delete(0, tk.END)
        email_entry.delete(0, tk.END)

    # Add Supplier button
    add_supplier_button = tk.Button(
        root,
        text="Add Supplier",
        width=15,
        command=add_supplier
    )
    add_supplier_button.pack(pady=15)

    

        # Saved Suppliers heading
    supplier_list_label = tk.Label(
        root,
        text="Saved Suppliers",
        font=("Arial", 14, "bold")
    )
    supplier_list_label.pack(pady=10)

    # Supplier table
    columns = (
        "SupplierID",
        "SupplierName",
        "ContactNumber",
        "Email"
    )

    supplier_table = ttk.Treeview(
        root,
        columns=columns,
        show="headings",
        height=6
    )

    supplier_table.heading("SupplierID", text="ID")
    supplier_table.heading("SupplierName", text="Supplier")
    supplier_table.heading("ContactNumber", text="Contact Number")
    supplier_table.heading("Email", text="Email")

    supplier_table.column("SupplierID", width=50)
    supplier_table.column("SupplierName", width=180)
    supplier_table.column("ContactNumber", width=130)
    supplier_table.column("Email", width=220)

    # Read suppliers from database
    connection = sqlite3.connect("brightmart.db")
    cursor = connection.cursor()

    cursor.execute("""
    SELECT
        SupplierID,
        SupplierName,
        ContactNumber,
        Email
    FROM SUPPLIER
    ORDER BY SupplierName
    """)

    suppliers = cursor.fetchall()

    connection.close()

    for supplier in suppliers:
        supplier_table.insert(
            "",
            tk.END,
            values=supplier
        )

    supplier_table.pack(pady=5)

        # Load selected supplier into the fields
    def select_supplier(event):
        selected_items = supplier_table.selection()

        if not selected_items:
            return

        selected_item = selected_items[0]
        supplier = supplier_table.item(selected_item)["values"]

        supplier_name_entry.delete(0, tk.END)
        supplier_name_entry.insert(0, supplier[1])

        contact_entry.delete(0, tk.END)
        contact_entry.insert(0, supplier[2])

        email_entry.delete(0, tk.END)
        email_entry.insert(0, supplier[3])

    supplier_table.bind(
        "<<TreeviewSelect>>",
        select_supplier
    )

        # Update selected supplier
    def update_supplier():
        selected_items = supplier_table.selection()

        if not selected_items:
            messagebox.showerror(
                "No Supplier Selected",
                "Please select a supplier to update."
            )
            return

        selected_item = selected_items[0]
        supplier_id = supplier_table.item(selected_item)["values"][0]

        supplier_name = supplier_name_entry.get().strip()
        contact_number = contact_entry.get().strip()
        email = email_entry.get().strip()

        if supplier_name == "" or contact_number == "":
            messagebox.showerror(
                "Missing Information",
                "Supplier name and contact number are required."
            )
            return

        connection = sqlite3.connect("brightmart.db")
        cursor = connection.cursor()

        cursor.execute("""
        UPDATE SUPPLIER
        SET SupplierName = ?,
            ContactNumber = ?,
            Email = ?
        WHERE SupplierID = ?
        """, (
            supplier_name,
            contact_number,
            email,
            supplier_id
        ))

        connection.commit()
        connection.close()

        messagebox.showinfo(
            "Supplier Updated",
            "Supplier updated successfully."
        )

        open_suppliers(full_name, role)

        update_supplier_button = tk.Button(
        root,
        text="Update Supplier",
        width=15,
        command=update_supplier
    )
        update_supplier_button.pack(pady=5)

            # Delete selected supplier
    def delete_supplier():
        selected_items = supplier_table.selection()

        if not selected_items:
            messagebox.showerror(
                "No Supplier Selected",
                "Please select a supplier to delete."
            )
            return

        selected_item = selected_items[0]
        supplier = supplier_table.item(selected_item)["values"]

        supplier_id = supplier[0]
        supplier_name = supplier[1]

        confirm = messagebox.askyesno(
            "Confirm Delete",
            f"Are you sure you want to delete {supplier_name}?"
        )

        if not confirm:
            return

        connection = sqlite3.connect("brightmart.db")
        connection.execute("PRAGMA foreign_keys = ON")
        cursor = connection.cursor()

        try:
            cursor.execute(
                "DELETE FROM SUPPLIER WHERE SupplierID = ?",
                (supplier_id,)
            )

            connection.commit()

            messagebox.showinfo(
                "Supplier Deleted",
                "Supplier deleted successfully."
            )

        except sqlite3.IntegrityError:
            messagebox.showerror(
                "Cannot Delete Supplier",
                "This supplier cannot be deleted because products are linked to it."
            )

        finally:
            connection.close()

        open_suppliers(full_name, role)

            # Delete Supplier button
    delete_supplier_button = tk.Button(
        root,
        text="Delete Supplier",
        width=15,
        command=delete_supplier
    )
    delete_supplier_button.pack(pady=5)

            # Update selected supplier
    def update_supplier():
        selected_items = supplier_table.selection()

        if not selected_items:
            messagebox.showerror(
                "No Supplier Selected",
                "Please select a supplier to update."
            )
            return

        selected_item = selected_items[0]
        supplier_id = supplier_table.item(selected_item)["values"][0]

        supplier_name = supplier_name_entry.get().strip()
        contact_number = contact_entry.get().strip()
        email = email_entry.get().strip()

        if supplier_name == "" or contact_number == "":
            messagebox.showerror(
                "Missing Information",
                "Supplier name and contact number are required."
            )
            return

        connection = sqlite3.connect("brightmart.db")
        cursor = connection.cursor()

        cursor.execute("""
        UPDATE SUPPLIER
        SET SupplierName = ?,
            ContactNumber = ?,
            Email = ?
        WHERE SupplierID = ?
        """, (
            supplier_name,
            contact_number,
            email,
            supplier_id
        ))

        connection.commit()
        connection.close()

        messagebox.showinfo(
            "Supplier Updated",
            "Supplier updated successfully."
        )

        open_suppliers(full_name, role)

            # Load selected supplier into the fields
    def select_supplier(event):
        selected_items = supplier_table.selection()

        if not selected_items:
            return

        selected_item = selected_items[0]
        supplier = supplier_table.item(selected_item)["values"]

        supplier_name_entry.delete(0, tk.END)
        supplier_name_entry.insert(0, supplier[1])

        contact_entry.delete(0, tk.END)
        contact_entry.insert(0, supplier[2])

        email_entry.delete(0, tk.END)
        email_entry.insert(0, supplier[3])

    supplier_table.bind(
        "<<TreeviewSelect>>",
        select_supplier
    )

    # Update selected supplier
    def update_supplier():
        selected_items = supplier_table.selection()

        if not selected_items:
            messagebox.showerror(
                "No Supplier Selected",
                "Please select a supplier to update."
            )
            return

        selected_item = selected_items[0]
        supplier_id = supplier_table.item(selected_item)["values"][0]

        supplier_name = supplier_name_entry.get().strip()
        contact_number = contact_entry.get().strip()
        email = email_entry.get().strip()

        if supplier_name == "" or contact_number == "":
            messagebox.showerror(
                "Missing Information",
                "Supplier name and contact number are required."
            )
            return

        connection = sqlite3.connect("brightmart.db")
        cursor = connection.cursor()

        cursor.execute("""
        UPDATE SUPPLIER
        SET SupplierName = ?,
            ContactNumber = ?,
            Email = ?
        WHERE SupplierID = ?
        """, (
            supplier_name,
            contact_number,
            email,
            supplier_id
        ))

        connection.commit()
        connection.close()

        messagebox.showinfo(
            "Supplier Updated",
            "Supplier updated successfully."
        )

        open_suppliers(full_name, role)

        # Update Supplier button
    update_supplier_button = tk.Button(
        root,
        text="Update Supplier",
        width=15,
        command=update_supplier
    )
    update_supplier_button.pack(pady=5)

    # Back button
    back_button = tk.Button(
        root,
        text="Back to Dashboard",
        width=20,
        command=lambda: open_dashboard(full_name, role)
    )
    back_button.pack(pady=5)


def open_products(full_name, role):
    # Clear the current screen
    for widget in root.winfo_children():
        widget.destroy()

    # Heading
    title_label = tk.Label(
        root,
        text="Product Management",
        font=("Arial", 22, "bold")
    )
    title_label.pack(pady=25)

    # Product Name
    product_name_label = tk.Label(root, text="Product Name")
    product_name_label.pack()

    product_name_entry = tk.Entry(root, width=30)
    product_name_entry.pack(pady=5)

    # Price
    price_label = tk.Label(root, text="Price")
    price_label.pack()

    price_entry = tk.Entry(root, width=30)
    price_entry.pack(pady=5)

    # Quantity
    quantity_label = tk.Label(root, text="Quantity")
    quantity_label.pack()

    quantity_entry = tk.Entry(root, width=30)
    quantity_entry.pack(pady=5)

    # Reorder Level
    reorder_label = tk.Label(root, text="Reorder Level")
    reorder_label.pack()

    reorder_entry = tk.Entry(root, width=30)
    reorder_entry.pack(pady=5)

    # Supplier ID
    # Supplier dropdown
    supplier_label = tk.Label(root, text="Supplier")
    supplier_label.pack()

    connection = sqlite3.connect("brightmart.db")
    cursor = connection.cursor()

    cursor.execute("""
    SELECT SupplierID, SupplierName
    FROM SUPPLIER
    ORDER BY SupplierName
    """)

    suppliers = cursor.fetchall()
    connection.close()

    supplier_options = [
        f"{supplier[0]} - {supplier[1]}"
        for supplier in suppliers
    ]

    supplier_combo = ttk.Combobox(
        root,
        values=supplier_options,
        width=27,
        state="readonly"
    )
    supplier_combo.pack(pady=5)

    # Function to save product
    def add_product():
        product_name = product_name_entry.get().strip()
        price = price_entry.get().strip()
        quantity = quantity_entry.get().strip()
        reorder_level = reorder_entry.get().strip()
        selected_supplier = supplier_combo.get()

        # Check required information
        if (
            product_name == ""
            or price == ""
            or quantity == ""
            or reorder_level == ""
            or selected_supplier == ""
        ):
            messagebox.showerror(
                "Missing Information",
                "Please complete all product fields."
            )
            return

        # Validate numbers
        try:
            price = float(price)
            quantity = int(quantity)
            reorder_level = int(reorder_level)
        except ValueError:
            messagebox.showerror(
                "Invalid Information",
                "Price must be a number and quantity values must be whole numbers."
            )
            return

        # Prevent invalid values
        if price <= 0 or quantity < 0 or reorder_level < 0:
            messagebox.showerror(
                "Invalid Information",
                "Price must be greater than zero and stock values cannot be negative."
            )
            return

        # Extract SupplierID from dropdown
        supplier_id = int(selected_supplier.split(" - ")[0])

        connection = sqlite3.connect("brightmart.db")
        connection.execute("PRAGMA foreign_keys = ON")
        cursor = connection.cursor()

        cursor.execute("""
        INSERT INTO PRODUCT
        (ProductName, Price, Quantity, ReorderLevel, SupplierID)
        VALUES (?, ?, ?, ?, ?)
        """, (
            product_name,
            price,
            quantity,
            reorder_level,
            supplier_id
        ))

        connection.commit()
        connection.close()

        messagebox.showinfo(
            "Product Added",
            "Product added successfully."
        )

        # Refresh Product Management screen
        open_products(full_name, role)

        # Clear fields
        product_name_entry.delete(0, tk.END)
        price_entry.delete(0, tk.END)
        quantity_entry.delete(0, tk.END)
        reorder_entry.delete(0, tk.END)
        supplier_combo.set("")

    # Add Product button
    add_button = tk.Button(
        root,
        text="Add Product",
        width=15,
        command=add_product
    )
    add_button.pack(pady=15)

    # Product list heading
    product_list_label = tk.Label(
        root,
        text="Saved Products",
        font=("Arial", 14, "bold")
    )
    product_list_label.pack(pady=10)

    # Create product table
    columns = (
        "ProductID",
        "ProductName",
        "Price",
        "Quantity",
        "ReorderLevel",
        "Supplier"
    )

    product_table = ttk.Treeview(
        root,
        columns=columns,
        show="headings",
        height=6
    )

    product_table.heading("ProductID", text="ID")
    product_table.heading("ProductName", text="Product")
    product_table.heading("Price", text="Price")
    product_table.heading("Quantity", text="Quantity")
    product_table.heading("ReorderLevel", text="Reorder Level")
    product_table.heading("Supplier", text="Supplier")

    product_table.column("ProductID", width=50)
    product_table.column("ProductName", width=140)
    product_table.column("Price", width=80)
    product_table.column("Quantity", width=80)
    product_table.column("ReorderLevel", width=100)
    product_table.column("Supplier", width=160)

    connection = sqlite3.connect("brightmart.db")
    cursor = connection.cursor()

    cursor.execute("""
    SELECT
        PRODUCT.ProductID,
        PRODUCT.ProductName,
        PRODUCT.Price,
        PRODUCT.Quantity,
        PRODUCT.ReorderLevel,
        SUPPLIER.SupplierName
    FROM PRODUCT
    JOIN SUPPLIER
        ON PRODUCT.SupplierID = SUPPLIER.SupplierID
    ORDER BY PRODUCT.ProductName
    """)

    products = cursor.fetchall()

    connection.close()

    for product in products:
        product_table.insert("", tk.END, values=product)

    product_table.pack(pady=5)

    def select_product(event):
        selected_items = product_table.selection()

        if not selected_items:
            return

        selected_item = selected_items[0]
        product = product_table.item(selected_item)["values"]

        product_name_entry.delete(0, tk.END)
        product_name_entry.insert(0, product[1])

        price_entry.delete(0, tk.END)
        price_entry.insert(0, product[2])

        quantity_entry.delete(0, tk.END)
        quantity_entry.insert(0, product[3])

        reorder_entry.delete(0, tk.END)
        reorder_entry.insert(0, product[4])

        for option in supplier_options:
            if option.endswith(f" - {product[5]}"):
                supplier_combo.set(option)
                break

    product_table.bind(
        "<<TreeviewSelect>>",
        select_product
    )

    # Update selected product
    def update_product():
        selected_items = product_table.selection()

        if not selected_items:
            messagebox.showerror(
                "No Product Selected",
                "Please select a product to update."
            )
            return

        selected_item = selected_items[0]
        product_id = product_table.item(selected_item)["values"][0]

        product_name = product_name_entry.get().strip()
        price = price_entry.get().strip()
        quantity = quantity_entry.get().strip()
        reorder_level = reorder_entry.get().strip()
        selected_supplier = supplier_combo.get()

        if (
            product_name == ""
            or price == ""
            or quantity == ""
            or reorder_level == ""
            or selected_supplier == ""
        ):
            messagebox.showerror(
                "Missing Information",
                "Please complete all product fields."
            )
            return

        try:
            price = float(price)
            quantity = int(quantity)
            reorder_level = int(reorder_level)

        except ValueError:
            messagebox.showerror(
                "Invalid Information",
                "Price must be a number and quantity values must be whole numbers."
            )
            return

        if price <= 0 or quantity < 0 or reorder_level < 0:
            messagebox.showerror(
                "Invalid Information",
                "Price must be greater than zero and stock values cannot be negative."
            )
            return

        supplier_id = int(selected_supplier.split(" - ")[0])

        connection = sqlite3.connect("brightmart.db")
        connection.execute("PRAGMA foreign_keys = ON")
        cursor = connection.cursor()

        cursor.execute("""
        UPDATE PRODUCT
        SET ProductName = ?,
            Price = ?,
            Quantity = ?,
            ReorderLevel = ?,
            SupplierID = ?
        WHERE ProductID = ?
        """, (
            product_name,
            price,
            quantity,
            reorder_level,
            supplier_id,
            product_id
        ))

        connection.commit()
        connection.close()

        messagebox.showinfo(
            "Product Updated",
            "Product updated successfully."
        )

        open_products(full_name, role)

         # Update Product button
    update_button = tk.Button(
        root,
        text="Update Product",
        width=15,
        command=update_product
    )
    update_button.pack(pady=5)

    # Delete selected product
    def delete_product():
        selected_items = product_table.selection()

        if not selected_items:
            messagebox.showerror(
                "No Product Selected",
                "Please select a product to delete."
            )
            return

        selected_item = selected_items[0]
        product = product_table.item(selected_item)["values"]

        product_id = product[0]
        product_name = product[1]

        confirm = messagebox.askyesno(
            "Confirm Delete",
            f"Are you sure you want to delete {product_name}?"
        )

        if not confirm:
            return

        connection = sqlite3.connect("brightmart.db")
        connection.execute("PRAGMA foreign_keys = ON")
        cursor = connection.cursor()

        try:
            cursor.execute(
                "DELETE FROM PRODUCT WHERE ProductID = ?",
                (product_id,)
            )

            connection.commit()

            messagebox.showinfo(
                "Product Deleted",
                "Product deleted successfully."
            )

        except sqlite3.IntegrityError:
            messagebox.showerror(
                "Cannot Delete Product",
                "This product is linked to an existing sales transaction."
            )

        finally:
            connection.close()

        open_products(full_name, role)


    # Delete Product button
    delete_button = tk.Button(
        root,
        text="Delete Product",
        width=15,
        command=delete_product
    )
    delete_button.pack(pady=5)

    # Back button
    back_button = tk.Button(
        root,
        text="Back to Dashboard",
        width=20,
        command=lambda: open_dashboard(full_name, role)
    )
    back_button.pack(pady=5)

def open_sales(full_name, role):
    # Clear current screen
    for widget in root.winfo_children():
        widget.destroy()

    # Heading
    title_label = tk.Label(
        root,
        text="Record Sale",
        font=("Arial", 22, "bold")
    )
    title_label.pack(pady=30)

    # Product
    product_label = tk.Label(
        root,
        text="Product"
    )
    product_label.pack()

    # Get products from database
    connection = sqlite3.connect("brightmart.db")
    cursor = connection.cursor()

    cursor.execute("""
    SELECT ProductID, ProductName, Price, Quantity
    FROM PRODUCT
    ORDER BY ProductName
    """)

    products = cursor.fetchall()

    connection.close()

    product_options = [
        f"{product[0]} - {product[1]}"
        for product in products
    ]

    product_combo = ttk.Combobox(
        root,
        values=product_options,
        width=30,
        state="readonly"
    )
    product_combo.pack(pady=5)

    # Quantity
    quantity_label = tk.Label(
        root,
        text="Quantity"
    )
    quantity_label.pack()

    sale_quantity_entry = tk.Entry(
        root,
        width=30
    )
    sale_quantity_entry.pack(pady=5)

        # Store items added to the current sale
    current_sale_items = []

    def add_item():
        selected_product = product_combo.get()
        quantity_text = sale_quantity_entry.get().strip()

        # Check required information
        if selected_product == "" or quantity_text == "":
            messagebox.showerror(
                "Missing Information",
                "Please select a product and enter a quantity."
            )
            return

        # Check quantity is a whole number
        try:
            quantity = int(quantity_text)
        except ValueError:
            messagebox.showerror(
                "Invalid Quantity",
                "Quantity must be a whole number."
            )
            return

        if quantity <= 0:
            messagebox.showerror(
                "Invalid Quantity",
                "Quantity must be greater than zero."
            )
            return

        # Get ProductID from dropdown
        product_id = int(selected_product.split(" - ")[0])

        # Find selected product details
        selected_product_data = None

        for product in products:
            if product[0] == product_id:
                selected_product_data = product
                break

        if selected_product_data is None:
            messagebox.showerror(
                "Product Error",
                "Selected product could not be found."
            )
            return

        product_name = selected_product_data[1]
        unit_price = float(selected_product_data[2])
        available_stock = int(selected_product_data[3])

        # Check available stock
        if quantity > available_stock:
            messagebox.showerror(
                "Insufficient Stock",
                f"Only {available_stock} units are available."
            )
            return

        # Calculate subtotal
        subtotal = unit_price * quantity

        # Add item to current sale
        current_sale_items.append({
            "ProductID": product_id,
            "ProductName": product_name,
            "Quantity": quantity,
            "UnitPrice": unit_price,
            "SubTotal": subtotal
        })

        # Calculate current total
        total = sum(
            item["SubTotal"]
            for item in current_sale_items
        )

        total_label.config(
            text=f"Total Amount: R{total:.2f}"
        )

        messagebox.showinfo(
            "Item Added",
            f"{product_name} added to the sale.\n"
            f"Quantity: {quantity}\n"
            f"Subtotal: R{subtotal:.2f}"
        )

        sale_quantity_entry.delete(0, tk.END)

            # Total
    total_label = tk.Label(
        root,
        text="Total Amount: R0.00",
        font=("Arial", 14, "bold")
    )
    total_label.pack(pady=10)

    # Store items added to the current sale
    current_sale_items = []

    # Function to add an item to the sale
    def add_item():
        selected_product = product_combo.get()
        quantity_text = sale_quantity_entry.get().strip()

        if selected_product == "" or quantity_text == "":
            messagebox.showerror(
                "Missing Information",
                "Please select a product and enter a quantity."
            )
            return

        try:
            quantity = int(quantity_text)

        except ValueError:
            messagebox.showerror(
                "Invalid Quantity",
                "Quantity must be a whole number."
            )
            return

        if quantity <= 0:
            messagebox.showerror(
                "Invalid Quantity",
                "Quantity must be greater than zero."
            )
            return

        product_id = int(selected_product.split(" - ")[0])

        selected_product_data = None

        for product in products:
            if product[0] == product_id:
                selected_product_data = product
                break

        if selected_product_data is None:
            messagebox.showerror(
                "Product Error",
                "Selected product could not be found."
            )
            return

        product_name = selected_product_data[1]
        unit_price = float(selected_product_data[2])
        available_stock = int(selected_product_data[3])

        if quantity > available_stock:
            messagebox.showerror(
                "Insufficient Stock",
                f"Only {available_stock} units are available."
            )
            return

        subtotal = unit_price * quantity

        current_sale_items.append({
            "ProductID": product_id,
            "ProductName": product_name,
            "Quantity": quantity,
            "UnitPrice": unit_price,
            "SubTotal": subtotal
        })

        total = sum(
            item["SubTotal"]
            for item in current_sale_items
        )

        total_label.config(
            text=f"Total Amount: R{total:.2f}"
        )

        messagebox.showinfo(
            "Item Added",
            f"{product_name} added to the sale.\n"
            f"Quantity: {quantity}\n"
            f"Subtotal: R{subtotal:.2f}"
        )

        sale_quantity_entry.delete(0, tk.END)


    # Add Item button
    add_item_button = tk.Button(
        root,
        text="Add Item",
        width=15,
        command=add_item
    )
    add_item_button.pack(pady=15)

        # Complete the current sale
    def complete_sale():
        if not current_sale_items:
            messagebox.showerror(
                "Empty Sale",
                "Please add at least one item before completing the sale."
            )
            return

        total_amount = sum(
            item["SubTotal"]
            for item in current_sale_items
        )

        connection = sqlite3.connect("brightmart.db")
        connection.execute("PRAGMA foreign_keys = ON")
        cursor = connection.cursor()

        low_stock_products = []

        try:
            connection.execute("BEGIN")

            sale_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            cursor.execute("""
            INSERT INTO SALE
            (SaleDate, UserID, TotalAmount)
            VALUES (?, ?, ?)
            """, (
                sale_date,
                root.current_user_id,
                total_amount
            ))

            sale_id = cursor.lastrowid

            for item in current_sale_items:
                product_id = item["ProductID"]
                quantity_sold = item["Quantity"]
                unit_price = item["UnitPrice"]
                subtotal = item["SubTotal"]

                # Check the latest stock quantity
                cursor.execute("""
                SELECT ProductName, Quantity, ReorderLevel
                FROM PRODUCT
                WHERE ProductID = ?
                """, (product_id,))

                product_record = cursor.fetchone()

                if product_record is None:
                    raise ValueError(
                        "A selected product could not be found."
                    )

                product_name = product_record[0]
                available_stock = product_record[1]
                reorder_level = product_record[2]

                if quantity_sold > available_stock:
                    raise ValueError(
                        f"Insufficient stock for {product_name}. "
                        f"Only {available_stock} units are available."
                    )

                # Save the sale item
                cursor.execute("""
                INSERT INTO SALE_ITEM
                (SaleID, ProductID, Quantity, UnitPrice, SubTotal)
                VALUES (?, ?, ?, ?, ?)
                """, (
                    sale_id,
                    product_id,
                    quantity_sold,
                    unit_price,
                    subtotal
                ))

                # Deduct stock
                new_quantity = available_stock - quantity_sold

                cursor.execute("""
                UPDATE PRODUCT
                SET Quantity = ?
                WHERE ProductID = ?
                """, (
                    new_quantity,
                    product_id
                ))

                # Check low-stock level
                if new_quantity <= reorder_level:
                    low_stock_products.append(
                        f"{product_name}: {new_quantity} remaining"
                    )

            connection.commit()

        except (sqlite3.Error, ValueError) as error:
            connection.rollback()

            messagebox.showerror(
                "Sale Failed",
                str(error)
            )

            connection.close()
            return

        connection.close()

        confirmation_message = (
            f"Sale completed successfully.\n"
            f"Sale ID: {sale_id}\n"
            f"Total: R{total_amount:.2f}"
        )

        if low_stock_products:
            confirmation_message += (
                "\n\nLow-stock warning:\n"
                + "\n".join(low_stock_products)
            )

        messagebox.showinfo(
            "Sale Completed",
            confirmation_message
        )

        # Reload the screen for a new sale
        open_sales(full_name, role)

    # Complete Sale
    complete_sale_button = tk.Button(
        root,
        text="Complete Sale",
        width=15,
        command=complete_sale
    )
    complete_sale_button.pack(pady=5)

    # Back
    back_button = tk.Button(
        root,
        text="Back to Dashboard",
        width=20,
        command=lambda: open_dashboard(full_name, role)
    )
    back_button.pack(pady=10)

def open_inventory(full_name, role):
    # Clear current screen
    for widget in root.winfo_children():
        widget.destroy()

    # Heading
    title_label = tk.Label(
        root,
        text="Inventory / Low Stock",
        font=("Arial", 22, "bold")
    )
    title_label.pack(pady=30)

    # Create inventory table
    columns = (
        "ProductID",
        "ProductName",
        "Quantity",
        "ReorderLevel",
        "Status"
    )

    inventory_table = ttk.Treeview(
        root,
        columns=columns,
        show="headings",
        height=12
    )

    inventory_table.heading("ProductID", text="ID")
    inventory_table.heading("ProductName", text="Product")
    inventory_table.heading("Quantity", text="Quantity")
    inventory_table.heading("ReorderLevel", text="Reorder Level")
    inventory_table.heading("Status", text="Status")

    inventory_table.column("ProductID", width=60)
    inventory_table.column("ProductName", width=180)
    inventory_table.column("Quantity", width=100)
    inventory_table.column("ReorderLevel", width=120)
    inventory_table.column("Status", width=120)

    inventory_table.pack(pady=15)

    # Read inventory from database
    connection = sqlite3.connect("brightmart.db")
    cursor = connection.cursor()

    cursor.execute("""
    SELECT
        ProductID,
        ProductName,
        Quantity,
        ReorderLevel
    FROM PRODUCT
    ORDER BY ProductName
    """)

    products = cursor.fetchall()

    connection.close()

    # Display inventory
    for product in products:
        product_id = product[0]
        product_name = product[1]
        quantity = product[2]
        reorder_level = product[3]

        if quantity <= reorder_level:
            status = "LOW STOCK"
        else:
            status = "In Stock"

        inventory_table.insert(
            "",
            tk.END,
            values=(
                product_id,
                product_name,
                quantity,
                reorder_level,
                status
            )
        )

    # Back button
    back_button = tk.Button(
        root,
        text="Back to Dashboard",
        width=20,
        command=lambda: open_dashboard(full_name, role)
    )
    back_button.pack(pady=15)

def open_reports(full_name, role):
        # Clear current screen
        for widget in root.winfo_children():
            widget.destroy()

        # Heading
        title_label = tk.Label(
            root,
            text="BrightMart Reports",
            font=("Arial", 22, "bold")
        )
        title_label.pack(pady=20)

        # Report description
        report_status_label = tk.Label(
            root,
            text="Select a report to display.",
            font=("Arial", 11)
        )
        report_status_label.pack(pady=5)

        # Generic report table
        report_columns = ("Column1", "Column2", "Column3", "Column4", "Column5")

        report_table = ttk.Treeview(
            root,
            columns=report_columns,
            show="headings",
            height=12
        )

        report_table.pack(pady=15)

        # Clear existing rows before loading another report
        def clear_report():
            for row in report_table.get_children():
                report_table.delete(row)

        # Configure table headings
        def configure_table(headings):
            for index, column in enumerate(report_columns):
                heading = headings[index] if index < len(headings) else ""

                report_table.heading(
                    column,
                    text=heading
                )

                report_table.column(
                    column,
                    width=150
                )

        # Display daily sales
        def show_daily_sales():
            clear_report()

            configure_table([
                "Sale ID",
                "Date",
                "Recorded By",
                "Total Amount",
                ""
            ])

            connection = sqlite3.connect("brightmart.db")
            cursor = connection.cursor()

            cursor.execute("""
            SELECT
                SALE.SaleID,
                SALE.SaleDate,
                USER.FullName,
                SALE.TotalAmount
            FROM SALE
            JOIN USER
                ON SALE.UserID = USER.UserID
            WHERE DATE(SALE.SaleDate) = DATE('now', 'localtime')
            ORDER BY SALE.SaleDate DESC
            """)

            sales = cursor.fetchall()
            connection.close()

            for sale in sales:
                report_table.insert(
                    "",
                    tk.END,
                    values=(
                        sale[0],
                        sale[1],
                        sale[2],
                        f"R{sale[3]:.2f}",
                        ""
                    )
                )

            total = sum(sale[3] for sale in sales)

            report_status_label.config(
                text=f"Daily Sales: {len(sales)} sale(s) | Total: R{total:.2f}"
            )

        # Display sales from the last 7 days
        def show_weekly_sales():
            clear_report()

            configure_table([
                "Sale ID",
                "Date",
                "Recorded By",
                "Total Amount",
                ""
            ])

            connection = sqlite3.connect("brightmart.db")
            cursor = connection.cursor()

            cursor.execute("""
            SELECT
                SALE.SaleID,
                SALE.SaleDate,
                USER.FullName,
                SALE.TotalAmount
            FROM SALE
            JOIN USER
                ON SALE.UserID = USER.UserID
            WHERE DATETIME(SALE.SaleDate)
                  >= DATETIME('now', '-6 days', 'localtime')
            ORDER BY SALE.SaleDate DESC
            """)

            sales = cursor.fetchall()
            connection.close()

            for sale in sales:
                report_table.insert(
                    "",
                    tk.END,
                    values=(
                        sale[0],
                        sale[1],
                        sale[2],
                        f"R{sale[3]:.2f}",
                        ""
                    )
                )

            total = sum(sale[3] for sale in sales)

            report_status_label.config(
                text=f"Last 7 Days: {len(sales)} sale(s) | Total: R{total:.2f}"
            )

        # Display current inventory
        def show_inventory_report():
            clear_report()

            configure_table([
                "Product ID",
                "Product",
                "Quantity",
                "Reorder Level",
                "Status"
            ])

            connection = sqlite3.connect("brightmart.db")
            cursor = connection.cursor()

            cursor.execute("""
            SELECT
                ProductID,
                ProductName,
                Quantity,
                ReorderLevel
            FROM PRODUCT
            ORDER BY ProductName
            """)

            products = cursor.fetchall()
            connection.close()

            for product in products:
                product_id = product[0]
                product_name = product[1]
                quantity = product[2]
                reorder_level = product[3]

                if quantity <= reorder_level:
                    status = "LOW STOCK"
                else:
                    status = "In Stock"

                report_table.insert(
                    "",
                    tk.END,
                    values=(
                        product_id,
                        product_name,
                        quantity,
                        reorder_level,
                        status
                    )
                )

            report_status_label.config(
                text=f"Current Inventory: {len(products)} product(s)"
            )

        # Display only low-stock products
        def show_low_stock_report():
            clear_report()

            configure_table([
                "Product ID",
                "Product",
                "Quantity",
                "Reorder Level",
                "Status"
            ])

            connection = sqlite3.connect("brightmart.db")
            cursor = connection.cursor()

            cursor.execute("""
            SELECT
                ProductID,
                ProductName,
                Quantity,
                ReorderLevel
            FROM PRODUCT
            WHERE Quantity <= ReorderLevel
            ORDER BY ProductName
            """)

            products = cursor.fetchall()
            connection.close()

            for product in products:
                report_table.insert(
                    "",
                    tk.END,
                    values=(
                        product[0],
                        product[1],
                        product[2],
                        product[3],
                        "LOW STOCK"
                    )
                )

            report_status_label.config(
                text=f"Low-Stock Products: {len(products)} product(s)"
            )

        # Report buttons
        button_frame = tk.Frame(root)
        button_frame.pack(pady=5)

        daily_button = tk.Button(
            button_frame,
            text="Daily Sales",
            width=16,
            command=show_daily_sales
        )
        daily_button.grid(row=0, column=0, padx=5, pady=5)

        weekly_button = tk.Button(
            button_frame,
            text="Last 7 Days",
            width=16,
            command=show_weekly_sales
        )
        weekly_button.grid(row=0, column=1, padx=5, pady=5)

        inventory_report_button = tk.Button(
            button_frame,
            text="Current Inventory",
            width=16,
            command=show_inventory_report
        )
        inventory_report_button.grid(row=1, column=0, padx=5, pady=5)

        low_stock_report_button = tk.Button(
            button_frame,
            text="Low Stock",
            width=16,
            command=show_low_stock_report
        )
        low_stock_report_button.grid(row=1, column=1, padx=5, pady=5)

        # Back button
        back_button = tk.Button(
            root,
            text="Back to Dashboard",
            width=20,
            command=lambda: open_dashboard(full_name, role)
        )
        back_button.pack(pady=10)


def open_dashboard(full_name, role):
    # Remove the login screen
    for widget in root.winfo_children():
        widget.destroy()

    # Dashboard heading
    dashboard_title = tk.Label(
        root,
        text="BrightMart Dashboard",
        font=("Arial", 22, "bold")
    )
    dashboard_title.pack(pady=30)

    # Logged-in user
    welcome_label = tk.Label(
        root,
        text=f"Welcome {full_name} | Role: {role}",
        font=("Arial", 12)
    )
    welcome_label.pack(pady=10)

        # Store Manager functions
    if role == "Store Manager":

        products_button = tk.Button(
            root,
            text="Products",
            width=20,
            height=2,
            command=lambda: open_products(full_name, role)
        )
        products_button.pack(pady=5)

        suppliers_button = tk.Button(
            root,
            text="Suppliers",
            width=20,
            height=2,
            command=lambda: open_suppliers(full_name, role)
        )
        suppliers_button.pack(pady=5)

        sales_button = tk.Button(
            root,
            text="Record Sale",
            width=20,
            height=2,
            command=lambda: open_sales(full_name, role)
        )
        sales_button.pack(pady=5)

        inventory_button = tk.Button(
            root,
            text="Inventory / Low Stock",
            width=20,
            height=2,
            command=lambda: open_inventory(full_name, role)
        )
        inventory_button.pack(pady=5)

        reports_button = tk.Button(
            root,
            text="Reports",
            width=20,
            height=2,
            command=lambda: open_reports(full_name, role)
        )
        reports_button.pack(pady=5)

    # Sales Staff functions
    elif role == "Sales Staff":

        sales_button = tk.Button(
            root,
            text="Record Sale",
            width=20,
            height=2,
            command=lambda: open_sales(full_name, role)
        )
        sales_button.pack(pady=5)

        inventory_button = tk.Button(
            root,
            text="Inventory / Low Stock",
            width=20,
            height=2,
            command=lambda: open_inventory(full_name, role)
        )
        inventory_button.pack(pady=5)

    # Business Owner functions
    elif role == "Business Owner":

        inventory_button = tk.Button(
            root,
            text="Inventory / Low Stock",
            width=20,
            height=2,
            command=lambda: open_inventory(full_name, role)
        )
        inventory_button.pack(pady=5)

        reports_button = tk.Button(
            root,
            text="Reports",
            width=20,
            height=2,
            command=lambda: open_reports(full_name, role)
        )
        reports_button.pack(pady=5)

def login():
    username = username_entry.get()
    password = password_entry.get()

    connection = sqlite3.connect("brightmart.db")
    cursor = connection.cursor()

    cursor.execute(
        "SELECT UserID, FullName, Role FROM USER WHERE Username = ? AND Password = ?",
        (username, password)
    )

    user = cursor.fetchone()

    connection.close()

    if user:
        user_id = user[0]
        full_name = user[1]
        role = user[2]

        root.current_user_id = user_id

        open_dashboard(full_name, role)

    else:
        messagebox.showerror(
            "Login Failed",
            "Incorrect username or password."
        )

# Create main window
root = tk.Tk()

root.title("BrightMart Inventory & Sales Management System")
root.geometry("900x700")

# Main heading
title_label = tk.Label(
    root,
    text="BrightMart Inventory & Sales Management System",
    font=("Arial", 20, "bold")
)
title_label.pack(pady=50)

# Login heading
login_label = tk.Label(
    root,
    text="Login",
    font=("Arial", 16, "bold")
)
login_label.pack(pady=10)

# Username
username_label = tk.Label(root, text="Username")
username_label.pack()

username_entry = tk.Entry(root, width=30)
username_entry.pack(pady=5)

# Password
password_label = tk.Label(root, text="Password")
password_label.pack()

password_entry = tk.Entry(root, width=30, show="*")
password_entry.pack(pady=5)

# Login button
login_button = tk.Button(
    root,
    text="Login",
    width=15,
    command=login
)
login_button.pack(pady=20)

# Keep window open
root.mainloop()