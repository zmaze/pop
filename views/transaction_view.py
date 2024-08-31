import tkinter as tk
from tkinter import ttk

class TransactionView(tk.Toplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.title("View Transactions")
        self.geometry("400x300")
        self.create_widgets()

    def create_widgets(self):
        label = ttk.Label(self, text="View transactions here.", font=("Helvetica", 12))
        label.pack(pady=20)
