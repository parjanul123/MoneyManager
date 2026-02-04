"""
Management command pentru sincronizarea periodică a tranzacțiilor bancare
Folosire: python manage.py sync_bank_transactions
"""
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from finance.bank_services import sync_all_banks, update_account_balance
from finance.models import BankConnection
import logging

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Sincronizează tranzacții din bănci pentru toți utilizatorii'

    def add_arguments(self, parser):
        parser.add_argument(
            '--user',
            type=int,
            help='ID-ul utilizatorului pentru sincronizare (dacă omis, sincronizează toți)',
        )
        parser.add_argument(
            '--days',
            type=int,
            default=30,
            help='Sincronizează tranzacții din ultimele N zile (default: 30)',
        )
        parser.add_argument(
            '--bank',
            type=str,
            choices=['bt', 'revolut'],
            help='Sincronizează doar o bancă specifică',
        )

    def handle(self, *args, **options):
        user_id = options.get('user')
        days_back = options.get('days')
        bank_filter = options.get('bank')

        if user_id:
            try:
                user = User.objects.get(id=user_id)
                users = [user]
                self.stdout.write(f"Sincronizare pentru utilizatorul: {user.username}")
            except User.DoesNotExist:
                raise CommandError(f"Utilizatorul cu ID {user_id} nu există")
        else:
            users = User.objects.filter(bank_connections__isnull=False).distinct()
            self.stdout.write(f"Sincronizare pentru {users.count()} utilizatori")

        total_synced = 0

        for user in users:
            try:
                self.stdout.write(f"\n► Sincronizare {user.username}...")

                connections = BankConnection.objects.filter(
                    user=user,
                    is_active=True
                )

                if bank_filter:
                    connections = connections.filter(bank=bank_filter)

                for connection in connections:
                    try:
                        self.stdout.write(f"  ► {connection.get_bank_display()}...", ending='')

                        from finance.bank_services import BankServiceFactory
                        service = BankServiceFactory.get_service(connection)
                        synced = service.sync_transactions(days_back=days_back)

                        # Actualizează soldul
                        update_account_balance(connection)

                        self.stdout.write(f" ✓ ({synced} tranzacții)")
                        total_synced += synced

                    except Exception as e:
                        self.stdout.write(
                            self.style.ERROR(f"  ✗ Eroare: {str(e)}")
                        )
                        logger.error(f"Sync error for {connection.get_bank_display()}: {str(e)}")

            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f"✗ Eroare pentru {user.username}: {str(e)}")
                )
                logger.error(f"Error syncing user {user.username}: {str(e)}")

        self.stdout.write(
            self.style.SUCCESS(f"\n✓ Sincronizate total {total_synced} tranzacții!")
        )
