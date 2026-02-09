from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from allauth.socialaccount.models import SocialAccount
from .models import UserProfile, Transaction, Account, Budget
from .supabase_sync import sync_user_to_supabase, sync_profile_to_supabase, log_user_activity, log_transaction_activity
from .discord_notifications import (
    notify_transaction_created,
    notify_account_created,
    notify_budget_created,
    notify_user_joined,
    notify_discord_connected,
)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """Crează profil utilizator la înregistrare"""
    if created:
        UserProfile.objects.get_or_create(user=instance)
        # Sync to Supabase
        sync_user_to_supabase(instance)
        # Discord notification
        notify_user_joined(instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """Salvează profilul utilizatorului"""
    if hasattr(instance, 'profile'):
        instance.profile.save()
        # Sync to Supabase
        sync_profile_to_supabase(instance.profile)


@receiver(post_save, sender=SocialAccount)
def update_user_profile_from_discord(sender, instance, created, update_fields, **kwargs):
    """Actualizează profilul utilizatorului cu date de Discord la conectare"""
    if instance.provider == 'discord':
        try:
            user = instance.user
            profile, _ = UserProfile.objects.get_or_create(user=user)
            
            # Extrage date din Discord
            extra_data = instance.extra_data
            
            # Actualizează avatar URL
            if 'avatar' in extra_data:
                avatar_hash = extra_data['avatar']
                discord_id = extra_data.get('id', '')
                profile.avatar_url = f"https://cdn.discordapp.com/avatars/{discord_id}/{avatar_hash}.png"
            
            # Actualizează username și Discord ID
            if 'username' in extra_data:
                profile.discord_username = extra_data['username']
            
            if 'id' in extra_data:
                profile.discord_id = extra_data['id']
            
            # Actualizează user.first_name și last_name din Discord
            if 'username' in extra_data:
                user.first_name = extra_data.get('username', '')
                user.save()
            
            profile.save()
            
            # Sync to Supabase
            sync_profile_to_supabase(profile)
            sync_user_to_supabase(user)
            
            # Discord notification (only on first connection)
            if created:
                notify_discord_connected(user)
        except Exception as e:
            print(f"Eroare actualizare profil Discord: {e}")


@receiver(post_save, sender=Transaction)
def log_transaction_to_supabase(sender, instance, created, **kwargs):
    """Log transaction creation to Supabase"""
    if created:
        try:
            log_transaction_activity(instance.user, instance)
            # Discord notification
            notify_transaction_created(instance)
        except Exception as e:
            print(f"Eroare logging tranzacție: {e}")


@receiver(post_save, sender=Account)
def notify_account_creation(sender, instance, created, **kwargs):
    """Send Discord notification when account is created"""
    if created:
        try:
            notify_account_created(instance)
        except Exception as e:
            print(f"Eroare notificare cont Discord: {e}")


@receiver(post_save, sender=Budget)
def notify_budget_creation(sender, instance, created, **kwargs):
    """Send Discord notification when budget is created"""
    if created:
        try:
            notify_budget_created(instance)
        except Exception as e:
            print(f"Eroare notificare buget Discord: {e}")
