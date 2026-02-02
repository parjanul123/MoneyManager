#!/usr/bin/env python
"""
Test what allauth would send to Discord for token exchange
"""
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'moneymanager.settings')
django.setup()

from allauth.socialaccount.providers.discord.provider import DiscordProvider
from allauth.socialaccount.providers.discord.views import DiscordOAuth2Adapter
from allauth.socialaccount.models import SocialApp
from django.contrib.sites.models import Site

print("="*60)
print("DISCORD OAUTH2 CONFIGURATION IN DJANGO-ALLAUTH")
print("="*60)

try:
    social_app = SocialApp.objects.get(provider='discord')
    print(f"\n✅ Social App Found:")
    print(f"  Provider: {social_app.provider}")
    print(f"  Name: {social_app.name}")
    print(f"  Client ID: {social_app.client_id}")
    print(f"  Sites: {[s.domain for s in social_app.sites.all()]}")
    
    # Try to get adapter settings
    print(f"\n✅ Provider Info:")
    provider = DiscordProvider()
    print(f"  Provider ID: {provider.id}")
    print(f"  Scopes: {provider.get_default_scope()}")
    
except SocialApp.DoesNotExist:
    print("❌ Discord SocialApp NOT found!")

# Check what URLs would be used
print(f"\n✅ Expected Redirect URI:")
print(f"  http://127.0.0.1:9512/accounts/discord/login/callback/")

# Check if configured in discord.ini
import configparser
from pathlib import Path
config = configparser.ConfigParser()
if Path('discord.ini').exists():
    config.read('discord.ini')
    ini_redirect = config.get('discord', 'REDIRECT_URL')
    print(f"\n📋 discord.ini REDIRECT_URL:")
    print(f"  {ini_redirect}")
    
    if ini_redirect == "http://127.0.0.1:9512/accounts/discord/login/callback/":
        print(f"\n✅ URLs MATCH!")
    else:
        print(f"\n❌ URLs DON'T MATCH!")
        print(f"  Expected: http://127.0.0.1:9512/accounts/discord/login/callback/")
        print(f"  Got:      {ini_redirect}")
