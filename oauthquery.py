import requests
import json
import pandas as pd
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

# Query the Account object
query = "select id, name, type, NumberOfEmployees, AccountNumber, industry from Account"
headers = {
    'Authorization': f'Bearer {access_token}',
    'Content-Type': 'application/json'
}
query_url = f"{instance_url}/services/data/v52.0/query?q={query}"
query_response = requests.get(query_url, headers=headers)
query_data = query_response.json()

# Extract records and store them in a pandas DataFrame
records = query_data['records']
df = pd.DataFrame(records)

# Select only the desired columns
df = df[['Name', 'Type', 'Industry' , 'NumberOfEmployees' , 'AccountNumber' ]]

print(df)