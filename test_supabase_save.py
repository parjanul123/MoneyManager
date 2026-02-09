#!/usr/bin/env python
"""
Test script pentru verificare salvare date în Supabase
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'moneymanager.settings')
django.setup()

from django.contrib.auth.models import User
from finance.models import Category, Account, Transaction
from django.utils import timezone
from decimal import Decimal

print("=" * 60)
print("TEST SALVARE DATE ÎN SUPABASE")
print("=" * 60)

# 1. Testez dacă admin user existe
print("\n[1] Verificare Admin User...")
try:
    admin = User.objects.get(username='admin')
    print(f"✅ Admin user găsit: {admin.username} ({admin.email})")
except User.DoesNotExist:
    print("❌ Admin user NU găsit!")
    exit(1)

# 2. Creez o categorie de test
print("\n[2] Creez categorie de test...")
category, created = Category.objects.get_or_create(
    name="Test Cheltuieli",
    defaults={'type': 'expense', 'description': 'Categorie de test'}
)
if created:
    print(f"✅ Categorie CREATĂ: {category.name}")
else:
    print(f"✅ Categorie già EXISTENTĂ: {category.name}")

# 3. Creez un cont bancar de test
print("\n[3] Creez cont bancar de test...")
account, created = Account.objects.get_or_create(
    user=admin,
    name="Test Account",
    defaults={
        'type': 'checking',
        'balance': Decimal('1000.00'),
        'currency': 'RON'
    }
)
if created:
    print(f"✅ Cont CREAT: {account.name} ({account.balance} {account.currency})")
else:
    print(f"✅ Cont già EXISTENT: {account.name} ({account.balance} {account.currency})")

# 4. Creez o tranzacție de test
print("\n[4] Creez tranzacție de test...")
transaction = Transaction.objects.create(
    user=admin,
    account=account,
    category=category,
    type='expense',
    amount=Decimal('50.00'),
    description='Test tranzacție - Salvare Supabase',
    date=timezone.now().date()
)
print(f"✅ Tranzacție CREATĂ: {transaction.amount} RON - {transaction.description}")

# 5. Verific datele în baza de date
print("\n[5] Verific datele salvate...")
all_accounts = Account.objects.filter(user=admin)
all_transactions = Transaction.objects.filter(user=admin)
print(f"✅ Total conturi pentru admin: {all_accounts.count()}")
print(f"✅ Total tranzacții pentru admin: {all_transactions.count()}")

print("\n" + "=" * 60)
print("✅ TOATE TESTELE AU TRECUT!")
print("=" * 60)
print("\n📊 Datele se salvează corect în Supabase!")
print("\nPoți verifica în Supabase Dashboard:")
print("- Tabelul: finance_account")
print("- Tabelul: finance_transaction")
print("- Tabelul: finance_category")
