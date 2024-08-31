import tkinter as tk
from tkinter import ttk, messagebox
from tkinter import font as tkfont  # Import the font module
from services.inventory_service import InventoryService
# Ensure AddProductView, EditProductView, and SearchProductView are imported or defined elsewhere

class ProductView(tk.Toplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.title("Manage Products")
        self.geometry("600x400")
        self.inventory_service = InventoryService()
        self.create_widgets()

    def create_widgets(self):
        options_frame = ttk.Frame(self, padding="10")
        options_frame.pack(side=tk.TOP, fill=tk.X)

        add_button = ttk.Button(options_frame, text="Add Product", command=self.add_product)
        add_button.pack(side=tk.LEFT, padx=5, pady=5)

        edit_button = ttk.Button(options_frame, text="Edit Product", command=self.edit_product)
        edit_button.pack(side=tk.LEFT, padx=5, pady=5)

        delete_button = ttk.Button(options_frame, text="Delete Product", command=self.delete_product)
        delete_button.pack(side=tk.LEFT, padx=5, pady=5)

        search_button = ttk.Button(options_frame, text="Search Product", command=self.search_product)
        search_button.pack(side=tk.LEFT, padx=5, pady=5)

        list_frame = ttk.Frame(self, padding="10")
        list_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # Scrollbars
        self.v_scrollbar = ttk.Scrollbar(list_frame, orient="vertical")
        self.v_scrollbar.pack(side="right", fill="y")

        self.h_scrollbar = ttk.Scrollbar(list_frame, orient="horizontal")
        self.h_scrollbar.pack(side="bottom", fill="x")

        columns = ('Product ID', 'Name', 'Price', 'Quantity')
        self.product_tree = ttk.Treeview(list_frame, columns=columns, show='headings',
                                         yscrollcommand=self.v_scrollbar.set,
                                         xscrollcommand=self.h_scrollbar.set)
        self.product_tree.pack(fill=tk.BOTH, expand=True)

        # Attach scrollbars to Treeview
        self.v_scrollbar.config(command=self.product_tree.yview)
        self.h_scrollbar.config(command=self.product_tree.xview)

        # Define headings
        for col in columns:
            self.product_tree.heading(col, text=col)
            self.product_tree.column(col, minwidth=100, stretch=True)  # Autofit columns

        self.load_products()

    def load_products(self):
        for row in self.product_tree.get_children():
            self.product_tree.delete(row)

        products = self.inventory_service.get_all_products()
        for product in products:
            self.product_tree.insert('', tk.END, values=product)

        # Autofit columns
        font = tkfont.Font()
        for col in self.product_tree["columns"]:
            self.product_tree.column(col, width=tkfont.Font().measure(col))
            for item in self.product_tree.get_children():
                item_width = tkfont.Font().measure(self.product_tree.set(item, col))
                if self.product_tree.column(col, width=None) < item_width:
                    self.product_tree.column(col, width=item_width)

    def add_product(self):
        AddProductView(self, self.inventory_service, self.load_products)

    def edit_product(self):
        selected_item = self.product_tree.selection()
        if selected_item:
            product_id = self.product_tree.item(selected_item)['values'][0]
            EditProductView(self, self.inventory_service, product_id, self.load_products)
        else:
            messagebox.showwarning("No Selection", "Please select a product to edit.")

    def delete_product(self):
        selected_item = self.product_tree.selection()
        if selected_item:
            product_id = self.product_tree.item(selected_item)['values'][0]
            self.inventory_service.delete_product(product_id)
            self.load_products()
            messagebox.showinfo("Deleted", "Product has been deleted.")
        else:
            messagebox.showwarning("No Selection", "Please select a product to delete.")

    def search_product(self):
        SearchProductView(self, self.inventory_service, self.load_products)

class AddProductView(tk.Toplevel):
    def __init__(self, master, inventory_service, reload_callback):
        super().__init__(master)
        self.title("Add Product")
        self.geometry("400x300")
        self.inventory_service = inventory_service
        self.reload_callback = reload_callback
        self.create_widgets()

    def create_widgets(self):
        ttk.Label(self, text="Product Name:").pack(pady=10)
        self.name_entry = ttk.Entry(self)
        self.name_entry.pack(pady=10)

        ttk.Label(self, text="Price:").pack(pady=10)
        self.price_entry = ttk.Entry(self)
        self.price_entry.pack(pady=10)

        ttk.Label(self, text="Quantity:").pack(pady=10)
        self.quantity_entry = ttk.Entry(self)
        self.quantity_entry.pack(pady=10)

        submit_button = ttk.Button(self, text="Add Product", command=self.submit_product)
        submit_button.pack(pady=20)

    def submit_product(self):
        name = self.name_entry.get()
        price = float(self.price_entry.get())
        quantity = int(self.quantity_entry.get())

        self.inventory_service.add_product(name, price, quantity)
        self.reload_callback()
        self.destroy()

class EditProductView(tk.Toplevel):
    def __init__(self, master, inventory_service, product_id, reload_callback):
        super().__init__(master)
        self.title("Edit Product")
        self.geometry("400x300")
        self.inventory_service = inventory_service
        self.product_id = product_id
        self.reload_callback = reload_callback
        self.product = self.inventory_service.get_product_by_id(product_id)
        self.create_widgets()

    def create_widgets(self):
        ttk.Label(self, text="Product Name:").pack(pady=10)
        self.name_entry = ttk.Entry(self)
        self.name_entry.insert(0, self.product[1])
        self.name_entry.pack(pady=10)

        ttk.Label(self, text="Price:").pack(pady=10)
        self.price_entry = ttk.Entry(self)
        self.price_entry.insert(0, self.product[2])
        self.price_entry.pack(pady=10)

        ttk.Label(self, text="Quantity:").pack(pady=10)
        self.quantity_entry = ttk.Entry(self)
        self.quantity_entry.insert(0, self.product[3])
        self.quantity_entry.pack(pady=10)

        submit_button = ttk.Button(self, text="Update Product", command=self.submit_product)
        submit_button.pack(pady=20)

    def submit_product(self):
        name = self.name_entry.get()
        price = float(self.price_entry.get())
        quantity = int(self.quantity_entry.get())

        self.inventory_service.update_product(self.product_id, name, price, quantity)
        self.reload_callback()
        self.destroy()

class SearchProductView(tk.Toplevel):
    def __init__(self, master, inventory_service, reload_callback):
        super().__init__(master)
        self.title("Search Product")
        self.geometry("400x200")
        self.inventory_service = inventory_service
        self.reload_callback = reload_callback
        self.create_widgets()

    def create_widgets(self):
        ttk.Label(self, text="Enter Product Name:").pack(pady=10)
        self.name_entry = ttk.Entry(self)
        self.name_entry.pack(pady=10)

        search_button = ttk.Button(self, text="Search", command=self.search_product)
        search_button.pack(pady=20)

    def search_product(self):
        name = self.name_entry.get()
        products = self.inventory_service.search_product(name)

        if products:
            results = "\n".join([f"{p[1]}: {p[2]} units" for p in products])
            messagebox.showinfo("Search Results", results)
        else:
            messagebox.showinfo("Search Results", "No products found.")

        self.reload_callback()
        self.destroy()
