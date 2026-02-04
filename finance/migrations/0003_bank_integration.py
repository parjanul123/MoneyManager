# Generated migration for bank integration

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('finance', '0002_userprofile'),
    ]

    operations = [
        migrations.CreateModel(
            name='BankConnection',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bank', models.CharField(choices=[('bt', 'Banca Transilvania'), ('revolut', 'Revolut')], max_length=20)),
                ('account_name', models.CharField(max_length=100)),
                ('account_number', models.CharField(blank=True, max_length=50)),
                ('access_token', models.TextField(blank=True)),
                ('refresh_token', models.TextField(blank=True)),
                ('api_user_id', models.CharField(blank=True, max_length=255)),
                ('api_last_sync', models.DateTimeField(blank=True, null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bank_connections', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Bank Connections',
                'unique_together': {('user', 'bank', 'api_user_id')},
            },
        ),
        migrations.CreateModel(
            name='BankTransaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('external_id', models.CharField(max_length=255, unique=True)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=15)),
                ('currency', models.CharField(default='RON', max_length=3)),
                ('description', models.TextField()),
                ('date', models.DateTimeField()),
                ('recipient_name', models.CharField(blank=True, max_length=255)),
                ('recipient_account', models.CharField(blank=True, max_length=100)),
                ('sync_status', models.CharField(choices=[('pending', 'În așteptare'), ('synced', 'Sincronizat'), ('duplicated', 'Duplicat'), ('ignored', 'Ignorat')], default='pending', max_length=20)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('bank_connection', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='transactions', to='finance.bankconnection')),
                ('synced_to_transaction', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='bank_source', to='finance.transaction')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bank_transactions', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Bank Transactions',
                'ordering': ['-date'],
            },
        ),
    ]
