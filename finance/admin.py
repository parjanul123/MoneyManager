from django.contrib import admin
from .models import Category, Account, Transaction, Budget, Savings, UserProfile, BankConnection, BankTransaction


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'discord_username', 'discord_id', 'updated_at']
    list_filter = ['updated_at']
    search_fields = ['user__username', 'discord_username', 'discord_id']
    readonly_fields = ['discord_id', 'avatar_url', 'updated_at']


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'type']
    list_filter = ['type']
    search_fields = ['name']


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ['name', 'type', 'balance', 'currency', 'user']
    list_filter = ['type', 'currency']
    search_fields = ['name', 'user__username']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ['date', 'account', 'category', 'type', 'amount', 'user']
    list_filter = ['type', 'category', 'date', 'account']
    search_fields = ['description', 'user__username']
    readonly_fields = ['created_at', 'updated_at']
    date_hierarchy = 'date'


@admin.register(Budget)
class BudgetAdmin(admin.ModelAdmin):
    list_display = ['month', 'category', 'amount', 'user']
    list_filter = ['month', 'category']
    search_fields = ['user__username', 'category__name']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(Savings)
class SavingsAdmin(admin.ModelAdmin):
    list_display = ['name', 'target_amount', 'current_amount', 'deadline', 'user']
    list_filter = ['is_active', 'deadline']
    search_fields = ['name', 'user__username']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(BankConnection)
class BankConnectionAdmin(admin.ModelAdmin):
    list_display = ['user', 'bank', 'account_name', 'is_active', 'api_last_sync', 'created_at']
    list_filter = ['bank', 'is_active', 'created_at']
    search_fields = ['user__username', 'account_name', 'account_number']
    readonly_fields = ['api_user_id', 'api_last_sync', 'created_at', 'updated_at']
    fieldsets = (
        ('Informații Utilizator', {
            'fields': ('user', 'bank', 'account_name', 'account_number')
        }),
        ('Credențiale API', {
            'fields': ('access_token', 'refresh_token'),
            'classes': ('collapse',),
        }),
        ('Status', {
            'fields': ('is_active', 'api_user_id', 'api_last_sync')
        }),
        ('Timestampuri', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )


@admin.register(BankTransaction)
class BankTransactionAdmin(admin.ModelAdmin):
    list_display = ['external_id', 'user', 'bank_connection', 'amount', 'currency', 'date', 'sync_status']
    list_filter = ['bank_connection__bank', 'sync_status', 'currency', 'date']
    search_fields = ['user__username', 'external_id', 'description', 'recipient_name']
    readonly_fields = ['external_id', 'created_at', 'updated_at']
    fieldsets = (
        ('Informații Tranzacție', {
            'fields': ('user', 'bank_connection', 'external_id', 'date')
        }),
        ('Detalii Financiare', {
            'fields': ('amount', 'currency', 'description')
        }),
        ('Detalii Destinație', {
            'fields': ('recipient_name', 'recipient_account'),
            'classes': ('collapse',),
        }),
        ('Sincronizare', {
            'fields': ('sync_status', 'synced_to_transaction')
        }),
        ('Timestampuri', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )
    actions = ['mark_as_pending', 'mark_as_synced', 'mark_as_ignored']

    def mark_as_pending(self, request, queryset):
        queryset.update(sync_status='pending')
    mark_as_pending.short_description = "Marchează ca pending"

    def mark_as_synced(self, request, queryset):
        queryset.update(sync_status='synced')
    mark_as_synced.short_description = "Marchează ca sincronizat"

    def mark_as_ignored(self, request, queryset):
        queryset.update(sync_status='ignored')
    mark_as_ignored.short_description = "Marchează ca ignorat"
