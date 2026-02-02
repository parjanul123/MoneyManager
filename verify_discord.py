#!/usr/bin/env python
import os
import django
import sqlite3

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'moneymanager.settings')
django.setup()

from django.conf import settings
import configparser

# Citire config
config = configparser.ConfigParser()
config.read('discord.ini')
client_id = config.get('discord', 'CLIENT_ID')
client_secret = config.get('discord', 'CLIENT_SECRET')

# Conectare DB
db_path = settings.DATABASES['default']['NAME']
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Verifică ce e în bază
cursor.execute("SELECT id, client_id, secret FROM socialaccount_socialapp WHERE provider='discord'")
existing = cursor.fetchone()

if existing:
    print(f"Găsit Discord app:")
    print(f"  ID: {existing[0]}")
    print(f"  Client ID din bază: {existing[1]}")
    print(f"  Secret din bază: {existing[2]}")
    print(f"\nDin discord.ini:")
    print(f"  Client ID: {client_id}")
    print(f"  Secret: {client_secret}")
    
    # Actualizeaza
    cursor.execute(
        "UPDATE socialaccount_socialapp SET client_id=?, secret=? WHERE provider='discord'",
        (client_id, client_secret)
    )
    conn.commit()
    print("\n✅ Actualizat!")
else:
    print("❌ Nu găsit Discord app în bază!")

conn.close()
