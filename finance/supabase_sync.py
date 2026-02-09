"""
Supabase REST API Integration - Sync user data to Supabase
This bypasses direct database connection and uses HTTP/REST API instead
"""

import os
import requests
import json
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

SUPABASE_URL = os.environ.get('SUPABASE_API_URL', 'https://shwbounuzknxjvvebyym.supabase.co')
SUPABASE_KEY = os.environ.get('SUPABASE_ANON_KEY', '')
SUPABASE_SERVICE_KEY = os.environ.get('SUPABASE_SERVICE_KEY', '')

# Headers for Supabase API
HEADERS = {
    'Content-Type': 'application/json',
    'apikey': SUPABASE_KEY or SUPABASE_SERVICE_KEY,
}

# Default table names - adjust based on actual Supabase structure
USERS_TABLE = 'django_users'
ACTIVITY_TABLE = 'user_activity'
PROFILES_TABLE = 'django_user_profiles'


def sync_user_to_supabase(user):
    """
    Sync Django user registration data to Supabase
    
    Args:
        user: Django User instance
    
    Returns:
        dict: Response from Supabase or error info
    """
    if not SUPABASE_KEY and not SUPABASE_SERVICE_KEY:
        logger.warning("Supabase API keys not configured. Skipping sync.")
        return {'error': 'Supabase API keys not configured'}
    
    try:
        # Prepare user data for Supabase
        user_data = {
            'email': user.email,
            'username': user.username,
            'first_name': user.first_name or '',
            'last_name': user.last_name or '',
            'date_joined': user.date_joined.isoformat() if user.date_joined else None,
            'is_active': user.is_active,
            'django_user_id': user.id,
            'synced_at': datetime.now().isoformat(),
        }
        
        # Add profile info if exists
        if hasattr(user, 'profile'):
            user_data.update({
                'discord_id': user.profile.discord_id or '',
                'discord_username': user.profile.discord_username or '',
                'avatar_url': str(user.profile.avatar_url) if user.profile.avatar_url else '',
                'bio': user.profile.bio or '',
            })
        
        # Create table if doesn't exist - insert or update
        endpoint = f"{SUPABASE_URL}/rest/v1/{USERS_TABLE}"
        
        # Try to update if exists, else insert
        response = requests.post(
            endpoint,
            headers=HEADERS,
            json=user_data,
            timeout=10
        )
        
        if response.status_code in [200, 201]:
            logger.info(f"✓ Successfully synced user '{user.username}' to Supabase")
            # Also log activity
            log_user_activity(user, 'user_registered' if user.date_joined else 'user_updated')
            return {'success': True, 'data': response.json()}
        else:
            logger.error(f"✗ Failed to sync user to Supabase: {response.status_code} - {response.text}")
            return {'error': response.text, 'status_code': response.status_code}
    
    except Exception as e:
        logger.error(f"Exception syncing user to Supabase: {str(e)}")
        return {'error': str(e)}


def sync_profile_to_supabase(profile):
    """Sync user profile data to Supabase"""
    if not SUPABASE_KEY and not SUPABASE_SERVICE_KEY:
        return {'error': 'Supabase keys not configured'}
    
    try:
        profile_data = {
            'user_email': profile.user.email,
            'discord_id': profile.discord_id or '',
            'discord_username': profile.discord_username or '',
            'avatar_url': str(profile.avatar_url) if profile.avatar_url else '',
            'bio': profile.bio or '',
            'updated_at': profile.updated_at.isoformat() if profile.updated_at else None,
            'django_user_id': profile.user.id,
        }
        
        endpoint = f"{SUPABASE_URL}/rest/v1/{PROFILES_TABLE}"
        response = requests.post(
            endpoint,
            headers=HEADERS,
            json=profile_data,
            timeout=10
        )
        
        if response.status_code in [200, 201]:
            logger.info(f"✓ Synced profile for user '{profile.user.username}'")
            log_user_activity(profile.user, 'profile_updated')
            return {'success': True}
        else:
            logger.error(f"✗ Failed to sync profile: {response.status_code} - {response.text}")
            return {'error': response.text}
    
    except Exception as e:
        logger.error(f"Exception syncing profile: {str(e)}")
        return {'error': str(e)}


def log_user_activity(user, action, details=None):
    """
    Log user activity to Supabase activity table
    
    Args:
        user: Django User instance
        action: Action type (e.g., 'logged_in', 'user_registered', 'transaction_created')
        details: Optional additional details dict
    """
    if not SUPABASE_KEY and not SUPABASE_SERVICE_KEY:
        return {'error': 'Supabase keys not configured'}
    
    try:
        activity_data = {
            'user_id': user.id,
            'email': user.email,
            'username': user.username,
            'action': action,
            'timestamp': datetime.now().isoformat(),
        }
        
        if details:
            activity_data['details'] = json.dumps(details)
        
        endpoint = f"{SUPABASE_URL}/rest/v1/{ACTIVITY_TABLE}"
        response = requests.post(
            endpoint,
            headers=HEADERS,
            json=activity_data,
            timeout=10
        )
        
        if response.status_code in [200, 201]:
            logger.info(f"✓ Logged activity '{action}' for user '{user.username}'")
            return {'success': True}
        else:
            logger.error(f"✗ Failed to log activity: {response.status_code}")
            return {'error': response.text}
    
    except Exception as e:
        logger.error(f"Exception logging activity: {str(e)}")
        return {'error': str(e)}


def log_transaction_activity(user, transaction):
    """Log transaction creation/update"""
    details = {
        'transaction_id': transaction.id,
        'amount': float(transaction.amount),
        'type': transaction.type,
        'category': transaction.category.name if transaction.category else None,
        'account': transaction.account.name if transaction.account else None,
    }
    return log_user_activity(user, 'transaction_created', details)


def log_bank_connection_activity(user, bank_name, status):
    """Log bank connection attempt"""
    details = {
        'bank': bank_name,
        'status': status,
    }
    return log_user_activity(user, 'bank_connected', details)


def get_users_from_supabase():
    """Retrieve all synced users from Supabase"""
    if not SUPABASE_KEY and not SUPABASE_SERVICE_KEY:
        return []
    
    try:
        endpoint = f"{SUPABASE_URL}/rest/v1/{USERS_TABLE}"
        response = requests.get(endpoint, headers=HEADERS, timeout=10)
        
        if response.status_code == 200:
            return response.json()
        else:
            logger.error(f"Failed to fetch users: {response.status_code}")
            return []
    
    except Exception as e:
        logger.error(f"Exception fetching users: {str(e)}")
        return []


def get_user_activity_from_supabase(user_id=None):
    """Retrieve user activity logs from Supabase"""
    if not SUPABASE_KEY and not SUPABASE_SERVICE_KEY:
        return []
    
    try:
        endpoint = f"{SUPABASE_URL}/rest/v1/{ACTIVITY_TABLE}"
        
        if user_id:
            endpoint += f"?user_id=eq.{user_id}"
        
        response = requests.get(endpoint, headers=HEADERS, timeout=10)
        
        if response.status_code == 200:
            return response.json()
        else:
            logger.error(f"Failed to fetch activity: {response.status_code}")
            return []
    
    except Exception as e:
        logger.error(f"Exception fetching activity: {str(e)}")
        return []

