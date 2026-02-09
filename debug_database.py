#!/usr/bin/env python
"""
Debug script - verifică din ce bază de date citeste Django
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'moneymanager.settings')
django.setup()

from django.conf import settings
from django.db import connection

print("=" * 60)
print("DEBUG - VERIFIC BAZA DE DATE")
print("=" * 60)

# 1. Verific environment variables
print("\n[1] ENVIRONMENT VARIABLES:")
print(f"SUPABASE_DB_ENABLED: {os.environ.get('SUPABASE_DB_ENABLED', 'NOT SET')}")
print(f"SUPABASE_DB_HOST: {os.environ.get('SUPABASE_DB_HOST', 'NOT SET')}")
print(f"SUPABASE_DB_PASSWORD: {'SET' if os.environ.get('SUPABASE_DB_PASSWORD') else 'NOT SET'}")

# 2. Verific configurația Django
print("\n[2] DJANGO SETTINGS:")
print(f"DATABASES: {list(settings.DATABASES.keys())}")
default_db = settings.DATABASES['default']
print(f"ENGINE: {default_db['ENGINE']}")
print(f"NAME: {default_db['NAME']}")
if 'HOST' in default_db:
    print(f"HOST: {default_db['HOST']}")

# 3. Verific conexiunea curentă
print("\n[3] CONEXIUNEA CURENTĂ:")
print(f"Database: {connection.vendor}")
print(f"Settings DB: {connection.settings_dict['ENGINE']}")

# 4. Verific ce bază de date este folosită
if 'sqlite' in connection.settings_dict['ENGINE'].lower():
    print(f"\n❌ PROBLEM: Django folosește SQLite!")
    print(f"Fișierul: {connection.settings_dict['NAME']}")
    print(f"\n⚠️  Nu folosești Supabase! Datele se salvează local în SQLite!")
elif 'postgresql' in connection.settings_dict['ENGINE'].lower():
    print(f"\n✅ Django folosește PostgreSQL (Supabase)!")
    print(f"HOST: {connection.settings_dict['HOST']}")
    print(f"NAME: {connection.settings_dict['NAME']}")

# 5. Test conexiune
print("\n[4] TEST CONEXIUNE:")
try:
    with connection.cursor() as cursor:
        cursor.execute("SELECT 1")
        print("✅ Conexiune la baza de date: OK")
except Exception as e:
    print(f"❌ Eroare conexiune: {e}")

print("\n" + "=" * 60)
