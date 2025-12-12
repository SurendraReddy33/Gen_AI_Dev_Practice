from datetime import datetime

def log_transaction(func):
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        print(f"[{datetime.now()}] {func.__name__} is executed")
        return result

    return wrapper

class Bank:
    def __init__(self, name):
        self.name = name
        self.customers = []

    @log_transaction
    def add_customer(self, customer):
        self.customers.append(customer)

class customer:
    def __init__(self, name, balance):
        self.name = name
        self.balance = balance

    @log_transaction
    def deposit(self, amount):
        self.balance = amount

    @log_transaction
    def withdraw(self, amount):
        self.balance = amount


statebank = Bank("State Bank of India")

surendra_account = customer("Surendra", 50000)
statebank.add_customer(surendra_account)

vonna_account = customer("vonna", 30000)
statebank.add_customer(vonna_account)

surendra_account.deposit(50000)
vonna_account.deposit(100000)

surendra_account.withdraw(1000)
vonna_account.withdraw(5000)

