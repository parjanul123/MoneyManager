#!/usr/bin/env python
"""
Check Discord app configuration directly via Discord API
This requires a user with admin rights to the Discord application
"""

import requests
import json

print("""
╔════════════════════════════════════════════════════════════════╗
║  VERIFICARE APLICAȚIE DISCORD MANUALĂ                        ║
╚════════════════════════════════════════════════════════════════╝

Pentru a verifica configurația exact din Discord, trebuie să:

1. Intri pe https://discord.com/developers/applications
2. Selectezi aplicația "Money Manager" (ID: 1467859133091811349)
3. Mergi în "OAuth2" > "General"
4. Verifici că:
   - Client ID matches: 1467859133091811349
   - Client Secret (dacă nu îl mai ții minte, poți genera altul novo)
   - Redirect URLs include: http://127.0.0.1:9512/accounts/discord/login/callback/

5. IMPORTANTE:
   - Redirect URL trebuie să fie EXACT egal (port, http/https, path)
   - Client Secret ar trebui să fie ~24 caractere
   - OAuth2 URL Generator > Add URL: http://127.0.0.1:9512/accounts/discord/login/

Dacă ai generat nou Secret, copiază-l în discord.ini și rulează verify_discord.py

""")

import configparser
from pathlib import Path

config = configparser.ConfigParser()
if Path('discord.ini').exists():
    config.read('discord.ini')
    print("┌────────────────────────────────────────────────────────────────┐")
    print("│ VALORILE CURENTE DIN discord.ini:                              │")
    print("├────────────────────────────────────────────────────────────────┤")
    print(f"│ CLIENT_ID:    {config.get('discord', 'CLIENT_ID'):<40} │")
    print(f"│ CLIENT_SECRET (primii 10 chars): {config.get('discord', 'CLIENT_SECRET')[:10]}...                  │")
    print(f"│ REDIRECT_URL: {config.get('discord', 'REDIRECT_URL'):<25} │")
    print("└────────────────────────────────────────────────────────────────┘")

print("\n⚠️  ACTION REQUIRED:")
print("1. Deschide: https://discord.com/developers/applications/1467859133091811349/oauth2/general")
print("2. Verifică că Redirect URL are: http://127.0.0.1:9512/accounts/discord/login/callback/")
print("3. Dacă CLIENT_SECRET e altered, regenerează-l și copiază în discord.ini")
print("4. După actualizare, rulează: py verify_discord.py")
