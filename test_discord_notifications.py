#!/usr/bin/env python
"""
Test script for Discord notifications
Testează dacă notificări Discord funcționează corect
"""

import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'moneymanager.settings')
django.setup()

from django.contrib.auth.models import User
from django.utils import timezone
from decimal import Decimal
from finance.models import Transaction, Account, Category, Budget, UserProfile
from finance.discord_notifications import (
    send_discord_message,
    notify_transaction_created,
    notify_account_created,
    notify_budget_created,
    notify_user_joined,
    notify_discord_connected,
)
from django.conf import settings


def check_webhook_url():
    """Verifică dacă webhook URL este configurat"""
    webhook_url = getattr(settings, 'DISCORD_WEBHOOK_URL', '')
    
    print("\n" + "="*60)
    print("🔍 VERIFICARE WEBHOOK URL")
    print("="*60)
    
    if not webhook_url:
        print("❌ WEBHOOK_URL nu este configurat!")
        print("\n📝 Pași:")
        print("1. Deschide discord.ini")
        print("2. Completează WEBHOOK_URL = https://discord.com/api/webhooks/...")
        print("3. Restartează serverul Django")
        return False
    
    if webhook_url.startswith("YOUR_"):
        print("❌ WEBHOOK_URL este placeholder/necompletate!")
        print(f"Configurare actuală: {webhook_url}")
        return False
    
    print(f"✅ WEBHOOK_URL este configurat:")
    print(f"   {webhook_url[:80]}...")
    return True


def test_basic_message():
    """Testează trimiterea unui mesaj simplu"""
    print("\n" + "="*60)
    print("📤 TEST 1: Mesaj Simplu")
    print("="*60)
    
    result = send_discord_message(
        title="🧪 Test Mesaj",
        description="Aceasta este o notificare de test",
        fields={
            "Status": "OK",
            "Timestamp": timezone.now().strftime("%d.%m.%Y %H:%M:%S"),
        },
        color=0x00FF00  # Verde
    )
    
    if result:
        print("✅ Mesaj de test trimis!")
    else:
        print("❌ Eroare la trimiterea mesajului")
    
    return result


def test_transaction_notification():
    """Testează notificare pentru tranzacție"""
    print("\n" + "="*60)
    print("📤 TEST 2: Notificare Tranzacție")
    print("="*60)
    
    try:
        # Luă un utilizator și un cont
        user = User.objects.first()
        if not user:
            print("❌ Nu sunt utilizatori în bază")
            return False
        
        account = user.accounts.first()
        if not account:
            print("❌ Utilizatorul nu are conturi")
            return False
        
        category = Category.objects.first()
        if not category:
            print("❌ Nu sunt categorii în bază")
            return False
        
        # Crează o tranzacție de test
        print(f"\n📌 Date test:")
        print(f"   Utilizator: {user.username}")
        print(f"   Cont: {account.name}")
        print(f"   Categorie: {category.name}")
        
        # Notifică
        result = notify_transaction_created(None)
        
        # Notificăm cu o tranzacție existentă
        transaction = user.transactions.first()
        if transaction:
            result = notify_transaction_created(transaction)
            if result:
                print("✅ Notificare tranzacție trimisă!")
            else:
                print("❌ Eroare la trimiterea notificării")
        else:
            print("⚠️  Nu sunt tranzacții, voi trimite test default")
            result = send_discord_message(
                title="💸 Cheltuială nouă (TEST)",
                description="Aceasta este o notificare de test",
                fields={
                    "Utilizator": user.username,
                    "Conta": account.name,
                    "Suma": "50.00 RON",
                    "Categoria": category.name,
                },
                color=0xFF3333
            )
            if result:
                print("✅ Notificare cheltuială test trimisă!")
        
        return result
        
    except Exception as e:
        print(f"❌ Eroare: {e}")
        return False


def test_account_notification():
    """Testează notificare pentru cont"""
    print("\n" + "="*60)
    print("📤 TEST 3: Notificare Cont Nou")
    print("="*60)
    
    try:
        user = User.objects.first()
        if not user:
            print("❌ Nu sunt utilizatori în bază")
            return False
        
        account = user.accounts.first()
        if not account:
            print("❌ Utilizatorul nu are conturi")
            return False
        
        print(f"\n📌 Date test:")
        print(f"   Utilizator: {user.username}")
        print(f"   Cont: {account.name}")
        print(f"   Tip: {account.get_type_display()}")
        print(f"   Valută: {account.currency}")
        
        result = notify_account_created(account)
        
        if result:
            print("✅ Notificare cont trimisă!")
        else:
            print("❌ Eroare la trimiterea notificării")
        
        return result
        
    except Exception as e:
        print(f"❌ Eroare: {e}")
        return False


def test_budget_notification():
    """Testează notificare pentru buget"""
    print("\n" + "="*60)
    print("📤 TEST 4: Notificare Buget Nou")
    print("="*60)
    
    try:
        user = User.objects.first()
        if not user:
            print("❌ Nu sunt utilizatori în bază")
            return False
        
        budget = user.budgets.first()
        if not budget:
            print("⚠️  Nu sunt bugete, voi trimite test default")
            category = Category.objects.first()
            if not category:
                print("❌ Nu sunt categorii")
                return False
            
            result = send_discord_message(
                title="📊 Buget nou",
                description="Un nou buget a fost configurat",
                fields={
                    "Utilizator": user.username,
                    "Categoria": category.name,
                    "Buget": "1000.00 RON",
                    "Luna": "February 2026",
                },
                color=0xFFA500
            )
            if result:
                print("✅ Notificare buget test trimisă!")
            return result
        
        print(f"\n📌 Date test:")
        print(f"   Utilizator: {user.username}")
        print(f"   Categoria: {budget.category.name}")
        print(f"   Buget: {budget.amount}")
        print(f"   Luna: {budget.month}")
        
        result = notify_budget_created(budget)
        
        if result:
            print("✅ Notificare buget trimisă!")
        else:
            print("❌ Eroare la trimiterea notificării")
        
        return result
        
    except Exception as e:
        print(f"❌ Eroare: {e}")
        return False


def test_user_notification():
    """Testează notificare pentru utilizator nou"""
    print("\n" + "="*60)
    print("📤 TEST 5: Notificare Utilizator Nou")
    print("="*60)
    
    try:
        user = User.objects.first()
        if not user:
            print("❌ Nu sunt utilizatori în bază")
            return False
        
        print(f"\n📌 Date test:")
        print(f"   Utilizator: {user.username}")
        print(f"   Email: {user.email}")
        print(f"   Data înregistrării: {user.date_joined}")
        
        result = notify_user_joined(user)
        
        if result:
            print("✅ Notificare utilizator nou trimisă!")
        else:
            print("❌ Eroare la trimiterea notificării")
        
        return result
        
    except Exception as e:
        print(f"❌ Eroare: {e}")
        return False


def main():
    """Rulează toate testele"""
    print("\n")
    print("🧪 TEST DISCORD NOTIFICATIONS - Money Manager")
    print("="*60)
    
    # Verifică webhook URL
    if not check_webhook_url():
        print("\n❌ Setup incomplet. Configurează WEBHOOK_URL mai întâi.")
        return 1
    
    # Rulează testele
    tests = [
        test_basic_message,
        test_transaction_notification,
        test_account_notification,
        test_budget_notification,
        test_user_notification,
    ]
    
    results = []
    for test in tests:
        try:
            result = test()
            results.append(result)
        except Exception as e:
            print(f"❌ Eroare la test: {e}")
            results.append(False)
    
    # Sumar
    print("\n" + "="*60)
    print("📊 SUMAR REZULTATE")
    print("="*60)
    
    passed = sum(1 for r in results if r)
    total = len(results)
    
    print(f"\n✅ Teste trecute: {passed}/{total}")
    
    if passed == total:
        print("\n🎉 Toți testele au trecut! Discord notifications funcționează corect.")
        return 0
    else:
        print(f"\n⚠️  {total - passed} test(e) au eșuat.")
        print("\n📝 Verifică:")
        print("1. WEBHOOK_URL este configurat corect în discord.ini")
        print("2. Webhook-ul este activ pe Discord")
        print("3. Canalul Discord este accesibil")
        return 1


if __name__ == '__main__':
    sys.exit(main())
