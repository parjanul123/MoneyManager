# Money Manager - Aplicație Django de Gestionare a Banilor

O aplicație Django completă pentru gestionarea finanțelor personale, urmărirea cheltuielilor și veniturilor, stabilirea bugetelor și obiectivelor de economii.

## 🚀 Funcționalități

- **Dashboard** - Vizualizare rapidă a soldului total și statisticilor lunare
- **Gestionarea Conturilor** - Creare și gestionarea mai multor conturi bancare
- **Tranzacții** - Înregistrare și urmărire a cheltuielilor și veniturilor
- **Bugete** - Stabilire de bugete lunare pe categorii
- **Obiective de Economii** - Urmărire progres pentru obiectivele de economii
- **Rapoarte** - Analize vizuale ale cheltuielilor și veniturilor
- **Filtrare** - Filtrare avansată a tranzacțiilor
- **Interfață Responsivă** - Design modern cu Bootstrap 5

## 📋 Cerințe

- Python 3.8+
- Django 6.0+
- SQLite (inclus)

## 🔧 Instalare și Configurare

### 1. Clonează sau descarcă proiectul

```bash
cd D:\MoneyManager
```

### 2. Activează mediul virtual

```bash
# Pe Windows:
.\venv\Scripts\activate

# Pe Linux/Mac:
source venv/bin/activate
```

### 3. Instalează dependențele (dacă nu sunt deja instalate)

```bash
pip install django djangorestframework python-decouple
```

### 4. Aplică migrațiile

```bash
python manage.py migrate
```

### 5. Inițializează categoriile predefinite

```bash
python init_categories.py
```

### 6. Creează superutilizator (admin)

```bash
python manage.py createsuperuser
```

Urmează instrucțiunile și introdu:
- Username: (alege un username)
- Email: (introdu emailul tău)
- Password: (alege o parolă)

## ▶️ Pornirea Aplicației

```bash
python manage.py runserver
```

Aplicația va fi disponibilă la: **http://127.0.0.1:8000**

### Accesare Admin Panel

1. Mergi la: http://127.0.0.1:8000/admin
2. Conectează-te cu credențialele tale de superutilizator
3. Gestionează categoriile, conturile și alte date

### Accesare Dashboard

1. Mergi la: http://127.0.0.1:8000/finance/
2. Vei fi redirecționat la login (pentru prima vizită trebuie să fi conectat)
3. După login, vei vedea dashboard-ul cu toate funcționalitățile

## 📱 Structura Proiectului

```
MoneyManager/
├── moneymanager/          # Folder configurare proiect
│   ├── settings.py        # Setări Django
│   ├── urls.py            # URL-uri principale
│   └── wsgi.py
├── finance/               # Aplicația principală
│   ├── models.py          # Modelele de date
│   ├── views.py           # Logica afișare
│   ├── forms.py           # Formulare
│   ├── admin.py           # Configurare admin
│   ├── urls.py            # URL-uri aplicație
│   ├── migrations/        # Migrații bază de date
│   └── templates/
│       └── finance/       # Template-uri HTML
├── manage.py              # Management script
└── init_categories.py     # Script inițializare
```

## 🗂️ Modele de Date

### Category (Categorie)
- `name` - Denumirea categoriei
- `description` - Descriere
- `type` - Tip (cheltuială/venit)

### Account (Cont)
- `user` - Utilizator asociat
- `name` - Denumirea contului
- `type` - Tip cont (curent, economii, portofel, investiții)
- `balance` - Sold disponibil
- `currency` - Monedă (default RON)

### Transaction (Tranzacție)
- `user` - Utilizator
- `account` - Contul asociat
- `category` - Categorie
- `type` - Tip (cheltuială/venit)
- `amount` - Suma
- `description` - Descriere
- `date` - Data tranzacției

### Budget (Buget)
- `user` - Utilizator
- `category` - Categorie
- `amount` - Suma bugetată
- `month` - Luna la care se aplică

### Savings (Economii)
- `user` - Utilizator
- `name` - Denumire obiectiv
- `target_amount` - Suma țintă
- `current_amount` - Suma acumulată
- `deadline` - Termen limită (opțional)
- `is_active` - Activ/Inactiv

## 🎯 Cazuri de Utilizare

### 1. Creare Cont Nou
1. Mergi la **Conturi**
2. Apasă **Cont Nou**
3. Completează formularul (Nume, Tip, Sold inițial, Monedă)
4. Salvează

### 2. Adaugare Tranzacție
1. Mergi la **Tranzacții** sau apasă butonul de pe Dashboard
2. Apasă **Tranzacție Nouă**
3. Selectează contul, categoria, tipul (cheltuială/venit)
4. Introdu suma și descriere
5. Salvează

### 3. Stabilire Buget Lunar
1. Mergi la **Bugete**
2. Apasă **Buget Nou**
3. Selectează categoria și luna
4. Introdu suma bugetată
5. Salvează

### 4. Urmărire Obiective de Economii
1. Mergi la **Economii**
2. Apasă **Obiectiv Nou**
3. Introdu nume, suma țintă, suma curentă și termen
4. Salvează

## 📊 Rapoarte și Analize

În secțiunea **Rapoarte** poți vedea:
- Grafice cu cheltuielile pe categorii
- Grafice cu veniturile pe categorii
- Procent de progres pentru fiecare categorie

## 🔐 Securitate

- Utilizatorii pot vedea doar propriile date
- Parole sunt hash-uite și securizate
- CSRF protection activat

## 🛠️ Comenzi Utile

```bash
# Creare superutilizator
python manage.py createsuperuser

# Ștergere bază de date și reset (NU folosi în producție!)
python manage.py migrate zero finance
rm db.sqlite3

# Generare export date
python manage.py dumpdata > backup.json

# Restaurare date
python manage.py loaddata backup.json
```

## 📝 Categorii Predefinite

### Cheltuieli
- Hrană
- Transport
- Chirie
- Utilități
- Sănătate
- Educație
- Divertisment
- Cumpărături
- Telefon/Internet
- Siguranță

### Venituri
- Salariu
- Freelance
- Bonus
- Vânzări
- Dobanzi

## 🚀 Implementări Viitoare

- [ ] Export CSV/PDF pentru rapoarte
- [ ] Notificări pentru bugete depășite
- [ ] Grafice avansate cu Chart.js
- [ ] Clasificare automată a tranzacțiilor
- [ ] API REST
- [ ] Aplicație mobilă
- [ ] Importare din bănci
- [ ] Cripare date sensibile

## 📄 Licență

Acest proiect este liber de a fi folosit și modificat.

## 👨‍💻 Suport

Pentru probleme sau sugestii, contactează dezvoltatorul.

---

**Versiune:** 1.0.0  
**Data:** Februarie 2026
"# MoneyManager" 
