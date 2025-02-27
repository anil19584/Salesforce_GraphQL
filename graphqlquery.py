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

# Function to get access token
def get_access_token(token_url, payload):
    response = requests.post(token_url, data=payload)
    if response.status_code == 200:
        return response.json().get('access_token')
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
    
# Obtain access token
access_token = get_access_token(token_url, payload)

# Salesforce instance URL
instance_url = 'https://mindful-goat-p5c3v5-dev-ed.trailblaze.my.salesforce.com'


# GraphQL query
query = """
{
  uiapi {
    query {
      Account {
        edges {
          node {
            Name {
              value
            }
            Type {
              value
            }
            Industry {
              value
            }
            NumberOfEmployees {
              value
            }
            AccountNumber {
              value
            }
          }
        }
      }
    }
  }
}
"""

# Perform the GraphQL query and store the data in a pandas DataFrame
try:
    data = query_salesforce(access_token, instance_url, query)
    
    # Extract relevant data from the response and store it in a list of dictionaries
    accounts = []
    for edge in data['data']['uiapi']['query']['Account']['edges']:
        node = edge['node']
        account = {
            'Name': node['Name']['value'],
            'Type': node['Type']['value'],
            'Industry': node['Industry']['value'],
            'NumberOfEmployees': node['NumberOfEmployees']['value'],
            'AccountNumber': node['AccountNumber']['value']
        }
        accounts.append(account)
    
    # Create a pandas DataFrame from the list of dictionaries
    df = pd.DataFrame(accounts)
    
    # Print the DataFrame
    print(df)
except Exception as e:
    print(e)
