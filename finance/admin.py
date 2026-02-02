from django.contrib import admin
from .models import Category, Account, Transaction, Budget, Savings, UserProfile


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
