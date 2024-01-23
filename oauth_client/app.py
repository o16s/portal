import requests
from urllib.parse import urlencode, urlsplit, parse_qs, urlparse
from dotenv import load_dotenv
import os
from selenium import webdriver
import time
from datetime import datetime, timedelta

browser = webdriver.Chrome()

load_dotenv()

# OAuth2 Client Setup
client_id = "openremote"
client_secret = ""  # Your client secret (if needed)
scope = "openid"  # Adjust the scope to your needs
base_url = os.getenv("OR_URL")
authorization_base_url = f"{base_url}auth/realms/master/protocol/openid-connect/auth"
token_url = f"{base_url}auth/realms/master/protocol/openid-connect/token"
redirect_uri = f"{base_url}p"

try:
    # Construct the authorization URL
    authorization_url = f"{authorization_base_url}?response_type=code&client_id={client_id}&scope={scope}&redirect_uri={redirect_uri}"

    # Use the browser to open the authorization URL
    browser.get(authorization_url)

    # Wait for the user to authorize the app
    # This is a simplistic way to wait. You might need a more robust way to determine when the redirect has happened.
    while True:
        if browser.current_url.startswith(redirect_uri):
            break
        time.sleep(1)
        print(browser.current_url)

    # The browser is now at the redirect URI, capture the URL
    redirected_url = browser.current_url

finally:
    # Close the browser
    browser.quit()

# Extract the authorization code from the URL
parsed_url = urlparse(redirected_url)
auth_code = parse_qs(parsed_url.query)['code'][0]

# Step 2: Exchange the Authorization Code for an Access Token
data = {
    'grant_type': 'authorization_code',
    'client_id': client_id,
    'client_secret': client_secret,
    'code': auth_code,
    'redirect_uri': redirect_uri
}
response = requests.post(token_url, data=data)
token_response = response.json()

# Print the access token (or store it securely for future use)
print("Access Token:")
print(token_response['access_token'])
access_token = token_response['access_token']



# Assuming the token response includes a refresh token and expires_in (lifetime of access token in seconds)
refresh_token = token_response.get('refresh_token')
expires_in = token_response.get('expires_in')
expiration_time = datetime.now() + timedelta(seconds=expires_in)

def get_access_token():
    global access_token, expiration_time

    # If the current time is past the expiration time, refresh the token
    if datetime.now() >= expiration_time:
        refresh_data = {
            'grant_type': 'refresh_token',
            'refresh_token': refresh_token,
            'client_id': client_id,
            'client_secret': client_secret,
        }
        response = requests.post(token_url, data=refresh_data)
        
        if response.status_code == 200:
            refresh_response = response.json()
            access_token = refresh_response['access_token']
            expires_in = refresh_response.get('expires_in')
            expiration_time = datetime.now() + timedelta(seconds=expires_in)
            print("Access token refreshed successfully")
        else:
            print(f"Failed to refresh token: {response.status_code}")
            print(response.text)
            return None

    return access_token

while True:
    # Use the access token to access the API
    access_token = get_access_token()
    if access_token:
        asset_id = "7NRFpebtbzf4VLfqwckN2B"
        api_url = f"{base_url}api/master/asset/{asset_id}"

        headers = {
            'Authorization': f'Bearer {access_token}',
        }

        response = requests.get(api_url, headers=headers)

        if response.status_code == 200:
            # Successfully fetched the data
            asset_data = response.json()
            print(asset_data)
        else:
            # Something went wrong
            print(f"Failed to fetch data: {response.status_code}")
            print(response.text)
            
    time.sleep(1)