#!/usr/bin/env python
import os
import django
import sqlite3

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'moneymanager.settings')
django.setup()

from django.conf import settings

# Conectează-te la baza de date
db_path = settings.DATABASES['default']['NAME']
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Șterge TOATE Discord apps
cursor.execute("DELETE FROM socialaccount_socialapp WHERE provider='discord'")
cursor.execute("SELECT changes()")
deleted_apps = cursor.fetchone()[0]

# Șterge relațiile sites
cursor.execute("DELETE FROM socialaccount_socialapp_sites WHERE socialapp_id NOT IN (SELECT id FROM socialaccount_socialapp)")
cursor.execute("SELECT changes()")
deleted_sites = cursor.fetchone()[0]

conn.commit()
conn.close()

print(f"✅ Șterse {deleted_apps} aplicații Discord")
print(f"✅ Șterse {deleted_sites} relații sites")
print("\n💾 Pentru a adăuga Discord din nou, rulează:")
print("   py setup_discord_app.py")
