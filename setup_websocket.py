#!/usr/bin/env python
"""
Setup Django Channels WebSocket support for BT Pay
"""

import subprocess
import sys

def install_websocket_packages():
    """Install Django Channels and related packages"""
    
    packages = [
        'channels==4.0.0',
        'daphne==4.0.0',
        'channels-redis==4.1.0',
    ]
    
    print("📦 Installing WebSocket packages...")
    print("=" * 60)
    
    try:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install'] + packages)
        print("\n✅ WebSocket packages installed successfully!")
        print("\n📝 To run WebSocket server:")
        print("   daphne -b 0.0.0.0 -p 8000 moneymanager.asgi:application")
        print("\n📖 Or keep using runserver (HTTP only):")
        print("   python manage.py runserver")
        
        return True
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Error installing packages: {e}")
        return False

if __name__ == '__main__':
    success = install_websocket_packages()
    sys.exit(0 if success else 1)
