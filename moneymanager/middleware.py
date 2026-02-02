from django.contrib.auth import logout
from django.urls import resolve, Resolver404

class ForceLoginOnEveryRequest:
    """
    Middleware care forțează login-ul la fiecare intrare pe site
    Deconectează utilizatorul după procesarea fiecărui request
    Exclude: login, accounts (OAuth), logout, static files
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
        # URL-uri care nu necesită logout (login, accounts, etc)
        self.exempt_paths = [
            'account_login',
            'account_logout', 
            'account_signup',
            'socialaccount_login',
            'socialaccount_signup',
            'socialaccount_callback',
            'socialaccount_connections',
            'discord_login',
            'discord_callback',
        ]
        # Pathuri care trebuie exclude
        self.exempt_prefixes = [
            '/accounts/',
            '/static/',
            '/admin/',
            '/favicon.ico',
        ]
    
    def __call__(self, request):
        response = self.get_response(request)
        
        # NU logout-ează la URL-urile exempt
        for prefix in self.exempt_prefixes:
            if request.path.startswith(prefix):
                return response
        
        # Verific dacă utilizatorul este autenticat
        if request.user and request.user.is_authenticated:
            try:
                # Obțin URL name-ul curent
                resolved = resolve(request.path)
                url_name = resolved.url_name
                
                # Dacă nu e în lista de exempt, logout-ează
                if url_name and url_name not in self.exempt_paths:
                    logout(request)
            except (Resolver404, AttributeError):
                # Dacă nu se poate rezolva URL-ul, logout-ează
                logout(request)
        
        return response
