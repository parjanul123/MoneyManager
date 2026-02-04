"""
Quick Setup Script pentru Bank Integration
Rulează: python setup_bank_integration.py
"""

import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'moneymanager.settings')
django.setup()

from django.contrib.auth.models import User
from finance.models import Category


def setup_categories():
    """Creează categoriile implicite pentru tranzacții bancare"""
    default_categories = [
        ('Venituri', 'income', 'Salariu, bonusuri, etc.'),
        ('Cheltuieli Zilnice', 'expense', 'Mâncare, transport, etc.'),
        ('Utilități', 'expense', 'Electricitate, apă, gaz, internet'),
        ('Telefon', 'expense', 'Abonament telefon/internet'),
        ('Transport', 'expense', 'Benzină, transport public, taxi'),
        ('Cumpărături', 'expense', 'Haine, obiecte, etc.'),
        ('Divertisment', 'expense', 'Cinema, jocuri, cărți'),
        ('Sănătate', 'expense', 'Medicamente, doctor, dentist'),
        ('Împrumuturi', 'expense', 'Plăți rate, împrumuturi'),
        ('Investiții', 'income', 'Retururi investiții, dobânzi'),
        ('Transfer Inter-conturi', 'expense', 'Transfer între conturi proprii'),
    ]
    
    created = 0
    for name, type_, description in default_categories:
        cat, was_created = Category.objects.get_or_create(
            name=name,
            defaults={'type': type_, 'description': description}
        )
        if was_created:
            created += 1
            print(f"✓ Creată categorie: {name}")
        else:
            print(f"- Categorie existentă: {name}")
    
    print(f"\n✓ Setup categorii complet! ({created} noi)")


def test_imports():
    """Testează importurile"""
    try:
        from finance.models import BankConnection, BankTransaction
        from finance.bank_services import BankServiceFactory, sync_all_banks
        from finance.views import bank_connections_list
        print("✓ Toate importurile sunt OK!")
        return True
    except ImportError as e:
        print(f"✗ Import error: {e}")
        return False


def check_migrations():
    """Verifică dacă migrațiile au fost aplicate"""
    from django.core.management import call_command
    from io import StringIO
    import sys
    
    # Check if tables exist
    try:
        from finance.models import BankConnection, BankTransaction
        BankConnection.objects.count()
        BankTransaction.objects.count()
        print("✓ Tabelele de bază de date sunt create!")
        return True
    except Exception as e:
        print(f"✗ Eroare bază de date: {e}")
        print("\nRulează pentru a crea tabelele:")
        print("  python manage.py makemigrations")
        print("  python manage.py migrate")
        return False


def main():
    print("=" * 60)
    print("🏦 Setup Bank Integration - Money Manager")
    print("=" * 60)
    print()
    
    # 1. Test imports
    print("[1/3] Verificare import pachete...")
    if not test_imports():
        print("\n✗ Configurare eșuată! Instalează pachete din requirements.txt")
        sys.exit(1)
    print()
    
    # 2. Check migrations
    print("[2/3] Verificare bază de date...")
    if not check_migrations():
        print("\n✗ Rulează migrațiile Django mai întâi!")
        sys.exit(1)
    print()
    
    # 3. Setup categories
    print("[3/3] Setup categorii implicite...")
    setup_categories()
    print()
    
    print("=" * 60)
    print("✓ Setup complet!")
    print("=" * 60)
    print()
    print("Pași următori:")
    print("1. Mergi la /finance/banks/ pentru a conecta bănci")
    print("2. Introdu token-urile API pentru Revolut/BT")
    print("3. Sincronizează tranzacțiile")
    print("4. Revizuiește și acceptă tranzacțiile")
    print()
    print("Documentație: BANK_INTEGRATION_GUIDE.md")
    print()


if __name__ == '__main__':
    main()
