import tkinter as tk
from tkinter import ttk, messagebox
from views.product_view import ProductView
from views.transaction_view import TransactionView
from services.inventory_service import InventoryService
from services.report_service import ReportService
from datetime import datetime

class MainView(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.inventory_service = InventoryService()
        self.transactions = []
        self.pack(fill="both", expand=True)
        self.create_widgets()

    def create_widgets(self):
        self.create_menu()
        self.create_dashboard()
        self.create_status_bar()

    def create_menu(self):
        menu_bar = tk.Menu(self.master)
        self.master.config(menu=menu_bar)

        file_menu = tk.Menu(menu_bar, tearoff=0)
        file_menu.add_command(label="Exit", command=self.master.quit)
        menu_bar.add_cascade(label="File", menu=file_menu)

        help_menu = tk.Menu(menu_bar, tearoff=0)
        help_menu.add_command(label="About", command=self.show_about)
        menu_bar.add_cascade(label="Help", menu=help_menu)

    def create_dashboard(self):
        dashboard_frame = ttk.Frame(self, padding="10")
        dashboard_frame.pack(fill="both", expand=True)

        title_label = ttk.Label(dashboard_frame, text="Medical Retail POS System", font=("Helvetica", 18, "bold"))
        title_label.pack(pady=10)

        welcome_label = ttk.Label(dashboard_frame, text=f"Welcome! Today's Date: {datetime.now().strftime('%Y-%m-%d')}", font=("Helvetica", 14))
        welcome_label.pack(pady=5)

        metrics_frame = ttk.Frame(dashboard_frame, padding="10")
        metrics_frame.pack(fill="both", expand=True, pady=20)

        total_sales_label = ttk.Label(metrics_frame, text="Total Sales: $0.00", font=("Helvetica", 12))
        total_sales_label.grid(row=0, column=0, padx=20)

        top_selling_label = ttk.Label(metrics_frame, text="Top-Selling Product: N/A", font=("Helvetica", 12))
        top_selling_label.grid(row=0, column=1, padx=20)

        stock_alert_label = ttk.Label(metrics_frame, text="Stock Alerts: None", font=("Helvetica", 12))
        stock_alert_label.grid(row=0, column=2, padx=20)

        expiry_alert_label = ttk.Label(metrics_frame, text="Expiry Alerts: None", font=("Helvetica", 12))
        expiry_alert_label.grid(row=1, column=0, padx=20)

        shortcuts_frame = ttk.Frame(dashboard_frame, padding="10")
        shortcuts_frame.pack(fill="both", expand=True, pady=20)

        manage_products_button = ttk.Button(shortcuts_frame, text="Manage Products", command=self.open_product_view)
        manage_products_button.grid(row=0, column=0, padx=10, pady=10)

        view_transactions_button = ttk.Button(shortcuts_frame, text="View Transactions", command=self.open_transaction_view)
        view_transactions_button.grid(row=0, column=1, padx=10, pady=10)

        generate_report_button = ttk.Button(shortcuts_frame, text="Generate Report", command=self.generate_report)
        generate_report_button.grid(row=0, column=2, padx=10, pady=10)

        stock_alerts_button = ttk.Button(shortcuts_frame, text="Stock Alerts", command=self.show_stock_alerts)
        stock_alerts_button.grid(row=1, column=0, padx=10, pady=10)

        expiry_alerts_button = ttk.Button(shortcuts_frame, text="Expiry Alerts", command=self.show_expiry_alerts)
        expiry_alerts_button.grid(row=1, column=1, padx=10, pady=10)

        export_report_button = ttk.Button(shortcuts_frame, text="Export Report to CSV", command=self.export_report_to_csv)
        export_report_button.grid(row=1, column=2, padx=10, pady=10)

    def create_status_bar(self):
        status_bar = tk.Label(self.master, text="Ready", bd=1, relief=tk.SUNKEN, anchor=tk.W)
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)

    def show_about(self):
        messagebox.showinfo("About", "Medical Retail POS System v2.0\nDeveloped by [Your Name]")

    def open_product_view(self):
        ProductView(self.master)

    def open_transaction_view(self):
        TransactionView(self.master)

    def update_inventory(self, product_id, quantity_sold):
        updated = self.inventory_service.update_inventory(product_id, quantity_sold)
        if updated:
            low_stock_products = self.inventory_service.check_stock_levels()
            if low_stock_products.size > 0:
                low_stock_names = ", ".join(low_stock_products[:, 1])
                messagebox.showwarning("Low Stock Alert", f"Low stock on: {low_stock_names}")

    def show_stock_alerts(self):
        low_stock_products = self.inventory_service.check_stock_levels()
        if low_stock_products.size > 0:
            low_stock_names = ", ".join(low_stock_products[:, 1])
            messagebox.showinfo("Stock Alerts", f"Low stock on: {low_stock_names}")
        else:
            messagebox.showinfo("Stock Alerts", "All products are sufficiently stocked.")

    def show_expiry_alerts(self):
        # Implement expiry alert logic here (placeholder)
        messagebox.showinfo("Expiry Alerts", "No products are nearing expiration.")

    def generate_report(self):
        report_service = ReportService(self.transactions)
        report_data = report_service.generate_sales_report()
        report_text = f"Total Sales: ${report_data['total_sales']}\n"
        report_text += f"Average Sale: ${report_data['average_sale']}\n"
        report_text += f"Max Sale: ${report_data['max_sale']}"
        messagebox.showinfo("Sales Report", report_text)

    def export_report_to_csv(self):
        report_service = ReportService(self.transactions)
        report_service.export_to_csv('sales_report.csv')
        messagebox.showinfo("Export Successful", "Sales report has been exported to sales_report.csv")

    def open_product_view(self):
         ProductView(self.master)


