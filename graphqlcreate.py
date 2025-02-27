
import requests
import json
import pandas as pd
import tkinter as tk
from tkinter import messagebox
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

# Function to get access token
def get_access_token(token_url, payload):
    response = requests.post(token_url, data=payload)
    if response.status_code == 200:
        return response.json().get('access_token')
    else:
        raise Exception(f"Error: {response.status_code}, {response.text}")

# Function to get Salesforce instance URL
def get_instance_url(access_token):
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }
    response = requests.get('https://login.salesforce.com/services/oauth2/userinfo', headers=headers)
    if response.status_code == 200:
        return response.json().get('instance_url')
    else:
        raise Exception(f"Error: {response.status_code}, {response.text}")


# Function to perform GraphQL query
def query_salesforce(access_token, instance_url, query):
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }
    response = requests.post(
        f'{instance_url}/services/data/v50.0/graphql',
        headers=headers,
        json={'query': query}
    )
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Error: {response.status_code}, {response.text}")

# Function to insert data into Salesforce
def insert_account(access_token, instance_url, name, account_type, industry):
    mutation = f"""
    mutation {{
      createAccount(input: {{
        Name: "{name}",
        Type: "{account_type}",
        Industry: "{industry}"
      }}) {{
        account {{
          Id
          Name
          Type
          Industry
        }}
      }}
    }}
    """
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }
    response = requests.post(
        f'{instance_url}/services/data/v50.0/graphql',
        headers=headers,
        json={'query': mutation}
    )
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Error: {response.status_code}, {response.text}")

# Function to handle form submission
def submit_form():
    name = name_entry.get()
    account_type = type_entry.get()
    industry = industry_entry.get()
    
    try:
        # Obtain access token
        access_token = get_access_token(token_url, payload)
        # Get Salesforce instance URL
        instance_url = get_instance_url(access_token)
        # instance_url = 'https://mindful-goat-p5c3v5-dev-ed.trailblaze.my.salesforce.com'
        # Insert new account into Salesforce
        result = insert_account(access_token, instance_url, name, account_type, industry)
        messagebox.showinfo("Success", f"Account created successfully: {result['data']['createAccount']['account']['Id']}")
    except Exception as e:
        messagebox.showerror("Error", str(e))

# Create the main window
root = tk.Tk()
root.title("Salesforce Account Creator")

# Create and place the labels and entry widgets
tk.Label(root, text="Account Name").grid(row=0, column=0)
name_entry = tk.Entry(root)
name_entry.grid(row=0, column=1)

tk.Label(root, text="Account Type").grid(row=1, column=0)
type_entry = tk.Entry(root)
type_entry.grid(row=1, column=1)

tk.Label(root, text="Industry").grid(row=2, column=0)
industry_entry = tk.Entry(root)
industry_entry.grid(row=2, column=1)

# Create and place the submit button
submit_button = tk.Button(root, text="Create Account", command=submit_form)
submit_button.grid(row=3, columnspan=2)

# Run the application
root.mainloop()

