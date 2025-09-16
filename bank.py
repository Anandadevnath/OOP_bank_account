import os
import json
from datetime import datetime

class Account:
    def __init__(self, account_number, balance, customer_id):
        self.account_number = account_number
        self.balance = balance
        self.customer_id = customer_id

    def deposit(self, amount):
        if amount <= 0:
            raise ValueError("Deposit amount must be positive.")
        self.balance += amount

    def withdraw(self, amount):
        if amount <= 0:
            raise ValueError("Withdrawal amount must be positive.")
        if amount > self.balance:
            raise ValueError("Insufficient balance.")
        self.balance -= amount

    def get_balance(self):
        return self.balance

class SavingAccount(Account):
    interestRate = 0.03 

    def __init__(self, account_number, balance, customer_id, **kwargs):
        super().__init__(account_number, balance, customer_id)
    def addMonthlyInterest(self):
        monthly_interest = self.balance * (SavingAccount.interestRate / 12)
        self.balance += monthly_interest
        return monthly_interest

class CurrentAccount(Account):
    def __init__(self, account_number, balance, customer_id, overdraw_limit, **kwargs):
        super().__init__(account_number, balance, customer_id)
        self.overdraw_limit = overdraw_limit

    def withdraw(self, amount):
        if amount <= 0:
            raise ValueError("Withdrawal amount must be positive.")
        if amount > self.balance + self.overdraw_limit:
            raise ValueError("Exceeds overdraw limit.")
        self.balance -= amount

class Customer:
    def __init__(self, customer_id, name, address, contact, accounts=None):
        self.customer_id = customer_id
        self.name = name
        self.address = address
        self.contact = contact
        self.accounts = accounts if accounts is not None else []

    def add_account(self, account_number):
        self.accounts.append(account_number)

class Transaction:
    def __init__(self, transaction_id, timestamp, account_number, transaction_type, amount):
        self.transaction_id = transaction_id
        self.timestamp = timestamp
        self.account_number = account_number
        self.transaction_type = transaction_type
        self.amount = amount

class BankApp:
    def __init__(self):
        self.customers = {}
        self.accounts = {}
        self.transactions = []
        self.load_data()
    def load_data(self):
        if os.path.exists('customers.txt'):
            with open('customers.txt', 'r') as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    data = json.loads(line)
                    customer = Customer(**data)
                    self.customers[customer.customer_id] = customer
        if os.path.exists('saving_accounts.txt'):
            with open('saving_accounts.txt', 'r') as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    data = json.loads(line)
                    acc = SavingAccount(**data)
                    self.accounts[acc.account_number] = acc
        if os.path.exists('current_accounts.txt'):
            with open('current_accounts.txt', 'r') as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    data = json.loads(line)
                    acc = CurrentAccount(**data)
                    self.accounts[acc.account_number] = acc
        if os.path.exists('transactions.txt'):
            with open('transactions.txt', 'r') as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    data = json.loads(line)
                    txn = Transaction(**data)
                    self.transactions.append(txn)
                    data = json.loads(line)
                    txn = Transaction(**data)
                    self.transactions.append(txn)

    def save_data(self):
        with open('customers.txt', 'w') as f:
            for customer in self.customers.values():
                f.write(json.dumps(customer.__dict__) + '\n')
        with open('saving_accounts.txt', 'w') as f:
            for acc in self.accounts.values():
                if isinstance(acc, SavingAccount):
                    f.write(json.dumps(acc.__dict__) + '\n')
        with open('current_accounts.txt', 'w') as f:
            for acc in self.accounts.values():
                if isinstance(acc, CurrentAccount):
                    f.write(json.dumps(acc.__dict__) + '\n')
        with open('transactions.txt', 'w') as f:
            for txn in self.transactions:
                f.write(json.dumps(txn.__dict__) + '\n')

    def run(self):
        print("Welcome to the Command Line Bank Application!")
        while True:
            print("\nOptions:")
            print("1. Create Customer")
            print("2. Create Account")
            print("3. Make Transaction")
            print("4. Check Balance")
            print("5. View Transaction History")
            print("6. Exit")
            choice = input("Enter your choice: ")
            try:
                if choice == '1':
                    self.create_customer()
                elif choice == '2':
                    self.create_account()
                elif choice == '3':
                    self.make_transaction()
                elif choice == '4':
                    self.check_balance()
                elif choice == '5':
                    self.view_transactions()
                elif choice == '6':
                    self.save_data()
                    print("Goodbye!")
                    break
                else:
                    print("Invalid choice. Try again.")
            except Exception as e:
                print(f"Error: {e}")

    def create_customer(self):
        customer_id = input("Enter customer ID: ")
        name = input("Enter name: ")
        address = input("Enter address: ")
        contact = input("Enter contact: ")
        customer = Customer(customer_id, name, address, contact)
        self.customers[customer_id] = customer
        print("Customer created.")
        self.save_data()

    def create_account(self):
        customer_id = input("Enter customer ID: ")
        if customer_id not in self.customers:
            print("Customer not found.")
            return
        acc_type = input("Account type (saving/current): ").lower()
        account_number = input("Enter account number: ")
        balance = float(input("Enter initial balance: "))
        if acc_type == 'saving':
            acc = SavingAccount(account_number, balance, customer_id)
            self.accounts[account_number] = acc
        elif acc_type == 'current':
            overdraw_limit = float(input("Enter overdraw limit: "))
            acc = CurrentAccount(account_number, balance, customer_id, overdraw_limit)
            self.accounts[account_number] = acc
        else:
            print("Invalid account type.")
            return
        self.customers[customer_id].add_account(account_number)
        print("Account created.")
        self.save_data()

    def make_transaction(self):
        account_number = input("Enter account number: ")
        if account_number not in self.accounts:
            print("Account not found.")
            return
        txn_type = input("Transaction type (deposit/withdraw): ").lower()
        amount = float(input("Enter amount: "))
        txn_id = f"TXN{len(self.transactions)+1}"
        timestamp = datetime.now().isoformat()
        acc = self.accounts[account_number]
        if txn_type == 'deposit':
            acc.deposit(amount)
        elif txn_type == 'withdraw':
            acc.withdraw(amount)
        else:
            print("Invalid transaction type.")
            return
        txn = Transaction(txn_id, timestamp, account_number, txn_type, amount)
        self.transactions.append(txn)
        print("Transaction successful.")
        self.save_data()

    def check_balance(self):
        account_number = input("Enter account number: ")
        if account_number not in self.accounts:
            print("Account not found.")
            return
        acc = self.accounts[account_number]
        print(f"Balance: {acc.get_balance()}")

    def view_transactions(self):
        account_number = input("Enter account number: ")
        txns = [txn for txn in self.transactions if txn.account_number == account_number]
        if not txns:
            print("No transactions found.")
            return
        for txn in txns:
            print(f"ID: {txn.transaction_id}, Time: {txn.timestamp}, Type: {txn.transaction_type}, Amount: {txn.amount}")
