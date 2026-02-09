# 🔗 Obținere API Tokens pentru Conectare Conturi Bancare

## 1. REVOLUT - Personal Token

### Pasii de obținere:

1. **Deschide aplicația Revolut pe telefon**
2. Mergi la: **Settings** → **API** (sau **Developer**)
3. Click pe **"Create New Token"** / **"Generate Token"**
4. Copiază token-ul generat (este o lungă secvență de caractere)
5. **Cuvântul cheie:** Nu-l mai pierzi din nou

### Link util:
- [📖 Documentația Revolut API](https://revolut.com/business/api/)

---

## 2. BANCA TRANSILVANIA - Open Banking API (PSD2)

### Pasii de obținere:

#### Opțiunea A: Contact Direct BT (dacă portalul leurs nu funcționează)

1. **Contactează Banca Transilvania:**
   - 📞 Call Center: 0371 311 311
   - 🌐 Email: openbanking@banca-transilvania.ro
   - Solicită: Client ID + Client Secret pentru Open Banking API

2. **Completează cererea cu:**
   - Nume aplicație: MoneyManager
   - Redirect URI: `http://localhost:9512/finance/oauth/callback/`
   - Scopes necesare: accounts, transactions

#### Opțiunea B: OAuth Flow (După obținerea Client ID/Secret)

1. **Înlocuiește valorile în URL:**
```
https://openapi.banca-transilvania.ro/oauth/authorize?client_id=YOUR_CLIENT_ID&redirect_uri=http://localhost:9512/finance/oauth/callback/&response_type=code&scope=accounts%20transactions
```

2. **După autentificare, vei primi un CODE în URL**
3. **Schimbă CODE cu ACCESS TOKEN:**
```bash
curl -X POST https://openapi.banca-transilvania.ro/oauth/token \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "grant_type=authorization_code" \
  -d "code=YOUR_CODE" \
  -d "client_id=YOUR_CLIENT_ID" \
  -d "client_secret=YOUR_CLIENT_SECRET" \
  -d "redirect_uri=http://localhost:9512/finance/oauth/callback/"
```

### Link-uri utile:

**REVOLUT:**
- **[🔐 Revolut API Docs](https://revolut.com/business/api/)**

**BANCA TRANSILVANIA:**
- **📧 Email:** openbanking@banca-transilvania.ro
- **☎️ Phone:** 0371 311 311  
- **📖 OAuth Endpoint:** https://openapi.banca-transilvania.ro/oauth/authorize

---

## 3. Unde introduci Tokenurile în Aplicație?

Mergi la: **http://127.0.0.1:9512/finance/banks/create/**

Și completezi formularul cu:
- **Bank:** Selectează banca (Revolut / Banca Transilvania)
- **Account Name:** Numele pe care vrei să-l dai
- **Access Token / Client ID:** Token-ul obținut mai sus

---

## ⚠️ Sfaturi de Siguranță

- ✓ Nu partaja tokenurile cu nimeni
- ✓ Păstrează-le într-un loc sigur
- ✓ Dacă expune un token, regenerează-l din aplicație
- ✓ Tokenurile se salvează criptat în baza de date
