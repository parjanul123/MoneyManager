#!/usr/bin/env python
"""
Create middleware to log all HTTP requests/responses, especially OAuth ones
"""

middleware_code = '''
# /moneymanager/logging_middleware.py

import logging
import json
from django.utils.deprecation import MiddlewareMixin

logger = logging.getLogger(__name__)

class RequestLoggingMiddleware(MiddlewareMixin):
    """Log all requests and responses for debugging"""
    
    def process_request(self, request):
        if 'discord' in request.path or 'oauth' in request.path.lower():
            logger.info(f"📥 REQUEST: {request.method} {request.path}")
            logger.info(f"   Query: {request.GET.dict()}")
            if request.META.get('CONTENT_TYPE'):
                logger.info(f"   Content-Type: {request.META['CONTENT_TYPE']}")
        return None
    
    def process_response(self, request, response):
        if 'discord' in request.path or 'oauth' in request.path.lower():
            logger.info(f"📤 RESPONSE: {response.status_code} for {request.method} {request.path}")
            if response.status_code >= 400:
                logger.error(f"   ⚠️  ERROR Response: {response.status_code}")
                try:
                    if hasattr(response, 'content'):
                        logger.error(f"   Body: {response.content[:500]}")
                except:
                    pass
        return response
'''

print(middleware_code)

print("\n" + "="*60)
print("INSTRUCȚIUNI:")
print("="*60)
print("1. Creează fișier: /moneymanager/logging_middleware.py")
print("2. Copiază codul de mai sus în fișier")
print("3. Adaugă în settings.py MIDDLEWARE array:")
print("   'moneymanager.logging_middleware.RequestLoggingMiddleware',")
print("   (preferabil la FINAL, după alte middleware)")
print("4. Repornește serverul")
print("5. Testează Discord OAuth și verifică console output")
