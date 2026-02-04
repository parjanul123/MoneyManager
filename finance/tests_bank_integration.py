"""
Test Suite pentru Bank Integration
Rulează: python manage.py test finance.tests_bank_integration
"""

from django.test import TestCase, Client
from django.contrib.auth.models import User
from finance.models import BankConnection, BankTransaction, Account, Transaction, Category
from finance.bank_services import BankServiceFactory, RevolutBankService, BTBankService
from unittest.mock import patch, MagicMock
from decimal import Decimal
from datetime import datetime, timedelta
from django.utils import timezone


class BankConnectionModelTests(TestCase):
    """Testează modelul BankConnection"""
    
    def setUp(self):
        self.user = User.objects.create_user('testuser', 'test@example.com', 'password')
    
    def test_create_revolut_connection(self):
        """Testează crearea conexiune Revolut"""
        conn = BankConnection.objects.create(
            user=self.user,
            bank='revolut',
            account_name='Revolut Test',
            access_token='test_token_123'
        )
        
        self.assertEqual(conn.bank, 'revolut')
        self.assertEqual(conn.account_name, 'Revolut Test')
        self.assertTrue(conn.is_active)
        self.assertIn('Revolut', str(conn))
    
    def test_create_bt_connection(self):
        """Testează crearea conexiune BT"""
        conn = BankConnection.objects.create(
            user=self.user,
            bank='bt',
            account_name='BT Curent',
            access_token='bt_token_456'
        )
        
        self.assertEqual(conn.bank, 'bt')
        self.assertIn('BT', str(conn))
    
    def test_unique_constraint(self):
        """Testează constraint de unicitate"""
        conn1 = BankConnection.objects.create(
            user=self.user,
            bank='revolut',
            account_name='Revolut 1',
            access_token='token1',
            api_user_id='user123'
        )
        
        # Încercă să creezi duplicate - ar trebui să eșueze
        with self.assertRaises(Exception):
            conn2 = BankConnection.objects.create(
                user=self.user,
                bank='revolut',
                account_name='Revolut 2',
                access_token='token2',
                api_user_id='user123'
            )


class BankTransactionModelTests(TestCase):
    """Testează modelul BankTransaction"""
    
    def setUp(self):
        self.user = User.objects.create_user('testuser', 'test@example.com', 'password')
        self.connection = BankConnection.objects.create(
            user=self.user,
            bank='revolut',
            account_name='Test Account',
            access_token='token'
        )
    
    def test_create_bank_transaction(self):
        """Testează crearea tranzacție bancară"""
        trans = BankTransaction.objects.create(
            user=self.user,
            bank_connection=self.connection,
            external_id='ext_123',
            amount=Decimal('100.00'),
            currency='RON',
            description='Test transaction',
            date=timezone.now(),
            sync_status='pending'
        )
        
        self.assertEqual(trans.amount, Decimal('100.00'))
        self.assertEqual(trans.sync_status, 'pending')
        self.assertIsNone(trans.synced_to_transaction)
    
    def test_transaction_linking(self):
        """Testează linkarea cu Transaction"""
        account = Account.objects.create(
            user=self.user,
            name='Test Account',
            balance=Decimal('1000.00'),
            currency='RON'
        )
        
        transaction = Transaction.objects.create(
            user=self.user,
            account=account,
            type='income',
            amount=Decimal('100.00'),
            description='Linked transaction',
            date=timezone.now().date()
        )
        
        bank_trans = BankTransaction.objects.create(
            user=self.user,
            bank_connection=self.connection,
            external_id='ext_456',
            amount=Decimal('100.00'),
            currency='RON',
            description='Bank transaction',
            date=timezone.now(),
            sync_status='pending'
        )
        
        # Link them
        bank_trans.synced_to_transaction = transaction
        bank_trans.sync_status = 'synced'
        bank_trans.save()
        
        self.assertEqual(bank_trans.synced_to_transaction, transaction)
        self.assertEqual(bank_trans.sync_status, 'synced')


class BankServiceFactoryTests(TestCase):
    """Testează factory pentru servicii bancare"""
    
    def setUp(self):
        self.user = User.objects.create_user('testuser', 'test@example.com', 'password')
    
    def test_revolut_service(self):
        """Testează crearea serviciu Revolut"""
        conn = BankConnection.objects.create(
            user=self.user,
            bank='revolut',
            account_name='Test',
            access_token='token'
        )
        
        service = BankServiceFactory.get_service(conn)
        self.assertIsInstance(service, RevolutBankService)
    
    def test_bt_service(self):
        """Testează crearea serviciu BT"""
        conn = BankConnection.objects.create(
            user=self.user,
            bank='bt',
            account_name='Test',
            access_token='token'
        )
        
        service = BankServiceFactory.get_service(conn)
        self.assertIsInstance(service, BTBankService)
    
    def test_invalid_bank(self):
        """Testează eroare pentru bancă necunoscută"""
        conn = BankConnection(
            user=self.user,
            bank='invalid_bank',
            account_name='Test',
            access_token='token'
        )
        
        with self.assertRaises(ValueError):
            BankServiceFactory.get_service(conn)


class BankViewsTests(TestCase):
    """Testează vederile pentru bănci"""
    
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user('testuser', 'test@example.com', 'password123')
        self.client.login(username='testuser', password='password123')
    
    def test_bank_connections_list_view(self):
        """Testează afișare listă conectări"""
        response = self.client.get('/finance/banks/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'finance/bank_connections_list.html')
    
    def test_bank_dashboard_view(self):
        """Testează dashboard bancar"""
        response = self.client.get('/finance/banks/dashboard/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'finance/bank_dashboard.html')
    
    def test_bank_connection_create_view(self):
        """Testează formular conectare"""
        response = self.client.get('/finance/banks/create/')
        self.assertEqual(response.status_code, 200)
        self.assertIn('BankConnectionForm', str(response.content))


class BankSyncTests(TestCase):
    """Testează sincronizare tranzacții"""
    
    def setUp(self):
        self.user = User.objects.create_user('testuser', 'test@example.com', 'password')
        self.account = Account.objects.create(
            user=self.user,
            name='Test Account',
            balance=Decimal('1000.00'),
            currency='RON'
        )
    
    @patch('finance.bank_services.requests.get')
    def test_revolut_api_call(self, mock_get):
        """Testează apel API Revolut (mock)"""
        mock_response = MagicMock()
        mock_response.json.return_value = {
            'accounts': [{
                'id': 'acc123',
                'type': 'CURRENT',
                'balance': 1500.50,
                'currency': 'RON'
            }]
        }
        mock_get.return_value = mock_response
        
        conn = BankConnection.objects.create(
            user=self.user,
            bank='revolut',
            account_name='Test',
            access_token='token'
        )
        
        service = RevolutBankService(conn)
        balance = service.get_balance()
        
        self.assertIsNotNone(balance)
        self.assertEqual(balance['balance'], Decimal('1500.50'))
        self.assertEqual(balance['currency'], 'RON')


class ManagementCommandTests(TestCase):
    """Testează management command"""
    
    def setUp(self):
        self.user = User.objects.create_user('testuser', 'test@example.com', 'password')
    
    def test_sync_command_exists(self):
        """Testează dacă command-ul de sincronizare există"""
        from django.core.management import call_command
        from io import StringIO
        
        # Ar trebui să nu eșueze
        out = StringIO()
        call_command('sync_bank_transactions', stdout=out)
        output = out.getvalue()
        
        self.assertIn('Sincronizate', output)


# Test utilities
def create_test_bank_connection(user, bank='revolut'):
    """Helper function pentru crearea conexiune test"""
    return BankConnection.objects.create(
        user=user,
        bank=bank,
        account_name=f'Test {bank.upper()}',
        access_token='test_token_123',
        api_user_id='test_user_id'
    )


def create_test_bank_transaction(user, connection, amount=100.00):
    """Helper function pentru crearea tranzacție test"""
    return BankTransaction.objects.create(
        user=user,
        bank_connection=connection,
        external_id=f'ext_{timezone.now().timestamp()}',
        amount=Decimal(str(amount)),
        currency='RON',
        description='Test transaction',
        date=timezone.now(),
        sync_status='pending'
    )
