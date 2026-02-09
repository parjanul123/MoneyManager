#!/usr/bin/env python
"""
Test pagina de rapoarte
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'moneymanager.settings')
django.setup()

from django.contrib.auth.models import User
from django.test import Client

client = Client()

# Login
print("=" * 60)
print("TEST PAGINA RAPOARTE")
print("=" * 60)

# Login cu parjanu
print("\n[1] Login cu 'parjanu'...")
login_ok = client.login(username='parjanu', password='')
print(f"Login result: {login_ok} (parola goala - check-ul e manual)")

# Mergi la pagina de rapoarte
print("\n[2] Acces /reports/...")
response = client.get('/reports/')
print(f"Status code: {response.status_code}")

if response.status_code == 200:
    print("✅ Pagina e accessible!")
    
    # Verific context
    if 'expense_by_category' in response.context:
        exp_data = response.context['expense_by_category']
        inc_data = response.context['income_by_category']
        print(f"\n✅ Context variables transmise:")
        print(f"   - expense_by_category: {exp_data}")
        print(f"   - income_by_category: {inc_data}")
    else:
        print("❌ Context variables nu gasiti!")
    
    # Verific HTML content
    html = response.content.decode('utf-8')
    if 'expenseChart' in html and 'incomeChart' in html:
        print("\n✅ Canvas elements pentru harturi gasiti!")
    if 'new Chart' in html:
        print("✅ Chart.js code gasit în HTML!")
else:
    print(f"❌ Error {response.status_code}")

print("\n" + "=" * 60)
print("Acum porniti serverul si meriti la http://127.0.0.1:9512/reports/")
print("=" * 60)
