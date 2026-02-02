# /moneymanager/logging_middleware.py

import logging
from django.utils.deprecation import MiddlewareMixin

logger = logging.getLogger(__name__)

class RequestLoggingMiddleware(MiddlewareMixin):
    """Log all OAuth-related requests and responses for debugging"""
    
    def process_request(self, request):
        if 'discord' in request.path or 'oauth' in request.path.lower() or 'accounts' in request.path:
            logger.info(f"📥 REQUEST: {request.method} {request.path}")
            logger.info(f"   Query params: {dict(request.GET)}")
        return None
    
    def process_response(self, request, response):
        if 'discord' in request.path or 'oauth' in request.path.lower() or 'accounts' in request.path:
            logger.info(f"📤 RESPONSE: {response.status_code} for {request.method} {request.path}")
            if response.status_code >= 400:
                logger.error(f"   ⚠️  ERROR Status: {response.status_code}")
        return response
