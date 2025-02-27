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

# Function to insert account record
def insert_account():
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

    result = sf.Account.create(account_data)
    messagebox.showinfo("Success", f"Account created with ID: {result['id']}")

# Create the UI
root = tk.Tk()
root.title("Salesforce Account Inserter")

tk.Label(root, text="Name").grid(row=0)
tk.Label(root, text="Type").grid(row=1)
tk.Label(root, text="Number of Employees").grid(row=2)
tk.Label(root, text="Account Number").grid(row=3)
tk.Label(root, text="Industry").grid(row=4)

name_entry = tk.Entry(root)
type_entry = tk.Entry(root)
employees_entry = tk.Entry(root)
account_number_entry = tk.Entry(root)
industry_entry = tk.Entry(root)

name_entry.grid(row=0, column=1)
type_entry.grid(row=1, column=1)
employees_entry.grid(row=2, column=1)
account_number_entry.grid(row=3, column=1)
industry_entry.grid(row=4, column=1)

tk.Button(root, text="Insert Account", command=insert_account).grid(row=5, column=1)

root.mainloop()