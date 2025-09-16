# Command Line Bank Application

## Overview

This is a command line bank application for managing customers, accounts (Savings and Current), and transactions. It uses object-oriented programming principles and stores all data persistently in text files.

## Features

- **Customer Management:** Create and manage customers with multiple accounts.
- **Account Management:** Create Savings and Current accounts, each with specific features (interest rate, overdraw limit).
- **Transactions:** Deposit and withdraw money, with transaction history tracking.
- **File Persistence:** All data is saved in text files (`customers.txt`, `saving_accounts.txt`, `current_accounts.txt`, `transactions.txt`).
- **Command Line Interface:** Easy-to-use CLI for all operations.
- **Error Handling:** Robust error messages for invalid inputs and file errors.

## File Structure

- `main.py` — Entry point for the application.
- `bank.py` — Contains all classes and CLI logic.
- `customers.txt` — Stores customer records.
- `saving_accounts.txt` — Stores savings account records.
- `current_accounts.txt` — Stores current account records.
- `transactions.txt` — Stores transaction history.

## How to Run

1. Make sure you have Python installed.
2. Open a terminal in the project directory.
3. Run the application:
   ```
   python main.py
   ```
4. Follow the on-screen menu to interact with the bank system.

## Sample CLI Menu

```
Options:
1. Create Customer
2. Create Account
3. Make Transaction
4. Check Balance
5. View Transaction History
6. Exit
Enter your choice:
```

## Screenshots

*(Add screenshots of your CLI in use here)*

## Notes

- Data files are updated immediately after each operation.
- If you encounter errors, ensure your data files are not empty or corrupted.
- For any issues, check that Python has write permissions in your project folder.

## Author

Osamah Mahdi  
Unit Code: BN111  
Unit Name: Programming Fundamentals  
School of Information Technology and Engineering  
Moderator: Dr Amoakoh GyasiAgyei
