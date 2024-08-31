class InventoryService:
    def __init__(self):
        self.products = []  # Example: [("1", "Product A", 100.0, 50)]

    def get_all_products(self):
        return self.products

    def add_product(self, name, price, quantity):
        product_id = len(self.products) + 1
        self.products.append((product_id, name, price, quantity))

    def get_product_by_id(self, product_id):
        for product in self.products:
            if product[0] == product_id:
                return product
        return None

    def update_product(self, product_id, name, price, quantity):
        for i, product in enumerate(self.products):
            if product[0] == product_id:
                self.products[i] = (product_id, name, price, quantity)

    def delete_product(self, product_id):
        self.products = [p for p in self.products if p[0] != product_id]

    def search_product(self, name):
        return [p for p in self.products if name.lower() in p[1].lower()]

    def check_stock_levels(self):
        return [p for p in self.products if p[3] <= 5]  # Example stock level check
