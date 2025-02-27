import requests
import json
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
print(response_data)

# Check if the request was successful
if response.status_code == 200:
    access_token = response_data['access_token']
    instance_url = response_data['instance_url']
    print(f"Access Token: {access_token}")
    print(f"Instance URL: {instance_url}")

    # Use the access token to make authenticated requests to Salesforce
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }

    # Example: Get the details of the current user
    user_info_url = f"{instance_url}/services/oauth2/userinfo"
    user_info_response = requests.get(user_info_url, headers=headers)
    user_info = user_info_response.json()
    print(json.dumps(user_info, indent=2))
else:
    print(f"Failed to obtain access token: {response_data}")
