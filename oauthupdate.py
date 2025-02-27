import requests
import json
import tkinter as tk
from tkinter import messagebox
from simple_salesforce import Salesforce
from oauthlogin import client_id, client_secret, token_url

# Your Salesforce connected app credentials imported from oauthlogin.py
client_id = client_id
client_secret = client_secret
token_url = token_url

# Prepare the payload for the token request
payload = {
    'grant_type': 'client_credentials',
    'client_id': client_id,
    'client_secret': client_secret
}

# Make the token request
response = requests.post(token_url, data=payload)
response_data = response.json()
access_token = response_data['access_token']
instance_url = response_data['instance_url']

# Authenticate with Salesforce using simple_salesforce
sf = Salesforce(instance_url=instance_url, session_id=access_token)

# Function to search for an account
def search_account():
    name = search_entry.get()
    query = f"SELECT Id, Name, Type, NumberOfEmployees, AccountNumber, Industry FROM Account WHERE Name = '{name}'"
    result = sf.query(query)
    
    if result['totalSize'] == 0:
        messagebox.showinfo("Not Found", "No account found with that name.")
    else:
        account = result['records'][0]
        id_entry.delete(0, tk.END)
        id_entry.insert(0, account['Id'])
        name_entry.delete(0, tk.END)
        name_entry.insert(0, account['Name'])
        type_entry.delete(0, tk.END)
        type_entry.insert(0, account['Type'])
        employees_entry.delete(0, tk.END)
        employees_entry.insert(0, account['NumberOfEmployees'])
        account_number_entry.delete(0, tk.END)
        account_number_entry.insert(0, account['AccountNumber'])
        industry_entry.delete(0, tk.END)
        industry_entry.insert(0, account['Industry'])

# Function to update account record
def update_account():
    account_id = id_entry.get()
    name = name_entry.get()
    account_type = type_entry.get()
    num_employees = employees_entry.get()
    account_number = account_number_entry.get()
    industry = industry_entry.get()

    account_data = {
        'Name': name,
        'Type': account_type,
        'NumberOfEmployees': num_employees,
        'AccountNumber': account_number,
        'Industry': industry
    }

    result = sf.Account.update(account_id, account_data)
    messagebox.showinfo("Success", "Account updated successfully.")

# Create the UI
root = tk.Tk()
root.title("Salesforce Account Manager")

tk.Label(root, text="Search by Name").grid(row=0, column=0)
search_entry = tk.Entry(root)
search_entry.grid(row=0, column=1)
tk.Button(root, text="Search", command=search_account).grid(row=0, column=2)

tk.Label(root, text="ID").grid(row=1, column=0)
tk.Label(root, text="Name").grid(row=2, column=0)
tk.Label(root, text="Type").grid(row=3, column=0)
tk.Label(root, text="Number of Employees").grid(row=4, column=0)
tk.Label(root, text="Account Number").grid(row=5, column=0)
tk.Label(root, text="Industry").grid(row=6, column=0)

id_entry = tk.Entry(root)
name_entry = tk.Entry(root)
type_entry = tk.Entry(root)
employees_entry = tk.Entry(root)
account_number_entry = tk.Entry(root)
industry_entry = tk.Entry(root)

id_entry.grid(row=1, column=1)
name_entry.grid(row=2, column=1)
type_entry.grid(row=3, column=1)
employees_entry.grid(row=4, column=1)
account_number_entry.grid(row=5, column=1)
industry_entry.grid(row=6, column=1)

tk.Button(root, text="Update Account", command=update_account).grid(row=7, column=1)

root.mainloop()
