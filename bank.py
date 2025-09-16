import json
from datetime import datetime
import os

class Customer:
    def __init__(self, customer_id, name, address, contact):
        self.customer_id = customer_id
        self.name = name
        self.address = address
        self.contact = contact

class Account:
    def __init__(self, account_number, balance, customer_id, acc_type, overdraw_limit=0):
        self.account_number = account_number
        self.balance = balance
        self.customer_id = customer_id
        self.acc_type = acc_type
        self.overdraw_limit = overdraw_limit

class Transaction:
    def __init__(self, txn_id, account_number, txn_type, amount, timestamp):
        self.txn_id = txn_id
        self.account_number = account_number
        self.txn_type = txn_type
        self.amount = amount
        self.timestamp = timestamp

class BankApp:
    def __init__(self):
        self.customers = self.load_file('customers.txt')
        self.saving_accounts = self.load_file('saving_accounts.txt')
        self.current_accounts = self.load_file('current_accounts.txt')
        self.transactions = self.load_file('transactions.txt')

    def load_file(self, filename):
        if not os.path.exists(filename):
            return []
        with open(filename, 'r') as f:
            return [json.loads(line) for line in f if line.strip()]

    def save_file(self, filename, data):
        with open(filename, 'w') as f:
            for item in data:
                f.write(json.dumps(item) + '\n')

    def run(self):
        while True:
            print("\n1. Create Customer\n2. Create Account\n3. Deposit\n4. Withdraw\n5. Check Balance\n6. View Transactions\n7. Exit")
            choice = input("Choose: ")
            if choice == '1':
                self.create_customer()
            elif choice == '2':
                self.create_account()
            elif choice == '3':
                self.deposit()
            elif choice == '4':
                self.withdraw()
            elif choice == '5':
                self.check_balance()
            elif choice == '6':
                self.view_transactions()
            elif choice == '7':
                self.save_all()
                print("Bye!")
                break
            else:
                print("Invalid choice.")

    def create_customer(self):
        cid = input("Customer ID: ")
        name = input("Name: ")
        addr = input("Address: ")
        contact = input("Contact: ")
        self.customers.append(Customer(cid, name, addr, contact).__dict__)
        self.save_file('customers.txt', self.customers)
        print("Customer created.")

    def create_account(self):
        cid = input("Customer ID: ")
        if not any(c['customer_id'] == cid for c in self.customers):
            print("Customer not found.")
            return
        acc_num = input("Account Number: ")
        acc_type = input("Type (saving/current): ").lower()
        bal = float(input("Initial Balance: "))
        if acc_type == 'saving':
            acc = Account(acc_num, bal, cid, acc_type)
            self.saving_accounts.append(acc.__dict__)
            self.save_file('saving_accounts.txt', self.saving_accounts)
        elif acc_type == 'current':
            overdraw = float(input("Overdraw Limit: "))
            acc = Account(acc_num, bal, cid, acc_type, overdraw)
            self.current_accounts.append(acc.__dict__)
            self.save_file('current_accounts.txt', self.current_accounts)
        else:
            print("Invalid account type.")
            return
        print("Account created.")

    def deposit(self):
        acc_num = input("Account Number: ")
        acc = next((a for a in self.saving_accounts if a['account_number'] == acc_num), None)
        acc_type = 'saving'
        if not acc:
            acc = next((a for a in self.current_accounts if a['account_number'] == acc_num), None)
            acc_type = 'current'
        if not acc:
            print("Account not found.")
            return
        amt = float(input("Amount: "))
        if amt <= 0:
            print("Amount must be positive.")
            return
        acc['balance'] += amt
        txn = Transaction(f"TXN{len(self.transactions)+1}", acc_num, 'deposit', amt, datetime.now().isoformat()).__dict__
        self.transactions.append(txn)
        if acc_type == 'saving':
            self.save_file('saving_accounts.txt', self.saving_accounts)
        else:
            self.save_file('current_accounts.txt', self.current_accounts)
        self.save_file('transactions.txt', self.transactions)
        print("Deposited.")

    def withdraw(self):
        acc_num = input("Account Number: ")
        acc = next((a for a in self.saving_accounts if a['account_number'] == acc_num), None)
        acc_type = 'saving'
        if not acc:
            acc = next((a for a in self.current_accounts if a['account_number'] == acc_num), None)
            acc_type = 'current'
        if not acc:
            print("Account not found.")
            return
        amt = float(input("Amount: "))
        limit = acc['balance'] + (acc['overdraw_limit'] if acc_type == 'current' else 0)
        if amt <= 0 or amt > limit:
            print("Invalid or insufficient funds.")
            return
        acc['balance'] -= amt
        txn = Transaction(f"TXN{len(self.transactions)+1}", acc_num, 'withdraw', amt, datetime.now().isoformat()).__dict__
        self.transactions.append(txn)
        if acc_type == 'saving':
            self.save_file('saving_accounts.txt', self.saving_accounts)
        else:
            self.save_file('current_accounts.txt', self.current_accounts)
        self.save_file('transactions.txt', self.transactions)
        print("Withdrawn.")

    def check_balance(self):
        acc_num = input("Account Number: ")
        acc = next((a for a in self.saving_accounts if a['account_number'] == acc_num), None)
        if not acc:
            acc = next((a for a in self.current_accounts if a['account_number'] == acc_num), None)
        if acc:
            print(f"Balance: {acc['balance']}")
        else:
            print("Account not found.")

    def view_transactions(self):
        acc_num = input("Account Number: ")
        txns = [t for t in self.transactions if t['account_number'] == acc_num]
        if not txns:
            print("No transactions.")
        for t in txns:
            print(f"{t['txn_id']} | {t['txn_type']} | {t['amount']} | {t['timestamp']}")

    def save_all(self):
        self.save_file('customers.txt', self.customers)
        self.save_file('saving_accounts.txt', self.saving_accounts)
        self.save_file('current_accounts.txt', self.current_accounts)
        self.save_file('transactions.txt', self.transactions)

