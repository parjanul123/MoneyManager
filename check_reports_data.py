#!/usr/bin/env python
"""
Verifică datele din luna februarie 2026
"""
import os
import django
from datetime import date, timedelta

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'moneymanager.settings')
django.setup()

from django.contrib.auth.models import User
from finance.models import Transaction, Category
from django.utils import timezone
from django.db.models import Sum

print("=" * 60)
print("VERIFICARE DATE - FEBRUARIE 2026")
print("=" * 60)

user = User.objects.get(username='parjanu')
today = timezone.now().date()
month_start = today.replace(day=1)

print(f"\nUtilizator: {user.username}")
print(f"Data de azi: {today}")
print(f"Inceput luna: {month_start}")

# Toate tranzacțiile utilizatorului
print(f"\n[1] TOATE TRANZACȚIILE:")
all_trans = user.transactions.all().order_by('-date')
print(f"Total: {all_trans.count()} tranzacții")
for t in all_trans[:10]:
    print(f"  - {t.date} | {t.amount} RON | {t.type} | {t.description}")

# Tranzacțiile din luna curentă
print(f"\n[2] TRANZACȚII DIN FEBRUARIE (din {month_start}):")
month_trans = user.transactions.filter(date__gte=month_start)
print(f"Total: {month_trans.count()} tranzacții")
for t in month_trans:
    print(f"  - {t.date} | {t.amount} RON | {t.type} | Cat: {t.category}")

# Cheltuieli pe categorii
print(f"\n[3] CHELTUIELI PE CATEGORII (februarie):")
expenses = month_trans.filter(type='expense').values('category__name').annotate(total=Sum('amount')).order_by('-total')
for exp in expenses:
    print(f"  - {exp['category__name']}: {exp['total']} RON")

# Venituri pe categorii
print(f"\n[4] VENITURI PE CATEGORII (februarie):")
incomes = month_trans.filter(type='income').values('category__name').annotate(total=Sum('amount')).order_by('-total')
for inc in incomes:
    print(f"  - {inc['category__name']}: {inc['total']} RON")

# Total
print(f"\n[5] TOTAL:")
total_expenses = month_trans.filter(type='expense').aggregate(Sum('amount'))['amount__sum'] or 0
total_income = month_trans.filter(type='income').aggregate(Sum('amount'))['amount__sum'] or 0
print(f"Cheltuieli: {total_expenses} RON")
print(f"Venituri: {total_income} RON")
print(f"Net: {total_income - total_expenses} RON")

print("\n" + "=" * 60)
