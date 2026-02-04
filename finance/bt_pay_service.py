"""
BT Pay Integration Service
Detectează, categorizează și gestionează tranzacții BT Pay
"""

import re
import logging
from decimal import Decimal
from django.db.models import Sum, Q
from django.utils import timezone
from .models import BankTransaction, Transaction, Account, Category, User

logger = logging.getLogger(__name__)


class BTPay:
    """Serviciu pentru gestionarea tranzacțiilor BT Pay"""
    
    # Tipuri de comercianți
    MERCHANT_CATEGORIES = {
        # Food & Dining
        'food': ['coffee', 'restaurant', 'pizza', 'burger', 'mcdonalds', 'kfc', 
                'starbucks', 'subway', 'cafe', 'bar', 'pub', 'bistro', 'grill'],
        
        # Shopping
        'shopping': ['carrefour', 'auchan', 'lidl', 'penny', 'emag', 'altex',
                    'mall', 'store', 'shop', 'market', 'supermarket', 'hypermarket'],
        
        # Transport
        'transport': ['uber', 'bolt', 'taxi', 'gas station', 'benzina', 'carburant',
                     'parking', 'toll', 'bus', 'train', 'metro', 'transport'],
        
        # Utilities
        'utilities': ['electric', 'water', 'gas', 'internet', 'phone', 'utility',
                     'enel', 'eon', 'vodafone', 'orange', 'telekom'],
        
        # Entertainment
        'entertainment': ['cinema', 'movie', 'theatre', 'concert', 'netflix', 'spotify',
                         'game', 'steam', 'playstation', 'xbox', 'museum', 'theatre'],
        
        # Health
        'health': ['pharmacy', 'doctor', 'hospital', 'clinic', 'medical', 'dentist',
                  'healthcare', 'apteka', 'medic'],
        
        # Fitness
        'fitness': ['gym', 'fitness', 'sport', 'yoga', 'trainer'],
        
        # Education
        'education': ['school', 'university', 'course', 'book', 'library'],
        
        # Travel
        'travel': ['hotel', 'airbnb', 'booking', 'airline', 'flight', 'tourism'],
    }
    
    @staticmethod
    def is_bt_pay_transaction(description):
        """Verifică dacă e tranzacție BT Pay"""
        if not description:
            return False
        
        desc_lower = description.lower()
        return any([
            'bt pay' in desc_lower,
            'portofel digital' in desc_lower,
            'digital wallet' in desc_lower,
        ])
    
    @staticmethod
    def extract_merchant_name(description):
        """Extrage numele comerciantului din descriere"""
        if not description:
            return None
        
        # Pattern: "BT Pay - Merchant Name"
        match = re.search(r'BT Pay[:\s]*-?\s*([^,]+)', description, re.IGNORECASE)
        if match:
            merchant = match.group(1).strip()
            # Elimină info extra
            merchant = re.sub(r'\d{2}:\d{2}|\d{4}-\d{2}-\d{2}', '', merchant).strip()
            return merchant
        
        return description
    
    @staticmethod
    def guess_category(description):
        """Ghicește categoria pe baza descrierii"""
        if not description:
            return None
        
        desc_lower = description.lower()
        merchant = BTPay.extract_merchant_name(description).lower()
        
        # Cauta în categorii
        for category_name, keywords in BTPay.MERCHANT_CATEGORIES.items():
            for keyword in keywords:
                if keyword in desc_lower or keyword in merchant:
                    return category_name
        
        return None
    
    @staticmethod
    def categorize_bt_pay_transaction(bank_transaction):
        """Categorizează automat o tranzacție BT Pay"""
        if not BTPay.is_bt_pay_transaction(bank_transaction.description):
            return False
        
        # Ghicește categoria
        category_name = BTPay.guess_category(bank_transaction.description)
        
        if not category_name:
            logger.info(f"Could not auto-categorize: {bank_transaction.description}")
            return False
        
        try:
            # Găsește sau creează categoria
            category, created = Category.objects.get_or_create(
                name=category_name.title(),
                defaults={
                    'type': 'expense',
                    'description': f'BT Pay - {category_name}'
                }
            )
            
            # Creează tranzacția
            account = Account.objects.filter(
                user=bank_transaction.user,
                currency=bank_transaction.currency
            ).first()
            
            if not account:
                return False
            
            transaction = Transaction.objects.create(
                user=bank_transaction.user,
                account=account,
                category=category,
                type='expense',
                amount=abs(bank_transaction.amount),
                description=BTPay.extract_merchant_name(bank_transaction.description),
                date=bank_transaction.date.date(),
            )
            
            # Linkează
            bank_transaction.synced_to_transaction = transaction
            bank_transaction.sync_status = 'synced'
            bank_transaction.save()
            
            logger.info(f"Auto-categorized BT Pay: {bank_transaction.description} → {category.name}")
            return True
            
        except Exception as e:
            logger.error(f"Error categorizing BT Pay transaction: {e}")
            return False
    
    @staticmethod
    def auto_categorize_all_bt_pay(user):
        """Categorizează automat toate tranzacțiile BT Pay pending"""
        pending_bt_pay = BankTransaction.objects.filter(
            user=user,
            sync_status='pending',
            synced_to_transaction__isnull=True
        ).exclude(description__isnull=True)
        
        categorized = 0
        for bank_trans in pending_bt_pay:
            if BTPay.categorize_bt_pay_transaction(bank_trans):
                categorized += 1
        
        return categorized
    
    @staticmethod
    def get_bt_pay_stats(user, days=30):
        """Obține statistici BT Pay"""
        from datetime import timedelta
        
        start_date = timezone.now() - timedelta(days=days)
        
        bt_pay_transactions = BankTransaction.objects.filter(
            user=user,
            sync_status='synced',
            date__gte=start_date
        ).exclude(description__isnull=True)
        
        bt_pay_transactions = [
            t for t in bt_pay_transactions 
            if BTPay.is_bt_pay_transaction(t.description)
        ]
        
        stats = {
            'total_transactions': len(bt_pay_transactions),
            'total_amount': sum(abs(t.amount) for t in bt_pay_transactions),
            'transactions_by_category': {},
            'top_merchants': {}
        }
        
        # Categorii
        for trans in bt_pay_transactions:
            category = BTPay.guess_category(trans.description) or 'other'
            if category not in stats['transactions_by_category']:
                stats['transactions_by_category'][category] = {
                    'count': 0,
                    'total': Decimal('0')
                }
            stats['transactions_by_category'][category]['count'] += 1
            stats['transactions_by_category'][category]['total'] += abs(trans.amount)
        
        # Top comercianți
        merchants = {}
        for trans in bt_pay_transactions:
            merchant = BTPay.extract_merchant_name(trans.description) or 'Unknown'
            if merchant not in merchants:
                merchants[merchant] = {'count': 0, 'total': Decimal('0')}
            merchants[merchant]['count'] += 1
            merchants[merchant]['total'] += abs(trans.amount)
        
        # Sortează și iau top 10
        stats['top_merchants'] = dict(
            sorted(merchants.items(), key=lambda x: x[1]['total'], reverse=True)[:10]
        )
        
        return stats
    
    @staticmethod
    def notify_large_bt_pay(user, transaction, threshold=100):
        """Notifică pentru plăți mari prin BT Pay"""
        if not BTPay.is_bt_pay_transaction(transaction.description):
            return False
        
        if abs(transaction.amount) >= threshold:
            logger.warning(
                f"Large BT Pay transaction: {transaction.description} - {transaction.amount} {transaction.currency}"
            )
            
            # TODO: Adaugă email/SMS/Discord notification
            
            return True
        
        return False


def auto_sync_bt_pay(user):
    """Sincronizează și categorizează automat BT Pay tranzacții"""
    categorized = BTPay.auto_categorize_all_bt_pay(user)
    return categorized
