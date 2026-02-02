#!/usr/bin/env python
import os
import django
import configparser

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'moneymanager.settings')
django.setup()

from allauth.socialaccount.models import SocialApp
from django.contrib.sites.models import Site

# Citire configurare Discord din discord.ini
config = configparser.ConfigParser()
config.read('discord.ini')

client_id = config.get('discord', 'CLIENT_ID')
client_secret = config.get('discord', 'CLIENT_SECRET')

# Șterge aplicația veche dacă există
SocialApp.objects.filter(provider='discord').delete()

# Creează noua aplicație Discord
app = SocialApp.objects.create(
    provider='discord',
    name='Discord',
    client_id=client_id,
    secret=client_secret
)

# Adaugă siteul curent
site = Site.objects.get(id=1)
app.sites.add(site)

print("✅ Discord Social App configurată:")
print(f"   Provider: {app.provider}")
print(f"   Client ID: {app.client_id}")
print(f"   Site: {site.domain}")
