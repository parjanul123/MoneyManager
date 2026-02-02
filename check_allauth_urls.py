#!/usr/bin/env python
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'moneymanager.settings')
django.setup()

from django.urls import reverse
from django.test import RequestFactory
from django.contrib.sites.models import Site

print("="*60)
print("DJANGO ALLAUTH URL PATHS")
print("="*60)

# Construiește URL-urile care django-allauth va folosi
current_site = Site.objects.get(pk=1)
print(f"\nCurrent site: {current_site.domain}")

# Probabil urls
urls_to_check = [
    'socialaccount_callback_discord',
    'account_login',
]

print("\n" + "="*60)
print("URLS DISPONIBILE:")
print("="*60)
for url_name in ['socialaccount_callback_discord', 'account_login', 'socialaccount_signup']:
    try:
        url = reverse(url_name)
        full_url = f"http://{current_site.domain}{url}"
        print(f"  {url_name}: {url}")
        print(f"    Full: {full_url}")
    except Exception as e:
        print(f"  {url_name}: ERROR - {e}")

print("\n" + "="*60)
print("EXPECTED REDIRECT URI (MUST MATCH DISCORD APP):")
print("="*60)
callback_url = reverse('socialaccount_callback_discord')
full_callback = f"http://{current_site.domain}{callback_url}"
print(f"Expected: {full_callback}")

print("\n" + "="*60)
print("DISCORD APP CONFIGURATION:")
print("="*60)

from allauth.socialaccount.models import SocialApp
try:
    discord_app = SocialApp.objects.get(provider='discord')
    print(f"  Client ID: {discord_app.client_id}")
    print(f"  Sites: {[site.domain for site in discord_app.sites.all()]}")
except:
    print("  Discord app not found!")

import configparser
from pathlib import Path

config = configparser.ConfigParser()
if Path('discord.ini').exists():
    config.read('discord.ini')
    print(f"\n  discord.ini REDIRECT_URL: {config.get('discord', 'REDIRECT_URL')}")
    print(f"  discord.ini SCOPES: {config.get('discord', 'SCOPES')}")
