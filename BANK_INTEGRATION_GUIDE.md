# 🏦 Integrare API Bancare - BT și Revolut

## Overview
Aplicația suportă sincronizarea automată a soldurilor și tranzacțiilor din:
- **Revolut** - Folosind Personal Token
- **Banca Transilvania (BT)** - Folosind Open Banking API (PSD2)

## Setup și Configurare

### 1. Instalare Pachete Python

Adaugă în `requirements.txt`:
```
requests==2.31.0
cryptography==41.0.0
```

Apoi instalează:
```bash
pip install -r requirements.txt
```

### 2. Creează Migrația pentru Baza de Date

```bash
python manage.py makemigrations finance
python manage.py migrate finance
```

### 3. Adaugă în `INSTALLED_APPS` (dacă nu este deja)

În `moneymanager/settings.py`:
```python
INSTALLED_APPS = [
    # ...
    'finance',
    # ...
]
```

---

## Configurare Revolut

### Obțin Personal Token

1. Deschide aplicația Revolut
2. Merge la **Settings** → **API**
3. Selectează **Create New Token**
4. Copiază token-ul generat

### Conectare în Aplicație

1. Mergi la `/finance/banks/create/`
2. Selectează **Revolut** din dropdown
3. Completează:
   - **Account Name**: Numele pe care vrei să-l dai (ex: "Revolut Privat")
   - **Access Token**: Token-ul copiat mai sus
4. Click **Conectează**

---

## Configurare Banca Transilvania

### Obțin Access Token (Open Banking)

**Opțiunea 1: Prin Portalul BT Open Banking**

1. Mergi pe [BT Open Banking](https://openbanking.banca-transilvania.ro/)
2. Crează un cont / Conectare
3. Generează o aplicație API
4. Obți:
   - `Client ID`
   - `Client Secret`
   - `Authorization URL`

**Opțiunea 2: Autentificare OAuth**

Pentru a obține token prin OAuth:

```bash
# 1. Deschide browser-ul și accesează URL-ul de autentificare
https://openapi.banca-transilvania.ro/oauth/authorize?
    client_id=YOUR_CLIENT_ID
    &redirect_uri=http://localhost:8000/finance/oauth/callback/
    &response_type=code
    &scope=accounts%20transactions

# 2. După autentificare, vei primi un CODE
# 3. Schimbă CODE-ul cu un TOKEN:

curl -X POST https://openapi.banca-transilvania.ro/oauth/token \
  -d "grant_type=authorization_code" \
  -d "code=YOUR_CODE" \
  -d "client_id=YOUR_CLIENT_ID" \
  -d "client_secret=YOUR_CLIENT_SECRET" \
  -d "redirect_uri=http://localhost:8000/finance/oauth/callback/"
```

### Conectare în Aplicație

1. Mergi la `/finance/banks/create/`
2. Selectează **Banca Transilvania** din dropdown
3. Completează:
   - **Account Name**: Numele contului (ex: "BT Curent RON")
   - **Access Token**: Token-ul obținut
4. Click **Conectează**

---

## Utilizare

### Dashboard Bancar

Accesează `/finance/banks/dashboard/` pentru o vedere generală:
- Lista conturilor conectate
- Tranzacții sincronizate recent
- Statistici pe ultimii 30 zile
- Numărul de tranzacții în așteptare

### Sincronizare Manuală

**1. Sincronizare pentru un singur cont:**
```
GET /finance/banks/<bank_id>/sync/
```

**2. Sincronizare pentru toate conturile:**
```
GET /finance/banks/sync/
```

### Revizuire Tranzacții

După sincronizare, tranzacțiile apar în status **"Pending"** la:
```
/finance/banks/transactions/pending/
```

Pentru fiecare tranzacție poți:
- ✓ **Acceptă** - Creează o înregistrare în contul tău
- ✗ **Ignora** - Marchează ca ignorată
- Alege categoria și descrierea

### Sincronizare Automată (Cron Job)

Configurează o sarcină periodică (ex: zilnică):

**Opțiunea 1: Cron Linux/Mac**

```bash
# Editează crontab
crontab -e

# Adaugă rând pentru sincronizare zilnică la ora 6:00 AM
0 6 * * * cd /path/to/MoneyManager && python manage.py sync_bank_transactions >> /var/log/bank_sync.log 2>&1
```

**Opțiunea 2: Django Background Tasks**

Instalează:
```bash
pip install celery redis
```

Sau folosește [django-crontab](https://github.com/dbader/django-crontab):
```bash
pip install django-crontab
```

În `settings.py`:
```python
CRONJOBS = [
    ('0 6 * * *', 'finance.management.commands.sync_bank_transactions'),
]
```

**Opțiunea 3: Windows Task Scheduler**

```batch
# Creează un batch file: sync_banks.bat
@echo off
cd D:\MoneyManager
python manage.py sync_bank_transactions
```

Apoi adaugă task în Task Scheduler cu trigger zilnic.

---

## API Endpoints

### Gestionare Conectări
- `GET /finance/banks/` - Lista conectări
- `POST /finance/banks/create/` - Creează conexiune
- `POST /finance/banks/<id>/delete/` - Șterge conexiune

### Sincronizare
- `POST /finance/banks/sync/` - Sincronizează toate conturile
- `POST /finance/banks/<id>/sync/` - Sincronizează un cont

### Tranzacții
- `GET /finance/banks/transactions/pending/` - Tranzacții în așteptare
- `POST /finance/banks/transactions/<id>/accept/` - Acceptă tranzacție
- `POST /finance/banks/transactions/<id>/ignore/` - Ignora tranzacție
- `GET /finance/banks/transactions/synced/` - Tranzacții acceptate

---

## Securitate

### ⚠️ Important:

1. **Token-uri**: În producție, stochează token-urile criptate!
   ```python
   # Instaleaza:
   pip install django-encrypted-model-fields
   ```

2. **Variabile de Mediu**: Nu pune token-uri în cod!
   ```python
   import os
   ACCESS_TOKEN = os.getenv('REVOLUT_TOKEN')
   ```

3. **HTTPS**: Folosește doar HTTPS în producție

4. **Rate Limiting**: API-urile au limite de apeluri. Configurează:
   ```python
   BANK_SYNC_TIMEOUT = 30  # secunde
   BANK_SYNC_RETRY = 3     # încercări
   ```

---

## Troubleshooting

### Eroare: "Invalid Token"
- Verifică dacă token-ul este corect
- Verifică dacă token-ul nu a expirat
- Pentru Revolut: regenerează token-ul dacă necesari

### Eroare: "401 Unauthorized"
- Token invalid sau expirat
- Pentru BT: Verifică dacă OAuth flow-ul a fost completat

### Nicio tranzacție sincronizată
- Verifică dacă banco are tranzacții în perioada selectată
- Verifică log-urile: `python manage.py sync_bank_transactions --user <user_id>`

### Connection Timeout
- Crește `timeout` în `bank_services.py`
- Verifică conexiunea la internet
- Verifică dacă API-ul băncii este disponibil

---

## Structura Modelelor

```
BankConnection
├── user (ForeignKey to User)
├── bank ('bt' sau 'revolut')
├── account_name (String)
├── access_token (Encrypted)
├── api_last_sync (DateTime)
└── is_active (Boolean)

BankTransaction
├── user (ForeignKey to User)
├── bank_connection (ForeignKey to BankConnection)
├── external_id (String, unique)
├── amount (Decimal)
├── currency (String)
├── date (DateTime)
├── sync_status ('pending', 'synced', 'duplicated', 'ignored')
└── synced_to_transaction (ForeignKey to Transaction)
```

---

## Exemplu de Flux Complet

```
1. Utilizator merge la /finance/banks/create/
   ↓
2. Selectează Revolut și introdu token
   ↓
3. Sistemul testează conexiunea și obține soldul
   ↓
4. Se creează BankConnection și se sincronizează tranzacțiile
   ↓
5. Tranzacțiile noi apare în /finance/banks/transactions/pending/
   ↓
6. Utilizator revizuiește și alege categoria
   ↓
7. Click "Accept" → Se creează Transaction și se actualizează Account
   ↓
8. Tranzacția apare în /finance/transactions/
```

---

## Comenzi Utile

```bash
# Sincronizare manuală pentru toți utilizatorii
python manage.py sync_bank_transactions

# Sincronizare pentru un utilizator specific
python manage.py sync_bank_transactions --user 1

# Sincronizare doar Revolut
python manage.py sync_bank_transactions --bank revolut

# Sincronizare din ultimele 7 zile
python manage.py sync_bank_transactions --days 7

# Combo
python manage.py sync_bank_transactions --user 1 --bank bt --days 14
```

---

## Roadmap Viitor

- [ ] Suport pentru mai multe bănci (ING, UniCredit, etc.)
- [ ] Criptare automată token-uri
- [ ] OAuth2 flow automat
- [ ] Machine Learning pentru categorizare automată
- [ ] Export CSV/PDF
- [ ] API RESTful public
- [ ] Notificări real-time
- [ ] Multi-currency consolidare

---

## Suport și FAQ

**Q: Pot folosi mai multe conturi din aceași bancă?**
A: Da! Fiecare conexiune este independentă.

**Q: Ce se întâmplă dacă token-ul expira?**
A: Sincronizarea va eșua cu eroare 401. Regenerează token-ul și actualizează conexiunea.

**Q: Datele sunt sigure?**
A: Stochează-le criptat în producție. Niciodată nu transmitem datele către terți.

**Q: Pot șterge o conexiune?**
A: Da, dar tranzacțiile sincronizate anterior rămân în sistem.

**Q: Cum pot exporta datele?**
A: Merge la /finance/transactions/ și folosește export (dacă disponibil).

---

**Ultima actualizare**: 4 februarie 2026
