#!/usr/bin/env python
"""
Test Discord OAuth flow direct
"""
import requests
import configparser
from pathlib import Path

config = configparser.ConfigParser()
config.read(Path('discord.ini'))

CLIENT_ID = config.get('discord', 'CLIENT_ID')
CLIENT_SECRET = config.get('discord', 'CLIENT_SECRET')
REDIRECT_URI = config.get('discord', 'REDIRECT_URL')

print(f"CLIENT_ID: {CLIENT_ID}")
print(f"CLIENT_SECRET: {CLIENT_SECRET[:10]}...")
print(f"REDIRECT_URI: {REDIRECT_URI}")

# Simulează un test de token exchange
test_code = "24MQCtiYhXUtDDWqbpz86C3rZpiCeD"  # Codul din eroare

print("\n" + "="*60)
print("TEST: Exchange code for token")
print("="*60)

data = {
    'client_id': CLIENT_ID,
    'client_secret': CLIENT_SECRET,
    'grant_type': 'authorization_code',
    'code': test_code,
    'redirect_uri': REDIRECT_URI,
    'scope': 'identify email guilds'
}

print("\nSending to: https://discord.com/api/oauth2/token")
print(f"Data: {data}")

try:
    response = requests.post('https://discord.com/api/oauth2/token', data=data)
    print(f"\nStatus: {response.status_code}")
    print(f"Response: {response.text}")
    
    if response.status_code == 200:
        print("\n✅ Token exchange successful!")
        token_data = response.json()
        print(f"Access Token: {token_data.get('access_token', '')[:20]}...")
    else:
        print(f"\n❌ Token exchange failed!")
        print(f"Error details: {response.json() if response.text else 'No response'}")
        
except Exception as e:
    print(f"\n❌ Error: {e}")

print("\n" + "="*60)
print("NOTES:")
print("="*60)
print("- Codul Discord expiră după ~15 minute")
print("- Fiecare cod poate fi folosit o singură dată")
print("- CLIENT_SECRET trebuie să se potrivească exact")
print("- REDIRECT_URI trebuie să se potrivească exact cu cea din Discord app")
