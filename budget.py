class Category:
    def __init__(self, category_name):
        self.category_name = category_name
        self.ledger = []

    def deposit(self, amount, description=""):
        self.ledger.append({"amount": amount, "description": description})

    def withdraw(self, amount, description=""):
        if self.check_funds(amount):
            self.ledger.append({"amount": -amount, "description": description})
            return True
        return False

    def get_balance(self):
        balance = 0
        for transaction in self.ledger:
            balance += transaction["amount"]
        return balance

    def transfer(self, amount, category):
        if self.check_funds(amount):
            self.withdraw(amount, f"Transfer to {category.category_name}")
            category.deposit(amount, f"Transfer from {self.category_name}")
            return True
        return False

    def check_funds(self, amount):
        return amount <= self.get_balance()

    def get_withdrawals(self):
      withdrawals = 0
      for item in self.ledger:
          if item["amount"] < 0:
              withdrawals += item["amount"]
      return abs(withdrawals)


    def __str__(self):
        title = f"{self.category_name:*^30}\n"
        items = ""
        total = 0
        for transaction in self.ledger:
            items += f"{transaction['description'][:23]:23}" + \
                f"{transaction['amount']:>7.2f}\n"
            total += transaction['amount']
        output = title + items + "Total: " + str(total)
        return output

def create_spend_chart(categories):
    # Calculate total withdrawals and percentages for each category
    total_withdrawals = sum(category.get_withdrawals() for category in categories)
    percentages = [category.get_withdrawals() / total_withdrawals * 100 for category in categories]
    rounded_percentages = [int(percent // 10) * 10 for percent in percentages]

    # Create bar chart
    chart = "Percentage spent by category\n"
    for i in range(100, -10, -10):
        chart += "{:>3d}| ".format(i)
        for percentage in rounded_percentages:
            if percentage >= i:
                chart += "o  "
            else:
                chart += "   "
        chart += "\n"

    # Add horizontal line and category names
    chart += "    " + "-" * (len(categories) * 3 + 1) + "\n"
    max_name_length = max(len(category.category_name) for category in categories)
    for i in range(max_name_length):
        chart += "     "
        for category in categories:
            if i < len(category.category_name):
                chart += category.category_name[i] + "  "
            else:
                chart += "   "
        chart += "\n"

    return chart.rstrip("\n")

