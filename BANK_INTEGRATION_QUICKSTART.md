# 🏦 Bank Integration Setup - QuickStart

## 🚀 Instalare Rapidă (5 minute)

### 1️⃣ Instalează Pachete
```bash
pip install -r requirements.txt
```

### 2️⃣ Aplică Migrațiile
```bash
python manage.py makemigrations finance
python manage.py migrate
```

### 3️⃣ Setup Categorii
```bash
python setup_bank_integration.py
```

### 4️⃣ Creează SuperUser (dacă nu ai)
```bash
python manage.py createsuperuser
```

---

## 📱 Conectare Bănci

### Revolut
1. Deschide aplicația Revolut
2. **Settings → API → Create New Token**
3. Copiază token-ul
4. Mergi la `http://localhost:8000/finance/banks/create/`
5. Selectează **Revolut**, completează token-ul
6. Click **Conectează**

### Banca Transilvania
1. Mergi pe [Open Banking BT](https://openbanking.banca-transilvania.ro/)
2. Creează o aplicație API
3. Obți access token (OAuth)
4. Mergi la `http://localhost:8000/finance/banks/create/`
5. Selectează **BT**, completează token-ul
6. Click **Conectează**

---

## 🔄 Sincronizare

### Manual
```
/finance/banks/sync/
```

### Command Line
```bash
python manage.py sync_bank_transactions
```

### Automat (Cron)
```bash
0 6 * * * cd /path/to/MoneyManager && python manage.py sync_bank_transactions
```

---

## 📊 Dashboard

- **Dashboard**: `/finance/banks/dashboard/`
- **Conturi**: `/finance/banks/`
- **Tranzacții Pending**: `/finance/banks/transactions/pending/`
- **Admin**: `/admin/` → Finance

---

## 📝 Fișiere Principale

| Fișier | Descriere |
|--------|-----------|
| `finance/bank_services.py` | Logica API (Revolut, BT) |
| `finance/bank_views.py` | Vederile web |
| `finance/models.py` | Modele BankConnection, BankTransaction |
| `finance/forms.py` | Formulare conectare |
| `BANK_INTEGRATION_GUIDE.md` | Documentație completă |

---

## ⚙️ Configurări (settings.py)

```python
# Bank API Timeouts
BANK_API_TIMEOUT = 30  # secunde

# Sincronizare automată
BANK_AUTO_SYNC_ENABLED = True
BANK_AUTO_SYNC_DAYS = 30
```

---

## 🐛 Troubleshooting

### Eroare: "No such table"
```bash
python manage.py migrate
```

### Eroare: "Invalid Token"
- Regenerează token-ul din app-ul bancii
- Verifică dacă token-ul nu a expirat

### Nicio tranzacție
```bash
python manage.py sync_bank_transactions --user 1 --days 60
```

---

## 📖 Documentație Completă

Vezi: **BANK_INTEGRATION_GUIDE.md**

---

## 🆘 Suport

- Log-uri: `python manage.py sync_bank_transactions` (verbose)
- Admin interface: `/admin/finance/`
- Django shell: `python manage.py shell`

---

**Setup complet! 🎉**
