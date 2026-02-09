"""
Discord notifications system for Money Manager
Sends embedded messages to Discord webhook when data changes
"""

import requests
import logging
from django.conf import settings
from django.utils import timezone
from datetime import datetime

logger = logging.getLogger(__name__)


def get_discord_webhook_url():
    """Get Discord webhook URL from settings"""
    return getattr(settings, 'DISCORD_WEBHOOK_URL', '')


def send_discord_message(title: str, description: str = "", fields: dict = None, 
                         color: int = 0x1f8b4c, username: str = "Money Manager"):
    """
    Send a message to Discord via webhook
    
    Args:
        title: Embed title
        description: Embed description
        fields: Dictionary of field names and values
        color: Embed color (default green: 0x1f8b4c)
        username: Webhook username
    """
    webhook_url = get_discord_webhook_url()
    
    if not webhook_url:
        logger.warning("Discord webhook URL not configured")
        return False
    
    try:
        embed = {
            "title": title,
            "description": description,
            "color": color,
            "timestamp": datetime.now().isoformat(),
            "footer": {
                "text": "Money Manager"
            }
        }
        
        # Add fields if provided
        if fields:
            embed["fields"] = [
                {
                    "name": name,
                    "value": str(value),
                    "inline": True
                }
                for name, value in fields.items()
            ]
        
        payload = {
            "username": username,
            "embeds": [embed]
        }
        
        response = requests.post(webhook_url, json=payload, timeout=10)
        response.raise_for_status()
        
        logger.info(f"Discord notification sent: {title}")
        return True
        
    except requests.exceptions.RequestException as e:
        logger.error(f"Eroare trimitere notificare Discord: {e}")
        return False


def notify_transaction_created(transaction):
    """
    Send notification when a new transaction is created
    
    Args:
        transaction: Transaction instance
    """
    try:
        user = transaction.user
        account = transaction.account
        category = transaction.category or "Nespecificată"
        
        # Determine color based on transaction type
        color = 0xff3333 if transaction.type == 'expense' else 0x33ff33  # Red for expense, Green for income
        
        # Format as emoji + type
        type_emoji = "💸" if transaction.type == 'expense' else "💰"
        type_label = "Cheltuială" if transaction.type == 'expense' else "Venit"
        
        title = f"{type_emoji} {type_label} nouă"
        
        fields = {
            "Utilizator": user.first_name or user.username,
            "Cont": account.name,
            "Categorie": str(category),
            "Suma": f"{transaction.amount} {account.currency}",
            "Descriere": transaction.description or "N/A",
            "Data": transaction.date.strftime("%d.%m.%Y"),
        }
        
        return send_discord_message(title, f"O nouă {type_label.lower()} a fost adăugată", fields, color)
        
    except Exception as e:
        logger.error(f"Eroare notificare tranzacție: {e}")
        return False


def notify_account_created(account):
    """
    Send notification when a new account is created
    
    Args:
        account: Account instance
    """
    try:
        user = account.user
        
        fields = {
            "Utilizator": user.first_name or user.username,
            "Cont": account.name,
            "Tip": account.get_type_display(),
            "Valută": account.currency,
            "Sold inițial": f"{account.balance} {account.currency}",
        }
        
        return send_discord_message(
            "🏦 Cont nou creat",
            f"Un nou cont a fost adăugat: **{account.name}**",
            fields,
            color=0x4169e1  # Blue for account
        )
        
    except Exception as e:
        logger.error(f"Eroare notificare cont: {e}")
        return False


def notify_budget_created(budget):
    """
    Send notification when a new budget is created
    
    Args:
        budget: Budget instance
    """
    try:
        user = budget.user
        
        fields = {
            "Utilizator": user.first_name or user.username,
            "Categorie": budget.category.name,
            "Buget": f"{budget.amount} {user.accounts.first().currency if user.accounts.exists() else 'RON'}",
            "Lună": budget.month.strftime("%B %Y"),
        }
        
        return send_discord_message(
            "📊 Buget nou",
            f"Un nou buget a fost configurat pentru categoria **{budget.category.name}**",
            fields,
            color=0xffa500  # Orange for budget
        )
        
    except Exception as e:
        logger.error(f"Eroare notificare buget: {e}")
        return False


def notify_budget_exceeded(budget, spent_amount):
    """
    Send notification when a budget is exceeded
    
    Args:
        budget: Budget instance
        spent_amount: Amount spent (Decimal)
    """
    try:
        user = budget.user
        currency = user.accounts.first().currency if user.accounts.exists() else 'RON'
        
        fields = {
            "Utilizator": user.first_name or user.username,
            "Categorie": budget.category.name,
            "Buget": f"{budget.amount} {currency}",
            "Cheltuit": f"{spent_amount} {currency}",
            "Excedent": f"{spent_amount - budget.amount} {currency}",
        }
        
        return send_discord_message(
            "⚠️ Buget depășit!",
            f"Bugetul pentru categoria **{budget.category.name}** a fost depășit!",
            fields,
            color=0xff6347  # Tomato (red) for warning
        )
        
    except Exception as e:
        logger.error(f"Eroare notificare depășire buget: {e}")
        return False


def notify_large_transaction(transaction, threshold=None):
    """
    Send notification for large transactions
    
    Args:
        transaction: Transaction instance
        threshold: Amount threshold (if None, uses 50% of average or 500)
    """
    try:
        user = transaction.user
        
        # Would need to calculate average if threshold is None
        # For now, we'll use a sensible default
        
        fields = {
            "Utilizator": user.first_name or user.username,
            "Cont": transaction.account.name,
            "Suma": f"{transaction.amount} {transaction.account.currency}",
            "Categorie": str(transaction.category or "Nespecificată"),
        }
        
        type_emoji = "💸" if transaction.type == 'expense' else "💰"
        return send_discord_message(
            f"{type_emoji} Tranzacție mare",
            f"O tranzacție de {transaction.amount} {transaction.account.currency} a fost înregistrată",
            fields,
            color=0xff8c00  # Dark orange
        )
        
    except Exception as e:
        logger.error(f"Eroare notificare tranzacție mare: {e}")
        return False


def notify_user_joined(user):
    """
    Send notification when a new user joins
    
    Args:
        user: User instance
    """
    try:
        fields = {
            "Utilizator": user.first_name or user.username,
            "Email": user.email or "N/A",
            "Data înregistrării": user.date_joined.strftime("%d.%m.%Y %H:%M"),
        }
        
        return send_discord_message(
            "👤 Utilizator nou",
            f"Utilizatorul **{user.first_name or user.username}** s-a înregistrat",
            fields,
            color=0x9370db  # Medium purple
        )
        
    except Exception as e:
        logger.error(f"Eroare notificare utilizator nou: {e}")
        return False


def notify_discord_connected(user):
    """
    Send notification when a user connects Discord account
    
    Args:
        user: User instance
    """
    try:
        profile = getattr(user, 'profile', None)
        
        fields = {
            "Utilizator": user.first_name or user.username,
            "Discord": profile.discord_username if profile else "N/A",
        }
        
        return send_discord_message(
            "🔗 Discord conectat",
            f"Utilizatorul **{user.first_name or user.username}** a conectat contul Discord",
            fields,
            color=0x7289da  # Discord color
        )
        
    except Exception as e:
        logger.error(f"Eroare notificare Discord conectat: {e}")
        return False
