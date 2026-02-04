"""
Servicii pentru integrarea API-urilor BT și Revolut
"""
import requests
import logging
from decimal import Decimal
from datetime import datetime, timedelta
from django.utils import timezone
from django.conf import settings
from .models import BankConnection, BankTransaction, Transaction, Account
import hashlib
import hmac

logger = logging.getLogger(__name__)


class BankAPIBase:
    """Clasa de bază pentru API-uri bancare"""
    
    def __init__(self, bank_connection):
        self.bank_connection = bank_connection
        self.user = bank_connection.user
    
    def sync_transactions(self, days_back=30):
        """Sincronizează tranzacțiile din ultimele N zile"""
        raise NotImplementedError
    
    def get_balance(self):
        """Obține soldul actual al contului"""
        raise NotImplementedError
    
    def _create_transaction_record(self, transaction_data):
        """Creează un înregistrare de tranzacție din datele API"""
        raise NotImplementedError


class RevolutBankService(BankAPIBase):
    """Serviciu pentru API Revolut"""
    
    BASE_URL = "https://api.revolut.com/1.0"
    
    def __init__(self, bank_connection):
        super().__init__(bank_connection)
        self.headers = {
            'Authorization': f'Bearer {bank_connection.access_token}',
            'Content-Type': 'application/json',
        }
    
    def get_balance(self):
        """Obține soldul curent din Revolut"""
        try:
            response = requests.get(
                f"{self.BASE_URL}/accounts",
                headers=self.headers,
                timeout=10
            )
            response.raise_for_status()
            
            accounts = response.json().get('accounts', [])
            
            balance_data = {}
            for account in accounts:
                if account.get('type') == 'CURRENT':
                    balance_data = {
                        'balance': Decimal(str(account.get('balance', 0))),
                        'currency': account.get('currency', 'RON'),
                        'id': account.get('id'),
                    }
                    self.bank_connection.api_user_id = account.get('id')
                    self.bank_connection.save()
            
            return balance_data
            
        except requests.RequestException as e:
            logger.error(f"Revolut API error: {str(e)}")
            return None
    
    def sync_transactions(self, days_back=30):
        """Sincronizează tranzacțiile din Revolut"""
        try:
            # Obține lista conturilor
            response = requests.get(
                f"{self.BASE_URL}/accounts",
                headers=self.headers,
                timeout=10
            )
            response.raise_for_status()
            
            accounts = response.json().get('accounts', [])
            synced_count = 0
            
            for account in accounts:
                if account.get('type') != 'CURRENT':
                    continue
                
                account_id = account.get('id')
                
                # Obține tranzacțiile pentru account
                from_date = (timezone.now() - timedelta(days=days_back)).isoformat()
                
                trans_response = requests.get(
                    f"{self.BASE_URL}/accounts/{account_id}/transactions",
                    headers=self.headers,
                    params={'from': from_date},
                    timeout=10
                )
                trans_response.raise_for_status()
                
                transactions = trans_response.json().get('transactions', [])
                
                for trans in transactions:
                    synced = self._create_transaction_record(trans)
                    if synced:
                        synced_count += 1
            
            self.bank_connection.api_last_sync = timezone.now()
            self.bank_connection.save()
            
            return synced_count
            
        except requests.RequestException as e:
            logger.error(f"Revolut sync error: {str(e)}")
            return 0
    
    def _create_transaction_record(self, transaction_data):
        """Creează înregistrare de tranzacție din datele Revolut"""
        try:
            external_id = transaction_data.get('id')
            
            # Verifică duplicatele
            if BankTransaction.objects.filter(external_id=external_id).exists():
                return False
            
            amount = Decimal(str(transaction_data.get('amount', 0)))
            
            bank_trans = BankTransaction.objects.create(
                user=self.user,
                bank_connection=self.bank_connection,
                external_id=external_id,
                amount=amount,
                currency=transaction_data.get('currency', 'RON'),
                description=transaction_data.get('description', ''),
                date=datetime.fromisoformat(transaction_data.get('completed_at', timezone.now().isoformat())),
                recipient_name=transaction_data.get('counterparty', {}).get('name', ''),
                recipient_account=transaction_data.get('counterparty', {}).get('account_number', ''),
                sync_status='pending'
            )
            
            logger.info(f"Created bank transaction: {bank_trans}")
            return True
            
        except Exception as e:
            logger.error(f"Error creating transaction record: {str(e)}")
            return False


class BTBankService(BankAPIBase):
    """Serviciu pentru API Banca Transilvania (Open Banking)"""
    
    # BT folosește Open Banking API (PSD2)
    BASE_URL = "https://openapi.banca-transilvania.ro/v3"
    
    def __init__(self, bank_connection):
        super().__init__(bank_connection)
        self.headers = {
            'Authorization': f'Bearer {bank_connection.access_token}',
            'Content-Type': 'application/json',
            'X-Request-ID': self._generate_request_id(),
        }
    
    @staticmethod
    def _generate_request_id():
        """Generează ID unic pentru request"""
        import uuid
        return str(uuid.uuid4())
    
    def get_balance(self):
        """Obține soldul curent din BT"""
        try:
            # Obține lista de conturi
            accounts_response = requests.get(
                f"{self.BASE_URL}/accounts",
                headers=self.headers,
                timeout=10
            )
            accounts_response.raise_for_status()
            
            accounts = accounts_response.json().get('Data', {}).get('Account', [])
            
            balance_data = {}
            for account in accounts:
                account_id = account.get('AccountId')
                
                # Obține detaliile contului
                balance_response = requests.get(
                    f"{self.BASE_URL}/accounts/{account_id}/balances",
                    headers=self.headers,
                    timeout=10
                )
                balance_response.raise_for_status()
                
                balances = balance_response.json().get('Data', {}).get('Balance', [])
                
                for balance in balances:
                    if balance.get('Type') == 'Closing.Booked':
                        balance_data = {
                            'balance': Decimal(str(balance.get('Amount', {}).get('Amount', 0))),
                            'currency': balance.get('Amount', {}).get('Currency', 'RON'),
                            'id': account_id,
                        }
                        self.bank_connection.api_user_id = account_id
                        self.bank_connection.save()
                        break
            
            return balance_data
            
        except requests.RequestException as e:
            logger.error(f"BT API error: {str(e)}")
            return None
    
    def sync_transactions(self, days_back=30):
        """Sincronizează tranzacțiile din BT"""
        try:
            # Obține lista conturilor
            accounts_response = requests.get(
                f"{self.BASE_URL}/accounts",
                headers=self.headers,
                timeout=10
            )
            accounts_response.raise_for_status()
            
            accounts = accounts_response.json().get('Data', {}).get('Account', [])
            synced_count = 0
            
            from_date = (timezone.now() - timedelta(days=days_back)).date().isoformat()
            to_date = timezone.now().date().isoformat()
            
            for account in accounts:
                account_id = account.get('AccountId')
                
                # Obține tranzacțiile pentru account
                trans_response = requests.get(
                    f"{self.BASE_URL}/accounts/{account_id}/transactions-booked",
                    headers=self.headers,
                    params={
                        'bookingDateFrom': from_date,
                        'bookingDateTo': to_date,
                    },
                    timeout=10
                )
                trans_response.raise_for_status()
                
                transactions = trans_response.json().get('Data', {}).get('Transaction', [])
                
                for trans in transactions:
                    synced = self._create_transaction_record(trans)
                    if synced:
                        synced_count += 1
            
            self.bank_connection.api_last_sync = timezone.now()
            self.bank_connection.save()
            
            return synced_count
            
        except requests.RequestException as e:
            logger.error(f"BT sync error: {str(e)}")
            return 0
    
    def _create_transaction_record(self, transaction_data):
        """Creează înregistrare de tranzacție din datele BT"""
        try:
            external_id = transaction_data.get('TransactionId')
            
            # Verifică duplicatele
            if BankTransaction.objects.filter(external_id=external_id).exists():
                return False
            
            amount_data = transaction_data.get('Amount', {})
            amount = Decimal(str(amount_data.get('Amount', 0)))
            
            # BT returnează detalii în Credit/DebitIndicator
            booking_date = transaction_data.get('BookingDate')
            value_date = transaction_data.get('ValueDate')
            
            bank_trans = BankTransaction.objects.create(
                user=self.user,
                bank_connection=self.bank_connection,
                external_id=external_id,
                amount=amount,
                currency=amount_data.get('Currency', 'RON'),
                description=transaction_data.get('SupplementaryData', {}).get('description', ''),
                date=datetime.fromisoformat(booking_date) if booking_date else timezone.now(),
                recipient_name=transaction_data.get('Counterparty', {}).get('Name', ''),
                recipient_account=transaction_data.get('Counterparty', {}).get('Identification', ''),
                sync_status='pending'
            )
            
            logger.info(f"Created bank transaction: {bank_trans}")
            return True
            
        except Exception as e:
            logger.error(f"Error creating transaction record: {str(e)}")
            return False


class BankServiceFactory:
    """Factory pentru a selecta serviciul corect"""
    
    SERVICES = {
        'revolut': RevolutBankService,
        'bt': BTBankService,
    }
    
    @staticmethod
    def get_service(bank_connection):
        """Returnează serviciul API potrivit"""
        service_class = BankServiceFactory.SERVICES.get(bank_connection.bank)
        if not service_class:
            raise ValueError(f"Unknown bank: {bank_connection.bank}")
        return service_class(bank_connection)


def sync_all_banks(user):
    """Sincronizează toate conturile bancare ale unui utilizator"""
    connections = BankConnection.objects.filter(user=user, is_active=True)
    total_synced = 0
    
    for connection in connections:
        try:
            service = BankServiceFactory.get_service(connection)
            synced = service.sync_transactions()
            total_synced += synced
            logger.info(f"Synced {synced} transactions from {connection.get_bank_display()}")
        except Exception as e:
            logger.error(f"Error syncing {connection.get_bank_display()}: {str(e)}")
    
    return total_synced


def update_account_balance(bank_connection, account=None):
    """Actualizează soldul unui cont din banca"""
    try:
        service = BankServiceFactory.get_service(bank_connection)
        balance_data = service.get_balance()
        
        if not balance_data:
            return False
        
        if not account:
            # Creaează sau actualizează cont automat
            account, created = Account.objects.get_or_create(
                user=bank_connection.user,
                name=bank_connection.account_name,
                defaults={
                    'type': 'checking',
                    'currency': balance_data.get('currency', 'RON'),
                }
            )
        
        account.balance = balance_data.get('balance')
        account.currency = balance_data.get('currency', 'RON')
        account.save()
        
        logger.info(f"Updated balance for {account.name}: {account.balance} {account.currency}")
        return True
        
    except Exception as e:
        logger.error(f"Error updating balance: {str(e)}")
        return False


def auto_sync_pending_transactions(user):
    """Sincronizează automat tranzacțiile pending cu conturile utilizatorului"""
    pending = BankTransaction.objects.filter(
        user=user,
        sync_status='pending',
        synced_to_transaction__isnull=True
    )
    
    synced_count = 0
    
    for bank_trans in pending:
        try:
            # Găsește contul corespunzător
            account = Account.objects.filter(
                user=user,
                currency=bank_trans.currency
            ).first()
            
            if not account:
                logger.warning(f"No account found for {bank_trans.currency}")
                continue
            
            # Creează tranzacție
            transaction = Transaction.objects.create(
                user=user,
                account=account,
                type='income' if bank_trans.amount > 0 else 'expense',
                amount=abs(bank_trans.amount),
                description=bank_trans.description,
                date=bank_trans.date.date() if bank_trans.date else timezone.now().date(),
                category=None,  # Utilizatorul va selecta categoria
            )
            
            bank_trans.synced_to_transaction = transaction
            bank_trans.sync_status = 'synced'
            bank_trans.save()
            
            synced_count += 1
            
        except Exception as e:
            logger.error(f"Error syncing transaction {bank_trans.external_id}: {str(e)}")
    
    return synced_count
