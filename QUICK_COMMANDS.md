# 🏦 Bank Integration - Quick Commands Reference

## 📦 Installation & Setup

```bash
# 1. Install packages
pip install -r requirements.txt

# 2. Create migrations
python manage.py makemigrations finance

# 3. Apply migrations
python manage.py migrate

# 4. Setup default categories
python setup_bank_integration.py

# 5. Create superuser (if needed)
python manage.py createsuperuser

# 6. Collect static files (production)
python manage.py collectstatic
```

## 🚀 Running the Server

```bash
# Development
python manage.py runserver

# Specific port
python manage.py runserver 0.0.0.0:8000

# Access web interface
http://localhost:8000/finance/banks/
```

## 🔄 Synchronization Commands

```bash
# Sync all users' banks (all accounts)
python manage.py sync_bank_transactions

# Sync specific user
python manage.py sync_bank_transactions --user 1

# Sync specific number of days
python manage.py sync_bank_transactions --days 60

# Sync only Revolut
python manage.py sync_bank_transactions --bank revolut

# Sync only BT
python manage.py sync_bank_transactions --bank bt

# Verbose output
python manage.py sync_bank_transactions --verbosity 3
```

## 🧪 Testing

```bash
# Run all bank integration tests
python manage.py test finance.tests_bank_integration

# Run specific test class
python manage.py test finance.tests_bank_integration.BankConnectionModelTests

# Run specific test method
python manage.py test finance.tests_bank_integration.BankConnectionModelTests.test_create_revolut_connection

# Run with verbose output
python manage.py test finance.tests_bank_integration -v 2

# Run and keep test database
python manage.py test finance.tests_bank_integration --keepdb
```

## 🛠️ Database Management

```bash
# Show pending migrations
python manage.py showmigrations finance

# Roll back migrations
python manage.py migrate finance 0002_userprofile

# Create new migration
python manage.py makemigrations finance --dry-run

# Apply specific migration
python manage.py migrate finance 0003_bank_integration
```

## 🐚 Django Shell

```bash
# Enter shell
python manage.py shell

# Inside shell:
from finance.models import BankConnection, BankTransaction
from finance.bank_services import BankServiceFactory

# Get user's connections
user = User.objects.get(username='testuser')
connections = BankConnection.objects.filter(user=user)

# Get balance
connection = connections.first()
service = BankServiceFactory.get_service(connection)
balance = service.get_balance()
print(balance)

# Sync transactions
synced = service.sync_transactions(days_back=30)
print(f"Synced {synced} transactions")

# View pending transactions
pending = BankTransaction.objects.filter(user=user, sync_status='pending')
for trans in pending:
    print(f"{trans.date}: {trans.amount} {trans.currency}")
```

## 📊 Django Admin

```bash
# Access admin
http://localhost:8000/admin/

# Login with superuser credentials
# Navigate to: Finance → Bank Connections
# Navigate to: Finance → Bank Transactions
```

## 📋 View URLs

```
http://localhost:8000/finance/banks/                          # List connections
http://localhost:8000/finance/banks/create/                   # Create connection
http://localhost:8000/finance/banks/dashboard/                # Dashboard
http://localhost:8000/finance/banks/sync/                     # Sync all
http://localhost:8000/finance/banks/1/sync/                   # Sync specific
http://localhost:8000/finance/banks/transactions/pending/     # View pending
http://localhost:8000/finance/banks/transactions/synced/      # View synced
http://localhost:8000/admin/finance/bankconnection/           # Admin connections
http://localhost:8000/admin/finance/banktransaction/          # Admin transactions
```

## ⚙️ Configuration

```python
# In moneymanager/settings.py:

BANK_API_TIMEOUT = 30  # seconds
BANK_AUTO_SYNC = True
BANK_SYNC_INTERVAL_HOURS = 6
BANK_DEFAULT_DAYS_BACK = 30
```

## 🐛 Debugging

```bash
# Enable debug logging
python manage.py sync_bank_transactions --verbosity 3

# View logs
tail -f logs/bank_sync.log

# Test API connection
python manage.py shell
>>> from finance.bank_services import RevolutBankService
>>> service = RevolutBankService(connection)
>>> service.get_balance()
```

## 📱 Cron Job Setup

### Linux/Mac
```bash
# Edit crontab
crontab -e

# Add line for daily sync at 6 AM
0 6 * * * cd /path/to/MoneyManager && python manage.py sync_bank_transactions

# Every 6 hours
0 */6 * * * cd /path/to/MoneyManager && python manage.py sync_bank_transactions

# Every 30 minutes
*/30 * * * * cd /path/to/MoneyManager && python manage.py sync_bank_transactions
```

### Windows Task Scheduler
```batch
# Create sync_banks.bat
@echo off
cd D:\MoneyManager
python manage.py sync_bank_transactions >> logs\bank_sync.log 2>&1

# Then schedule in Task Scheduler with desired interval
```

## 🔍 Verification Scripts

```bash
# Linux/Mac
bash SETUP_CHECKLIST.sh

# Windows PowerShell
powershell -ExecutionPolicy Bypass -File SETUP_CHECKLIST.ps1
```

## 📦 Requirements

```
Django==6.0.1
djangorestframework==3.16.1
python-decouple==3.8
requests==2.31.0          # Bank API calls
cryptography==41.0.0      # Token encryption (optional)
```

## 🚨 Troubleshooting Commands

```bash
# Check if tables exist
python manage.py dbshell
# Then: SELECT * FROM finance_bankconnection;

# Verify models are loaded
python manage.py shell
>>> from finance.models import BankConnection, BankTransaction
>>> print("Models loaded successfully")

# Test Revolut API
python manage.py shell
>>> from finance.bank_services import RevolutBankService
>>> service = RevolutBankService(connection)
>>> service.get_balance()

# Test BT API
python manage.py shell
>>> from finance.bank_services import BTBankService
>>> service = BTBankService(connection)
>>> service.get_balance()

# Check migration status
python manage.py showmigrations finance

# Inspect database
python manage.py dbshell
# .schema (SQLite)
# SHOW TABLES (MySQL)
# \dt (PostgreSQL)
```

## 📝 Useful Commands Chain

```bash
# Complete setup from scratch
pip install -r requirements.txt && \
python manage.py makemigrations finance && \
python manage.py migrate && \
python setup_bank_integration.py && \
python manage.py test finance.tests_bank_integration && \
python manage.py runserver

# Backup and restore
python manage.py dumpdata finance > finance_backup.json
python manage.py loaddata finance_backup.json

# Create test data
python manage.py shell < scripts/create_test_data.py

# Monitor sync process
watch -n 5 'python manage.py sync_bank_transactions --verbosity 2'
```

## 🔐 Security

```bash
# Change SECRET_KEY (production)
python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'

# Encrypt tokens
pip install django-encrypted-model-fields

# Check security issues
python manage.py check --deploy
```

## 📖 Documentation Files

- BANK_INTEGRATION_GUIDE.md - Complete guide
- BANK_INTEGRATION_QUICKSTART.md - Quick start
- BANK_INTEGRATION_SUMMARY.md - Implementation summary
- IMPLEMENTATION_STATUS.txt - Current status
- This file - Quick reference

## 🎯 Next Steps

1. Run setup: `python setup_bank_integration.py`
2. Start server: `python manage.py runserver`
3. Visit: http://localhost:8000/finance/banks/
4. Connect Revolut or BT account
5. Sync transactions
6. Review and accept transactions
7. Track balance and expenses

---

For detailed documentation, see BANK_INTEGRATION_GUIDE.md
