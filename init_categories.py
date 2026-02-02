import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'moneymanager.settings')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
django.setup()

from django.contrib.auth.models import User
from finance.models import Category

# Create default categories
expense_categories = [
    'Hrană',
    'Transport',
    'Chirie',
    'Utilități',
    'Sănătate',
    'Educație',
    'Divertisment',
    'Cumpărături',
    'Telefon/Internet',
    'Siguranță',
]

income_categories = [
    'Salariu',
    'Freelance',
    'Bonus',
    'Vânzări',
    'Dobanzi',
]

print("Creând categorii de cheltuieli...")
for cat_name in expense_categories:
    Category.objects.get_or_create(
        name=cat_name,
        defaults={'type': 'expense'}
    )
    print(f"✓ {cat_name}")

print("\nCreând categorii de venituri...")
for cat_name in income_categories:
    Category.objects.get_or_create(
        name=cat_name,
        defaults={'type': 'income'}
    )
    print(f"✓ {cat_name}")

print("\n✅ Categoriile au fost create cu succes!")
print("\nPentru a crea un superutilizator, rulează:")
print("python manage.py createsuperuser")
