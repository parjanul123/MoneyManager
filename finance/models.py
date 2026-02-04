from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.contrib.postgres.fields import ArrayField
import json

class UserProfile(models.Model):
    """Model pentru profil utilizator cu date de Discord"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    avatar_url = models.URLField(blank=True, null=True)
    discord_id = models.CharField(max_length=100, blank=True)
    discord_username = models.CharField(max_length=255, blank=True)
    bio = models.TextField(blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Profil {self.user.username}"
    
    class Meta:
        verbose_name_plural = "User Profiles"


class Category(models.Model):
    """Model pentru categoriile de cheltuieli/venituri"""
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    type = models.CharField(
        max_length=10,
        choices=[('expense', 'Cheltuială'), ('income', 'Venit')],
        default='expense'
    )
    
    class Meta:
        verbose_name_plural = "Categories"
    
    def __str__(self):
        return self.name


class Account(models.Model):
    """Model pentru conturi bancare/portofel"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='accounts')
    name = models.CharField(max_length=100)
    type = models.CharField(
        max_length=20,
        choices=[
            ('checking', 'Cont curent'),
            ('savings', 'Cont economii'),
            ('wallet', 'Portofel'),
            ('investment', 'Investiții'),
        ],
        default='checking'
    )
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    currency = models.CharField(max_length=3, default='RON')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.name} ({self.currency})"
    
    class Meta:
        ordering = ['-created_at']


class Transaction(models.Model):
    """Model pentru tranzacții (venituri și cheltuieli)"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='transactions')
    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='transactions')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    
    type = models.CharField(
        max_length=10,
        choices=[('expense', 'Cheltuială'), ('income', 'Venit')],
        default='expense'
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True)
    date = models.DateField(default=timezone.now)
    time = models.TimeField(auto_now_add=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.get_type_display()} - {self.amount} {self.account.currency}"
    
    class Meta:
        ordering = ['-date', '-time']


class Budget(models.Model):
    """Model pentru bugete lunare"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='budgets')
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    month = models.DateField(help_text="Ziua va fi setată pe 1")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.category.name} - {self.amount} ({self.month.strftime('%B %Y')})"
    
    class Meta:
        ordering = ['-month']
        unique_together = ['user', 'category', 'month']


class Savings(models.Model):
    """Model pentru obiective de economii"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='savings_goals')
    name = models.CharField(max_length=100)
    target_amount = models.DecimalField(max_digits=10, decimal_places=2)
    current_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    deadline = models.DateField(null=True, blank=True)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
    
    def progress_percentage(self):
        if self.target_amount == 0:
            return 0
        return (self.current_amount / self.target_amount) * 100
    
    class Meta:
        ordering = ['-created_at']


class BankConnection(models.Model):
    """Model pentru conectările la API-urile bancilor"""
    BANK_CHOICES = [
        ('bt', 'Banca Transilvania'),
        ('revolut', 'Revolut'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bank_connections')
    bank = models.CharField(max_length=20, choices=BANK_CHOICES)
    account_name = models.CharField(max_length=100)
    account_number = models.CharField(max_length=50, blank=True)
    
    # Credențiale (criptate în producție)
    access_token = models.TextField(blank=True)
    refresh_token = models.TextField(blank=True)
    
    # Metadate API
    api_user_id = models.CharField(max_length=255, blank=True)
    api_last_sync = models.DateTimeField(null=True, blank=True)
    
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.get_bank_display()} ({self.account_name})"
    
    class Meta:
        unique_together = ['user', 'bank', 'api_user_id']
        verbose_name_plural = "Bank Connections"


class BankTransaction(models.Model):
    """Model pentru tranzacții sincronizate din bănci"""
    SYNC_STATUS_CHOICES = [
        ('pending', 'În așteptare'),
        ('synced', 'Sincronizat'),
        ('duplicated', 'Duplicat'),
        ('ignored', 'Ignorat'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bank_transactions')
    bank_connection = models.ForeignKey(BankConnection, on_delete=models.CASCADE, related_name='transactions')
    
    # ID unic din API
    external_id = models.CharField(max_length=255, unique=True)
    
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    currency = models.CharField(max_length=3, default='RON')
    description = models.TextField()
    date = models.DateTimeField()
    
    # Detalii suplimentare
    recipient_name = models.CharField(max_length=255, blank=True)
    recipient_account = models.CharField(max_length=100, blank=True)
    
    # Status sincronizare
    sync_status = models.CharField(max_length=20, choices=SYNC_STATUS_CHOICES, default='pending')
    synced_to_transaction = models.ForeignKey(
        Transaction, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='bank_source'
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.get_sync_status_display()} - {self.amount} {self.currency} ({self.date.date()})"
    
    class Meta:
        ordering = ['-date']
        verbose_name_plural = "Bank Transactions"
