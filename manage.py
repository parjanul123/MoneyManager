#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
import webbrowser
import time
import threading


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'moneymanager.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    
    # Setează port default pe 9512 dacă rulezi 'runserver' fără parametri
    if len(sys.argv) == 2 and sys.argv[1] == 'runserver':
        sys.argv.append('127.0.0.1:9512')
        
        # Deschide browser-ul pe login page după ce serverul pornește
        def open_browser():
            time.sleep(2)  # Asteaptă 2 secunde ca serverul să pornească
            login_url = 'http://127.0.0.1:9512/accounts/login/'
            webbrowser.open(login_url)
            print(f'\n✅ Browser deschis pe: {login_url}\n')
        
        # Pornește deschiderea în thread separat
        browser_thread = threading.Thread(target=open_browser, daemon=True)
        browser_thread.start()
    
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
