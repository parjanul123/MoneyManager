# /finance/views_login.py

from django.shortcuts import render
from django.views import View
from allauth.account.forms import LoginForm

class CustomLoginView(View):
    """Arată login page cu ambele opțiuni (Discord + Form clasic)"""
    
    template_name = 'registration/login.html'
    
    def get(self, request):
        # Pasează form-ul în context pentru ambele opțiuni de login
        form = LoginForm()
        return render(request, self.template_name, {'form': form})
    
    def post(self, request):
        # POST-ul e tratat de allauth din accounts/
        form = LoginForm(request.POST)
        if form.is_valid():
            return render(request, self.template_name, {'form': form})
        return render(request, self.template_name, {'form': form})



