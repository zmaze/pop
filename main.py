import tkinter as tk
from views.main_view import MainView

def main():
    root = tk.Tk()
    root.title("Medical Retail POS System")
    root.geometry("800x600")
    
    # Load icon if available
    try:
        root.iconbitmap("assets/icon.png")
    except Exception as e:
        print("Icon not found, proceeding without it.")
    
    app = MainView(master=root)
    app.mainloop()

if __name__ == "__main__":
    main()
