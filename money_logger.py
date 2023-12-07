#!/usr/bin/env python3

import json
import datetime
from prettytable import PrettyTable
import os
import sys

# Get the absolute path of the script
script_path = os.path.abspath(sys.argv[0])
script_directory = os.path.dirname(script_path)

# Set the desired directory for saving the data file
data_directory = os.path.expanduser('~')  # Save in the user's home directory

# Change the current working directory to the script directory
os.chdir(script_directory)

# Verify the current working directory after the change
print(f'Current Working Directory: {os.getcwd()}')

# Set the path for the data file
data_file = os.path.join(data_directory, 'money_log.json')

# Rest of your code...


def save_data():
    try:
        with open(data_file, 'w') as file:
            json.dump(money_log, file, default=str)
        print(f'Data saved to {data_file}')
    except Exception as e:
        print(f'Error saving data: {e}')

def load_data():
    try:
        with open(data_file, 'r') as file:
            loaded_data = json.load(file)
            for key in money_log.keys():
                money_log[key] = loaded_data.get(key, [])
        print(f'Data loaded successfully from {data_file}')
    except FileNotFoundError:
        print(f'{data_file} not found, creating a new file.')
    except Exception as e:
        print(f'Error loading data: {e}')

def log_transaction(transaction_type, amount, category, note):
    try:
        entry = {
            'date': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f'),
            'amount': float(amount),
            'category': category,
            'note': note
        }
        money_log[transaction_type].append(entry)
        print(f'Transaction recorded: {transaction_type.capitalize()} - Amount: {amount} tk, Category: {category}, Note: {note}')
        save_data()
    except ValueError:
        print('Invalid amount. Please enter a valid number.')

def delete_log(log_type, index):
    try:
        deleted_entry = money_log[log_type].pop(index)
        print(f'Deleted entry: {deleted_entry}')
        save_data()
    except IndexError:
        print('Invalid index. Please enter a valid index.')

def display_logs():
    print('\nIncome Entries:')
    for i, entry in enumerate(money_log['income']):
        print(f"{i}. Date: {entry['date']}, Amount: {entry['amount']} tk, Category: {entry['category']}, Note: {entry['note']}")

    print('\nExpense Entries:')
    for i, entry in enumerate(money_log['expenses']):
        print(f"{i}. Date: {entry['date']}, Amount: {entry['amount']} tk, Category: {entry['category']}, Note: {entry['note']}")

def display_summary():
    income_total = sum(entry['amount'] for entry in money_log['income'])
    expenses_total = sum(entry['amount'] for entry in money_log['expenses'])
    
    balance = income_total - expenses_total

    # Using PrettyTable for a tabular display
    table = PrettyTable()
    table.field_names = ["Type", "Total Amount"]

    table.add_row(["Monthly Income", f"{income_total} tk"])
    table.add_row(["Monthly Expenses", f"{expenses_total} tk"])
    table.add_row(["Total Income", f"{sum(entry['amount'] for entry in money_log['income'])} tk"])
    table.add_row(["Total Expenses", f"{sum(entry['amount'] for entry in money_log['expenses'])} tk"])
    table.add_row(["Balance", f"{balance} tk"])

    print(table)

if __name__ == "__main__":
    money_log = {'income': [], 'expenses': []}
    
    load_data()

    while True:
        print('\n1. Record Income')
        print('2. Record Expenses')
        print('3. Display Summary')
        print('4. Display Logs')
        print('5. Delete Log Entry')
        print('6. Exit')

        choice = input('Select an option (1-6): ')

        if choice == '1':
            amount = input('Enter the income amount: ')
            note = input('Enter a note: ')
            log_transaction('income', amount, 'Income', note)

        elif choice == '2':
            amount = input('Enter the expense amount: ')
            category = input('Enter the expense category (e.g., food, shop, taxi, bills, health, misc): ')
            note = input('Enter a note: ')
            log_transaction('expenses', amount, category, note)

        elif choice == '3':
            display_summary()

        elif choice == '4':
            display_logs()

        elif choice == '5':
            log_type = input('Enter the log type (income or expenses): ')
            index = int(input('Enter the index of the entry to delete: '))
            delete_log(log_type, index)

        elif choice == '6':
            break

        else:
            print('Invalid choice. Please enter a number between 1 and 6.')
