#!/usr/bin/env python
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'moneymanager.settings')
django.setup()

from django.contrib.sites.models import Site
from allauth.socialaccount.models import SocialApp

# Verifica siturile
print("=" * 60)
print("SITES DIN BAZĂ:")
print("=" * 60)
for site in Site.objects.all():
    print(f"  ID: {site.id}, Domain: {site.domain}, Name: {site.name}")

print("\n" + "=" * 60)
print("SOCIAL APPS:")
print("=" * 60)
for app in SocialApp.objects.all():
    print(f"\n  Providei: {app.provider}")
    print(f"    Name: {app.name}")
    print(f"    Client ID: {app.client_id}")
    print(f"    Sites asociate: {list(app.sites.all())}")
    print(f"    Site IDs: {list(app.sites.values_list('id', flat=True))}")

    if not app.sites.exists():
        print(f"\n  ⚠️  ATENȚIE: {app.name} NU are site asociat!")
        print(f"  Adaug site 1 (127.0.0.1:9512)...")
        app.sites.add(1)
        print(f"  ✅ Adăugat!")

print("\n" + "=" * 60)
print("VERIFICARE FINALĂ:")
print("=" * 60)
for app in SocialApp.objects.all():
    if app.sites.exists():
        print(f"✅ {app.name} - sites OK: {list(app.sites.values_list('domain', flat=True))}")
    else:
        print(f"❌ {app.name} - FĂRĂ SITE!")
