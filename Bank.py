import tkinter as tk
from tkinter import messagebox
import sqlite3

# Create a SQLite database and table
conn = sqlite3.connect('bank.db')
c = conn.cursor()
c.execute('''
          CREATE TABLE IF NOT EXISTS accounts (
              id INTEGER PRIMARY KEY AUTOINCREMENT,
              account_number INTEGER,
              account_holder TEXT,
              balance REAL
          )
          ''')
conn.commit()

class BankApplication:
    def __init__(self, root):
        self.root = root
        self.root.title("Bank Application")

        # Create labels and entry widgets
        self.label_account_number = tk.Label(root, text="Account Number:")
        self.entry_account_number = tk.Entry(root)

        self.label_amount = tk.Label(root, text="Amount:")
        self.entry_amount = tk.Entry(root)

        # Create buttons
        self.button_create_account = tk.Button(root, text="Create Account", command=self.create_account)
        self.button_deposit = tk.Button(root, text="Deposit", command=self.deposit)
        self.button_withdraw = tk.Button(root, text="Withdraw", command=self.withdraw)
        self.button_transfer = tk.Button(root, text="Transfer", command=self.transfer)
        self.button_display_accounts = tk.Button(root, text="Display Accounts", command=self.display_accounts)

        # Place widgets on the grid
        self.label_account_number.grid(row=0, column=0, padx=10, pady=10)
        self.entry_account_number.grid(row=0, column=1, padx=10, pady=10)

        self.label_amount.grid(row=1, column=0, padx=10, pady=10)
        self.entry_amount.grid(row=1, column=1, padx=10, pady=10)

        self.button_create_account.grid(row=2, column=0, columnspan=2, pady=10)
        self.button_deposit.grid(row=3, column=0, columnspan=2, pady=10)
        self.button_withdraw.grid(row=4, column=0, columnspan=2, pady=10)
        self.button_transfer.grid(row=5, column=0, columnspan=2, pady=10)
        self.button_display_accounts.grid(row=6, column=0, columnspan=2, pady=10)

    def create_account(self):
        try:
            account_number = int(self.entry_account_number.get())

            # Check if the account already exists
            c.execute('SELECT * FROM accounts WHERE account_number = ?', (account_number,))
            existing_account = c.fetchone()
            if existing_account:
                messagebox.showerror("Error", "Account already exists!")
                return

            # If the account doesn't exist, create a new account
            account_holder = f"Holder{account_number}"
            balance = 0.0

            c.execute('INSERT INTO accounts (account_number, account_holder, balance) VALUES (?, ?, ?)',
                      (account_number, account_holder, balance))
            conn.commit()

            messagebox.showinfo("Success", "Account created successfully!")
        except ValueError:
            messagebox.showerror("Error", "Invalid input. Please enter a valid account number.")

    def deposit(self):
        try:
            account_number = int(self.entry_account_number.get())
            amount = float(self.entry_amount.get())

            # Update balance in the database
            c.execute('UPDATE accounts SET balance = balance + ? WHERE account_number = ?', (amount, account_number))
            conn.commit()

            messagebox.showinfo("Success", "Deposit successful!")
        except (ValueError, sqlite3.Error) as e:
            messagebox.showerror("Error", f"Invalid input. {str(e)}")

    def withdraw(self):
        try:
            account_number = int(self.entry_account_number.get())
            amount = float(self.entry_amount.get())

            # Check if sufficient balance is available
            c.execute('SELECT balance FROM accounts WHERE account_number = ?', (account_number,))
            balance = c.fetchone()[0]
            if balance < amount:
                messagebox.showerror("Error", "Insufficient balance!")
                return

            # Update balance in the database
            c.execute('UPDATE accounts SET balance = balance - ? WHERE account_number = ?', (amount, account_number))
            conn.commit()

            messagebox.showinfo("Success", "Withdrawal successful!")
        except (ValueError, sqlite3.Error) as e:
            messagebox.showerror("Error", f"Invalid input. {str(e)}")

    def transfer(self):
        try:
            account_number_from = int(self.entry_account_number.get())
            amount = float(self.entry_amount.get())

            # Check if sufficient balance is available
            c.execute('SELECT balance FROM accounts WHERE account_number = ?', (account_number_from,))
            balance_from = c.fetchone()[0]
            if balance_from < amount:
                messagebox.showerror("Error", "Insufficient balance for transfer!")
                return

            account_number_to = int(input("Enter the account number to transfer to: "))

            # Check if the target account exists
            c.execute('SELECT * FROM accounts WHERE account_number = ?', (account_number_to,))
            existing_account = c.fetchone()
            if not existing_account:
                messagebox.showerror("Error", "Target account does not exist!")
                return

            # Update balances in the database
            c.execute('UPDATE accounts SET balance = balance - ? WHERE account_number = ?', (amount, account_number_from))
            c.execute('UPDATE accounts SET balance = balance + ? WHERE account_number = ?', (amount, account_number_to))
            conn.commit()

            messagebox.showinfo("Success", "Transfer successful!")
        except (ValueError, sqlite3.Error) as e:
            messagebox.showerror("Error", f"Invalid input. {str(e)}")

    def display_accounts(self):
        # Retrieve data from the database
        c.execute('SELECT * FROM accounts')
        accounts = c.fetchall()

        # Display data in a messagebox
        if accounts:
            message = "Accounts:\n"
            for account in accounts:
                message += f"Account Number: {account[1]}, Account Holder: {account[2]}, Balance: {account[3]}\n"
            messagebox.showinfo("Accounts", message)
        else:
            messagebox.showinfo("Accounts", "No accounts found.")

if __name__ == "__main__":
    root = tk.Tk()
    app = BankApplication(root)
    root.mainloop()

# Close the database connection when the application is closed
conn.close()
