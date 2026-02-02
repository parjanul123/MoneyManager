#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'moneymanager.settings')
django.setup()

from allauth.socialaccount.models import SocialApp

# Șterge TOATE aplicațiile Discord vechi
deleted_count, _ = SocialApp.objects.filter(provider='discord').delete()
print(f"🗑️ Șterse {deleted_count} aplicații Discord vechi")

# Nu mai crează noi - settings.py va folosi configurația din discord.ini
print("✅ Baza de date curățată!")
