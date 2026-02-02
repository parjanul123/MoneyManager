#!/usr/bin/env python
"""
Create a custom Discord OAuth handler to debug the 401 error
"""

handler_code = '''
# /finance/views_debug.py - Custom debug handler for Discord OAuth

import logging
from django.http import JsonResponse
from allauth.socialaccount.providers.discord.provider import DiscordProvider
from allauth.socialaccount.providers.oauth2.views import OAuth2CallbackView

logger = logging.getLogger(__name__)

class DebugDiscordCallbackView(OAuth2CallbackView):
    """Custom Discord callback to debug 401 errors"""
    
    provider_class = DiscordProvider
    
    def get(self, request, *args, **kwargs):
        # Log all parameters
        code = request.GET.get('code')
        state = request.GET.get('state')
        error = request.GET.get('error')
        error_description = request.GET.get('error_description')
        
        logger.debug(f"Discord Callback received:")
        logger.debug(f"  Code: {code[:20]}...{code[-5:] if code else None}")
        logger.debug(f"  State: {state[:20]}...{state[-5:] if state else None}")
        logger.debug(f"  Error: {error}")
        logger.debug(f"  Error Description: {error_description}")
        logger.debug(f"  Full URL: {request.build_absolute_uri()}")
        logger.debug(f"  Request META: {dict(request.META)}")
        
        # Try to call parent
        try:
            response = super().get(request, *args, **kwargs)
            logger.debug(f"Parent response status: {response.status_code if hasattr(response, 'status_code') else 'N/A'}")
            return response
        except Exception as e:
            logger.error(f"Error in parent handler: {e}", exc_info=True)
            return JsonResponse({
                'error': str(e),
                'code': code,
                'state': state
            }, status=500)
'''

print(handler_code)

print("\n" + "="*60)
print("CREEAZĂ FIȘIERUL:")
print("="*60)
print("  Fișier: /finance/views_debug.py")
print("  Conținut: ^^ mai sus")
print()
print("APOI, ADAUGĂ ÎN /moneymanager/urls.py:")
print("  from finance.views_debug import DebugDiscordCallbackView")
print("  ")
print("  # Adaugă înainte de path('accounts/', include('allauth.urls'))")
print("  path('accounts/discord/login/callback/', DebugDiscordCallbackView.as_view(), name='discord_callback_debug'),")
print()
print("REPORNEȘTE serverul și testează OAuth")
print("Urmărește Django debug log pentru detalii")
