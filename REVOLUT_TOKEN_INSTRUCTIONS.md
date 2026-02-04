# 🔑 REVOLUT TOKEN - Instrucțiuni Corecte

## ❌ CE NU TREBUIE SĂ FACI

- ❌ **NU** folosi IBAN
- ❌ **NU** folosi BIC/SWIFT code (asta e pentru transferuri!)
- ❌ **NU** folosi parola ta Revolut
- ❌ **NU** folosi numărul cardului
- ❌ **NU** folosi cod de autentificare

## ✅ CE TREBUIE SĂ FACI

Tokenul este un **cod special generat în Revolut** pentru Money Manager.

---

## 🚀 OPȚIUNEA 1: Revolut App (Mobile) - Conturi Business

Dacă ai **Revolut Business**, API e mai ușor de găsit:

1. **Deschide Revolut App**
2. Mergi la: **Settings** (⚙️)
3. Caută: **"Business Tools"** / **"API & Webhooks"**
4. Click: **"Create API Key"** / **"Generate Token"**
5. Copie codul lung
6. Lipește la: http://localhost:8000/finance/banks/create/

---

## 🌐 OPȚIUNEA 2: Revolut Web Dashboard (RECOMANDATĂ!)

**IMPORTANT:** Dacă nu gasesti în app mobile, foloseste web:

1. Mergi la: https://app.revolut.com/ (pe computer)
2. Loghează-te cu contul tău Revolut
3. Mergi la: **Settings** (⚙️) → **Developer** 
4. Caută: **"API Keys"** / **"Personal API"**
5. Click: **"Create API Key"** / **"New Key"**
6. Dă nume: **"MoneyManager"**
7. Click: **"Generate"** / **"Create"**
8. **COPIAZĂ codul** (aXJpc18...)
9. **LIPEȘTE** la: http://localhost:8000/finance/banks/create/

---

## ⚠️ DACA NICI PE WEB NU GASESTI API?

**Posibil că contul tău nu are acces la API.** 

Revolut restricționează API accesul la:
- ❌ Conturi Standard (Personal) în anumite țări
- ✅ Revolut Business (are acces)
- ✅ Conturi Premium/Metal (uneori)

### Soluții:

**A) Contactează Revolut Support**
- Zii că vrei să accesezi API
- Cere: "Enable Personal API Access"
- De obicei sunt de acord și activează în 24h

**B) Upgrade la Revolut Business**
- Business accounts au API disponibil automat
- Free version (primele 2 luni)

**C) Folosi metodă alternativă**
- Conectează mai întâi **Banca Transilvania** (are OAuth2 direct)
- Va lucra și fără Revolut

---

## 🔍 GASIREA EXACTA A API-ULUI

### Pe Mobile App (Revolut):
```
Settings (⚙️)
  ├─ Preferences
  │   └─ Developer / API (pe Business)
  │
  ├─ Business Settings (daca ai Business)
  │   └─ API & Integration
  │       └─ API Keys
  │
  └─ Integrations
      └─ API / Developer
```

### Pe Web (https://app.revolut.com/):
```
Settings (⚙️) 
  ├─ Developer
  │   └─ API Keys ← AICI!
  │       └─ Create New
  │
  └─ Integrations
      └─ API
```

---

## ✅ DUPA CE AI TOKENUL:

1. Copiază codul lung (ex: `aXJpc18...`)
2. Du-te la: http://localhost:8000/finance/banks/create/
3. Selectează: **"Bank: Revolut"**
4. Paste în campo **"Token"**
5. Click **"Conectează"** ✅

---

## 🎯 RECOMANDARE FINALĂ

**DAĂ-I PE BANCA TRANSILVANIA PRIMA!**

- OAuth2 = mai simplu (doar login + aprob)
- Nu ai nevoie de token special
- Functionează instant

Mergi la: http://localhost:8000/finance/banks/create/
- Selectează: **Banca Transilvania**
- Click: **Autorizare BT**
- Login + Aprob
- GATA! ✅

Revenești la Revolut mai târziu când rezolvi API.

---

## 📞 SUPORT

**Revolut Support:**
- App → Settings → Help → Contact Support
- Email: support@revolut.com
- Cere: "Enable Personal API Access"

---

**TL;DR:** Daca nu gasesti API în Revolut, conectează mai întâi BT (e mai simplu), apoi resolve Revolut mai târziu! 🚀
