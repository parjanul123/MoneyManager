#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'moneymanager.settings')
django.setup()

from allauth.socialaccount.models import SocialApp

# Verifică câte Discord apps sunt
apps = SocialApp.objects.filter(provider='discord')
print(f"Discord apps în bază: {apps.count()}")
for app in apps:
    print(f"  - ID: {app.id}, Client ID: {app.client_id}, Name: {app.name}")

# Ștergem TOATE
if apps.count() > 0:
    deleted, _ = apps.delete()
    print(f"\n✅ Șterse {deleted} aplicații")
