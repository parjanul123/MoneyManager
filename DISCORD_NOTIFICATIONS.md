# 🎮 Discord Notifications Setup Guide

Sistemul de notificări Discord al Money Manager îți permite să primești automat în Discord notificări pentru orice modificări în aplicație.

## 🚀 Quick Setup - 3 Pași

### 1. Creează un Webhook pe Discord

1. Deschide serverul Discord unde vrei să primești notificări
2. Selectează canalul trebuie să primești notificări (de ex. #general)
3. Click dreapta pe canal → **Edit Channel** (sau settings icon)
4. Mergi la **Integrations** → **Webhooks**
5. Click pe **Create Webhook** (sau New Webhook)
6. Dă-i un nume (de ex. "Money Manager")
7. Click pe **Copy Webhook URL**

Webhook URL-ul ar trebui să arate așa:
```
https://discord.com/api/webhooks/1234567890/abcdefghijk
```

### 2. Adaugă URL-ul în discord.ini

Deschide fișierul `discord.ini` și completează:

```ini
WEBHOOK_URL = https://discord.com/api/webhooks/YOUR_ID_HERE/YOUR_TOKEN_HERE
```

### 3. Restartează Serverul Django

```bash
py manage.py runserver
```

## 📊 Ce Notificări Primești?

Aplicația trimite automat notificări pentru:

### 💰 Tranzacții Noi
- **Culoare:** Roșu pentru cheltuieli, Verde pentru venituri
- **Info:** Utilizator, Cont, Categorie, Suma, Descriere, Data

### 🏦 Conturi Noi
- **Culoare:** Albastru
- **Info:** Utilizator, Nume Cont, Tip, Valută, Sold Inițial

### 📊 Bugete Noi
- **Culoare:** Portocaliu
- **Info:** Utilizator, Categorie, Buget, Lună

### 👤 Utilizatori Noi
- **Culoare:** Purpuriu
- **Info:** Utilizator, Email, Data Înregistrării

### 🔗 Discord Conectat
- **Culoare:** Albastru Discord
- **Info:** Când un utilizator conectează contul Discord

## 🧪 Testare

### Metoda 1: Prin Django Shell

```bash
py manage.py shell
```

```python
from finance.models import Transaction, Account, Category
from finance.discord_notifications import notify_transaction_created
from django.contrib.auth.models import User

# Luăm o tranzacție existentă
transaction = Transaction.objects.first()

# Testăm notificarea
if transaction:
    notify_transaction_created(transaction)
    print("✅ Notificare trimisă!")
else:
    print("❌ Nu sunt tranzacții pentru test")
```

### Metoda 2: Creează Date de Test

1. Deschide aplicația pe http://127.0.0.1:9512
2. Creează o nouă tranzacție
3. Ar trebui să primești notificare pe Discord imediat

## 📝 Exemplu de Notificare

Notificările primite au acest format:

```
💸 Cheltuială nouă
O nouă cheltuială a fost adăugată

Utilizator: John Doe
Cont: My Checking Account
Categorie: Food
Suma: 50.25 RON
Descriere: Grocery shopping
Data: 09.02.2026
```

## 🔧 Configurare Avansată

### Dezactivează Notificări

Dacă vrei să dezactivezi notificările, lasă `WEBHOOK_URL` gol în `discord.ini`:

```ini
WEBHOOK_URL = 
```

### Personalizează Notificările

Deschide `finance/discord_notifications.py` și modifică colori, texte, etc.

### Notificări Condiționare

Poți adăuga logică suplimentară în `finance/signals.py` pentru a trimite notificări doar în anumite condiții.

## ❌ Troubleshooting

### "Eroare trimitere notificare Discord"

1. **URL-ul webhook nu este corect:**
   - Verifică că URL-ul din discord.ini este complet și corect
   - Asigură-te că s-a copiat integral

2. **Webhook-ul a fost șters:**
   - Creează un webhook nou pe Discord
   - Actualizează URL-ul în discord.ini

3. **Permisiuni insuficiente:**
   - Asigură-te că bot-ul/aplicația Discord are acces la canal
   - Verifică permisiunile kanalului

4. **URL-ul este gol:**
   - Merge la `discord.ini` și completează `WEBHOOK_URL`
   - Restartează serverul Django

### Notificări nu apar

1. Verifică că `WEBHOOK_URL` este completat în `discord.ini`
2. Verifică logurile serverului pentru erori:
   ```bash
   # În terminal unde rulează Django
   # Ar trebui să vezi: "Discord notification sent:"
   ```
3. Restartează serverul Django
4. Creează o nouă tranzacție/cont/buget de test

## 📚 Funcții Disponibile

Din `finance/discord_notifications.py`:

```python
# Tranzacție
notify_transaction_created(transaction)

# Cont
notify_account_created(account)

# Buget
notify_budget_created(budget)
notify_budget_exceeded(budget, spent_amount)

# Utilizator
notify_user_joined(user)
notify_discord_connected(user)

# Tranzacție Mare
notify_large_transaction(transaction)

# Custom (toate funcțiile folosesc)
send_discord_message(title, description, fields, color)
```

## 💡 Tips & Tricks

1. **Crează Canale Separate:**
   - #transactions pentru tranzacții
   - #accounts pentru conturi
   - #budgets pentru bugete

2. **Culori Custom:**
   ```python
   # În discord_notifications.py, schimbă color parameter
   send_discord_message(
       "Titlu",
       "Descriere",
       fields,
       color=0xFF0000  # Roșu
   )
   ```

3. **Șabloane Diferite:**
   - Poți crea funcții noi în `discord_notifications.py`
   - Poți apela notificațiile din views în loc de signals

4. **Monitorizare:**
   - Trimite o notificare zilnică cu sumar zei
   - Notificări doar pentru tranzacții > 500 RON
   - Notificări când bugetul aproape se termină

## 🔐 Securitate

⚠️ **IMPORTANT:**
- Nu partaja URL-ul webhook cu nimeni
- Dacă URL-ul ajunge public, șterge webhook-ul și creează altul
- Webhook-ul are acces plin la canalul seu

## 📞 Support

Pentru probleme:
1. Verifică log-urile Django (terminal)
2. Testează webhook-ul direct: https://webhook.site/
3. Verifica că token-ul webhook este încă valid pe Discord
