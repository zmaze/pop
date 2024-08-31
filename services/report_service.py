import csv

class ReportService:
    def __init__(self, transactions):
        self.transactions = transactions

    def generate_sales_report(self):
        total_sales = sum(transaction['total'] for transaction in self.transactions)
        average_sale = total_sales / len(self.transactions) if self.transactions else 0
        max_sale = max(transaction['total'] for transaction in self.transactions) if self.transactions else 0

        return {
            "total_sales": total_sales,
            "average_sale": average_sale,
            "max_sale": max_sale
        }

    def export_to_csv(self, file_name='sales_report.csv'):
        with open(file_name, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Transaction ID", "Product ID", "Quantity Sold", "Total Sale"])
            for transaction in self.transactions:
                writer.writerow([transaction['id'], transaction['product_id'], transaction['quantity'], transaction['total']])
