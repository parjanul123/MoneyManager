#!/usr/bin/env python
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'moneymanager.settings')
django.setup()

from django.urls import get_resolver, URLPattern
from django.urls.resolvers import URLResolver

print("="*60)
print("TOATE URLS DISPONIBILE:")
print("="*60)

resolver = get_resolver()

def print_urls(urlpatterns, prefix=''):
    for pattern in urlpatterns:
        if isinstance(pattern, URLResolver):
            print(f"{prefix}{pattern.pattern} -> {pattern.app_name if pattern.app_name else 'namespace'}")
            if hasattr(pattern, 'url_patterns'):
                print_urls(pattern.url_patterns, prefix + '  ')
        elif isinstance(pattern, URLPattern):
            name = pattern.name or '(unnamed)'
            print(f"{prefix}{pattern.pattern} -> {name}")

print_urls(resolver.url_patterns)

print("\n" + "="*60)
print("DISCORD-RELATED URLS:")
print("="*60)
for pattern in resolver.url_patterns:
    if 'discord' in str(pattern).lower() or 'accounts' in str(pattern).lower():
        print(pattern)
