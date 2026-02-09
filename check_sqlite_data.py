#!/usr/bin/env python
"""
Script pentru a verifica datele din SQLite local
"""
import sqlite3
import os

db_path = 'd:\\MoneyManager\\db.sqlite3'

if not os.path.exists(db_path):
    print("❌ Nu exista db.sqlite3 (am sters-o)")
    exit(1)

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

print("=" * 60)
print("DATE DIN SQLite LOCAL")
print("=" * 60)

# Users
print("\n[1] UTILIZATORI:")
cursor.execute("SELECT id, username, email FROM auth_user")
users = cursor.fetchall()
for user in users:
    print(f"  - {user[1]} ({user[2]}) - ID: {user[0]}")

# Accounts
print("\n[2] CONTURI BANCARE:")
cursor.execute("""
    SELECT id, user_id, name, balance, currency 
    FROM finance_account
""")
accounts = cursor.fetchall()
for acc in accounts:
    print(f"  - {acc[2]} ({acc[4]}) - Sold: {acc[3]} - User ID: {acc[1]}")

# Transactions
print("\n[3] TRANZACȚII:")
cursor.execute("""
    SELECT id, user_id, amount, description, type, date 
    FROM finance_transaction
    ORDER BY id DESC
    LIMIT 10
""")
transactions = cursor.fetchall()
for trans in transactions:
    print(f"  - {trans[2]} RON - {trans[3]} ({trans[4]}) - {trans[5]}")

# Categories
print("\n[4] CATEGORII:")
cursor.execute("SELECT id, name, type FROM finance_category")
categories = cursor.fetchall()
for cat in categories:
    print(f"  - {cat[1]} ({cat[2]})")

conn.close()

print("\n" + "=" * 60)
print("\n📍 Datele tale sunt în SQLite local, NU în Supabase!")
print("\nPentru a le vedea în Supabase Dashboard, trebuie:")
print("1. Să se conecteze la Supabase (problema de rețea)")
print("2. Sau să migrezi datele manual")
