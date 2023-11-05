class Category:
    def __init__(self, name):
        self.name = name
        self.total = 0.0
        self.ledger = []

    def __repr__(self):
        s = f"{self.name:*^30}\n"
        acc = 0
        for item in self.ledger:
          description = item['description'][:23]  # Truncate description if it exceeds 23 characters
          amount = f"{item['amount']:.2f}"  # Format amount as a float with two decimal places
          s += f"{description}{amount:>{30-len(description)}}\n"
          acc += item["amount"]
        s += f"Total: {acc:.2f}"
        return s
        

    def deposit(self, amount, *args):
        description = args[0] if args else ""
        self.total += amount
        self.ledger.append({"amount": amount, "description": description})
        
    def withdraw(self, amount, *args):
        can_withdraw = self.check_funds(amount)
        description = args[0] if args else "" 
            
        if can_withdraw:
            self.total -= amount
            self.ledger.append({"amount": -amount, "description": description})
        return can_withdraw
        
    def get_balance(self):
        return self.total

    def transfer(self, amount, instance):
        can_transfer = self.check_funds(amount)
        if can_transfer:
            self.withdraw(amount, f"Transfer to {instance.name}")
            instance.deposit(amount, f"Transfer from {self.name}")
        return can_transfer

    def check_funds(self, amount):
        if amount > self.total:
            return False
        return True

cat = Category("Food")

def create_spend_chart(categories):
    string = "Percentage spent by category\n"

    total = 0
    cats = {}

    # Calculate total spending in each category
    for cat in categories:
        cat_total = 0
        for item in cat.ledger:
            if item["amount"] < 0:
                total += item["amount"]
                cat_total += item["amount"]
        cats[cat.name] = abs(cat_total)

    total = abs(total)

    # Calculate the percentage spent in each category
    for key, val in cats.items():
        percent = (val / total) * 100
        cats[key] = percent

    # Build the spending chart
    for n in range(100, -1, -10):
        string += f"{str(n)+'|':>4}"
        for val in cats.values():
            if val >= n:
                string += " o "
            else:
                string += "   "
        string += " \n"

    # Add the horizontal line
    string += "    " + "---" * len(categories) + "-\n"

    # Get the maximum length of category names
    max_len = max(len(cat.name) for cat in categories)

    # Add category names with one space between them
    for i in range(max_len):
        string += "     "
        for cat in categories:
            if i < len(cat.name):
                string += cat.name[i] + "  "
            else:
                string += "   "
        if i < max_len - 1:  # Add a newline unless it's the last character
            string += "\n"


    return string