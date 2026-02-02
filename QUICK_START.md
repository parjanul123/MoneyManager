# 🚀 PORNIRE RAPIDĂ - Money Manager

## Prima Dată

### 1. Crează Superutilizator (Admin)
```bash
py manage.py createsuperuser
```
- Username: admin
- Email: admin@money.com
- Password: alege o parolă

### 2. Pornește Serverul
```bash
py manage.py runserver
```

Sau pe Windows, fă dublu-click pe: `run.bat`

## Accesare

- **Aplicație:** http://localhost:8000/finance/
- **Admin:** http://localhost:8000/admin/

## Primii Pași

1. Login cu credențialele create anterior
2. Mergi la **Conturi** și crează un cont (ex: "Portofel - 1000 RON")
3. Mergi la **Tranzacții** și adaugă câteva tranzacții
4. Mergi la **Bugete** și stabilește bugete lunare
5. Mergi la **Rapoarte** pentru a vedea analizele

## Probleme Frecvente

### Virtual Environment nu se activează
```bash
# Windows:
venv\Scripts\activate

# Linux/Mac:
source venv/bin/activate
```

### Port 8000 este deja ocupat
```bash
py manage.py runserver 8001
# sau
py manage.py runserver 0.0.0.0:9000
```

### Bază de date coruptă
```bash
# Ștergere și reinitializare
del db.sqlite3
py manage.py migrate
py init_categories.py
py manage.py createsuperuser
```

## Structura Aplicației

```
/finance/
  └── Secțiunea cu gestionarea banilor
    ├── Dashboard - Vizualizare rapidă
    ├── Conturi - Gestionare conturi
    ├── Tranzacții - Cheltuieli și venituri
    ├── Bugete - Planificare lunar
    ├── Economii - Obiective de economii
    └── Rapoarte - Analize și grafice
```

## Dată și Oră

Aplicația folosește timezone: **Europe/Bucharest**
Limba: **Română**

## Suport

Pentru mai mult detalii, citește **README.md**
