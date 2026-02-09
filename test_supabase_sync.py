#!/usr/bin/env python
"""
Test script pentru Supabase API connectivity
Ruleaza: py test_supabase_sync.py
"""

import os
import sys
from pathlib import Path

# Add project to path
sys.path.insert(0, str(Path(__file__).resolve().parent))

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'moneymanager.settings')

import django
django.setup()

from finance.supabase_sync import (
    log_user_activity, 
    sync_user_to_supabase,
    get_users_from_supabase,
    get_user_activity_from_supabase
)
from django.contrib.auth.models import User

print("\n" + "="*60)
print("SUPABASE CONNECTIVITY TEST")
print("="*60)

# Test 1: Get existing user
print("\n[TEST 1] Finding existing user...")
user = User.objects.first()
if user:
    print(f"✓ Found user: {user.username} (ID: {user.id}, Email: {user.email})")
else:
    print("✗ No users found in database")
    sys.exit(1)

# Test 2: Sync user to Supabase
print("\n[TEST 2] Syncing user to Supabase...")
result = sync_user_to_supabase(user)
if result.get('success'):
    print(f"✓ User sync successful!")
    print(f"  Response: {result}")
else:
    print(f"✗ User sync failed!")
    print(f"  Error: {result.get('error')}")

# Test 3: Log activity
print("\n[TEST 3] Logging activity to Supabase...")
activity_result = log_user_activity(user, 'test_activity', {'test': 'data'})
if activity_result.get('success'):
    print(f"✓ Activity logged successfully!")
else:
    print(f"✗ Activity logging failed!")
    print(f"  Error: {activity_result.get('error')}")

# Test 4: Retrieve users from Supabase
print("\n[TEST 4] Retrieving users from Supabase...")
users_from_supabase = get_users_from_supabase()
if users_from_supabase:
    print(f"✓ Found {len(users_from_supabase)} user(s) in Supabase:")
    for u in users_from_supabase[:3]:  # Show first 3
        print(f"  - {u.get('username')} ({u.get('email')})")
else:
    print(f"✗ No users found in Supabase or API error")

# Test 5: Retrieve activity logs
print("\n[TEST 5] Retrieving activity logs from Supabase...")
activity_logs = get_user_activity_from_supabase()
if activity_logs:
    print(f"✓ Found {len(activity_logs)} activity log(s):")
    for log in activity_logs[:3]:  # Show first 3
        print(f"  - {log.get('action')} by {log.get('username')} at {log.get('timestamp')}")
else:
    print(f"✗ No activity logs found or API error")

print("\n" + "="*60)
print("TEST COMPLETE")
print("="*60 + "\n")
