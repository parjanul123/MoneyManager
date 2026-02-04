# 🔐 Cum Să-Ți Conectezi Conturile Bancare

## 📍 ACESSO ÀS PÁGINAS PRINCIPAIS

### 1. **Dashboard BT Pay** (Datele tale în timp real) ⚡
```
http://localhost:8000/finance/bt-pay/live/
```
👉 AQUI VES TRANSAÇÕES EM TEMPO REAL

### 2. **Portal Bancário - Conectar Contas** 🏦
```
http://localhost:8000/finance/banks/
http://localhost:8000/finance/banks/create/
```
👉 AQUI CONECTAS REVOLUT E BANCA TRANSILVANIA

### 3. **Admin Panel**
```
http://localhost:8000/admin/
```
👉 Para gerenciamento avançado

---

## 🎯 ONDE ENCONTRA CADA COISA NA APLICAÇÃO

```
┌─────────────────────────────────────────────────────────┐
│  🏠 MONEY MANAGER (Navbar - Topo da página)            │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  Dashboard  │  Live  │  [💳 Conectare Cont] (verde)   │
│                      ↑                                 │
│                      └─ CLICA AQUI PARA CONECTAR      │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

---

## 🚀 PASSO A PASSO - COMO CONECTAR CONTAS

### ✅ PASSO 1: Abre Dashboard BT Pay
1. Vai a: **http://localhost:8000/finance/bt-pay/live/**
2. Vê um banner azul explicando os passos
3. Clica no botão verde **"💳 Conectare Cont"** (canto superior direito)

### ✅ PASSO 2: Escolhe o Banco

**Opção A: REVOLUT**
1. Vai a: http://localhost:8000/finance/banks/create/
2. Seleciona: **Bank: Revolut**
3. Vai em Revolut App → Settings → Integrations/API → Creia Token
4. Copia o token (e-mail_code_xxx...)
5. Cola o token na aplicação
6. Click: **Conectează** ✅

**Opção B: BANCA TRANSILVANIA (BT)**
1. Vai a: http://localhost:8000/finance/banks/create/
2. Seleciona: **Bank: Banca Transilvania**
3. Click: **"Autorizare BT"** (aparece um botão)
4. Eres levado para login.bt.ro
5. Faça login com suas credenciais BT
6. Autoriza acesso: "Permites que Money Manager vea tus cuentas?"
7. Click: **"Aprob"** / **"Authorize"** ✅
8. Eres levado de volta à aplicação
9. Conexão completa! ✅

### ✅ PASSO 3: Sincroniza Transações
1. Volta a: http://localhost:8000/finance/banks/
2. Vê seus bancos conectados
3. Click no botão **"Sincronizează"**
4. Espera 10-30 segundos
5. Transações baixadas ✅

### ✅ PASSO 4: Ve Dashboard
1. Volta a: http://localhost:8000/finance/bt-pay/live/
2. Vê:
   - ⏳ Transações Pending (à espera de categorização)
   - ✅ Transações sincronizadas
   - 📊 Estatísticas ao vivo
   - 🏪 Top comerciantes
   - 📈 Gráfico de 24 horas

---

## 🗂️ ESTRUTURA DE NAVEGAÇÃO

```
Money Manager (Home)
    │
    ├─ 📊 Dashboard (geral)
    │
    ├─ ⚡ Live (BT Pay - AQUI VES DADOS EM TEMPO REAL)
    │
    ├─ 🏦 Conectare Cont (BOTÃO VERDE - conecta bancos)
    │     └─ Revolut
    │     └─ Banca Transilvania
    │
    └─ User Menu (Profil, Deconectar)
```

---

## 📍 URLS RÁPIDAS - COPIE E COLE

| O Que Fazer | URL | Botão |
|------------|-----|--------|
| **Ver Dashboard ao vivo** | /finance/bt-pay/live/ | Botão "Live" no navbar |
| **Conectar banco** | /finance/banks/create/ | Botão "💳 Conectare Cont" (verde) |
| **Ver bancos conectados** | /finance/banks/ | Direto no navbar ou dashboard |
| **Sincronizar dados** | /finance/banks/sync/ | Após conectar banco |
| **Categorizar transações** | /finance/banks/transactions/pending/ | Link na página de sync |

---

## 🔑 TOKEN REVOLUT - COMO OBTER

1. **Abre Revolut App** no telefone
2. **Settings** (engrenagem) → **Integrations** / **API**
3. **Criar Token** / **Create API Token**
4. Dá um nome: ex. "MoneyManager"
5. **Copia o token** (aparece uma vez só!)
6. **Cola na aplicação** em /finance/banks/create/

Formato: `revolut_xxxx_yyyy_zzzz` (código longo)

---

## 🔐 OAUTH2 BANCA TRANSILVANIA - COMO FUNCIONA

1. **Clica "Autorizare BT"** na aplicação
   ↓
2. **Eres levado** para login.banca-transilvania.ro
   ↓
3. **Faça login** com suas credenciais BT
   ↓
4. **BT pergunta**: "Permites que Money Manager acesse tuas contas?"
   ↓
5. **Click "Aprob"**
   ↓
6. **Eres retornado** à aplicação
   ↓
7. ✅ **Conexão segura estabelecida**

**O que significa?**
- Nós NÃO vemos sua senha
- BT guarda a autorização
- Renovação automática
- Totalmente seguro

---

## ⚡ FLUXO RÁPIDO (5 MINUTOS)

```
1. Abre: http://localhost:8000/finance/bt-pay/live/
   ↓
2. Vê banner azul com instruções
   ↓
3. Click botão verde "💳 Conectare Cont"
   ↓
4. Escolhe Revolut ou BT
   ↓
5. Completa autenticação (Revolut = token, BT = OAuth2)
   ↓
6. Volta ao banco e clica "Sincronizează"
   ↓
7. Espera 30 segundos
   ↓
8. ✅ Dashboard mostra transações em tempo real!
```

---

## ❓ DÚVIDAS FREQUENTES

**P: Onde exatamente clico para conectar?**
A: Botão verde "💳 Conectare Cont" - canto superior direito de qualquer página

**P: Por que não vejo transações?**
A: Porque ainda não tem bancos conectados. Clica "💳 Conectare Cont"

**P: Como sincronizo?**
A: Após conectar banco, vai a /finance/banks/ e clica "Sincronizează"

**P: O que é Pending?**
A: Transações à espera de categorização (você escolhe o tipo de gasto)

**P: Quanta informação veem sobre minha senha?**
A: Nenhuma! OAuth2 = você loga no banco, não em nossa aplicação

**P: Posso conectar múltiplos bancos?**
A: SIM! Clica "Conectare Cont" novamente

---

## 🎯 RESUMO VISUAL

```
APLICAÇÃO MONEY MANAGER
    │
    ├─ NAVBAR (Topo)
    │   └─ [💳 Conectare Cont] ← CLICA AQUI
    │
    ├─ DASHBOARD /finance/bt-pay/live/
    │   ├─ Instrções claras (banner azul)
    │   ├─ Botão "Conectare Cont"
    │   ├─ Transações Pending ⏳
    │   ├─ Transações Sincronizadas ✅
    │   └─ Gráficos e estatísticas 📊
    │
    └─ PORTAL BANCÁRIO /finance/banks/
        ├─ Lista de bancos conectados
        ├─ Botão para conectar novo
        └─ Botão para sincronizar
```

---

**🚀 Começa agora: http://localhost:8000/finance/bt-pay/live/** 

Vê as instruções e segue os passos. Leva menos de 5 minutos!

---

### PASUL 2: Conectează REVOLUT

#### A. Obține Personal Token (din Revolut)

1. Deschide **Revolut App**
2. Settings → Integrations / API
3. Crează **New Token** (Personal Token)
4. Copie token-ul (lungă codificare)

#### B. Adaugă în Aplicație

1. Mergi la: http://localhost:8000/finance/banks/create/
2. Selectează: **Bank: Revolut**
3. Introduceți: **Token (din Revolut)**
4. Click: **Conectează**

✅ Sistem verifică automat tokenul cu API Revolut

---

### PASUL 3: Conectează BANCA TRANSILVANIA (BT)

#### A. Autentificare OAuth2

1. Mergi la: http://localhost:8000/finance/banks/create/
2. Selectează: **Bank: Banca Transilvania**
3. Click: **"Autorizare BT"**
4. Se deschide pagina BT
5. Loghează-te cu credențialele BT

#### B. Autorizează Accesul

1. BT cere permisiune pentru: "Citire conturi și tranzacții"
2. Click: **"Aprob" / "Authorize"**
3. Ești redirecționat înapoi
4. Conexiune établită ✅

---

## 📊 FLUX DE DATE

```
┌──────────────────────┐
│  Revolut App         │
│  (Personal Token)    │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────────────────────┐
│  Aplicația Money Manager             │
│  http://localhost:8000/finance/banks/│
└──────────┬───────────────────────────┘
           │
           │ 1. Conectare cont
           │ 2. Sincronizare tranzacții
           │ 3. Auto-categorizare
           │
           ▼
┌──────────────────────┐
│  Database SQLite     │
│  - Tranzacții       │
│  - Balanță          │
│  - Categorii        │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────────────────┐
│  Dashboard Timp Real             │
│  http://localhost:8000/finance/  │
│  - Pending tranzacții            │
│  - Statistici zilnice            │
│  - Top comercianți               │
└──────────────────────────────────┘
```

---

## 🎯 LOCURI DE ACCES

### Pentru Conectare
| Acțiune | URL |
|---------|-----|
| **Conectează cont** | http://localhost:8000/finance/banks/create/ |
| **Vezi conturi conectate** | http://localhost:8000/finance/banks/ |
| **Sincronizează tranzacții** | http://localhost:8000/finance/banks/sync/ |

### Pentru Gestionare Tranzacții
| Acțiune | URL |
|---------|-----|
| **Tranzacții în așteptare** | http://localhost:8000/finance/banks/transactions/pending/ |
| **BT Pay Dashboard** | http://localhost:8000/finance/bt-pay/live/ |
| **Auto-categorizare** | http://localhost:8000/finance/banks/transactions/pending/ |

### Pentru Vizualizare Statistici
| Acțiune | URL |
|---------|-----|
| **Statistici BT Pay** | http://localhost:8000/finance/bt-pay/live/ |
| **Rapoarte financiare** | http://localhost:8000/finance/reports/ |
| **Conturi bancare** | http://localhost:8000/finance/accounts/ |

---

## ⚡ RAPID START (5 minute)

### 1. Start Server
```bash
python manage.py runserver
```

### 2. Conectează REVOLUT
```
1. http://localhost:8000/finance/banks/create/
2. Bank: Revolut
3. Token: (din Revolut App Settings → API)
4. Click: Conectează ✅
```

### 3. Conectează BT
```
1. http://localhost:8000/finance/banks/create/
2. Bank: Banca Transilvania
3. Click: Autorizare (OAuth2)
4. Loghează-te + Aprob ✅
```

### 4. Sincronizează Tranzacții
```
1. http://localhost:8000/finance/banks/sync/
2. Click: Sincronizează acum
3. Așteptă 10-30 secunde
4. Tranzacții descărcate ✅
```

### 5. Categorizează
```
1. http://localhost:8000/finance/banks/transactions/pending/
2. Pentru fiecare: Selectează categorie + Accept
3. Sau: Auto-Categorize (pentru BT Pay)
4. Gata ✅
```

### 6. Vezi Dashboard
```
1. http://localhost:8000/finance/bt-pay/live/
2. Statistici live
3. Grafice
4. Cheltuieli zilnice ✅
```

---

## 🔑 TOKEN REVOLUT - Cum Se Obține

### Pe Telefon (Revolut App)
```
1. Deschide Revolut
2. Merge la: Settings (⚙️)
3. Appareaza: Integrations / API
4. Click: "Create API Token" / "Personal Token"
5. Dă nume: Ex. "MoneyManager"
6. Copiază token-ul
7. Salvează undeva (se vede o singură dată!)
```

### De așteptat
- Token are format: `xxxxx_yyy_zzzzzzzzzzzz...` (lungă codificare)
- Include prefix `revolut_` sau similar
- Stochare securizată: criptat în bază de date

---

## 🔐 OAUTH2 BANCA TRANSILVANIA - Cum Funcționează

### Proces Automat
```
1. Click "Autorizare BT" în aplicație
   ↓
2. Ești trimis la login.banca-transilvania.ro
   ↓
3. Introduceți credențiale BT (nume utilizator + parolă)
   ↓
4. BT cere permisiuni:
   - ✓ Citi conturi și balanțe
   - ✓ Citi istoricul tranzacțiilor
   ↓
5. Click "Aprob"
   ↓
6. Ești returnat la Money Manager
   ↓
7. Conexiune sigură stabilită ✅
   
8. Acces token salvat criptat
9. Refresh token pentru refresh automat
```

### Ce Înseamnă
- **OAuth2 = Conexiune sigură**
- Noi NU vedem parola ta BT
- BT te intreabă: "Permiti Money Manager să acceseze conturile?"
- Tu aprovi → conexiune securizată

---

## 🔄 FLUX COMPLET DE SINCRONIZARE

```
1. USER: Click "Sincronizează"
   ↓
2. SERVER: Citește token salvat
   ↓
3. API REVOLUT/BT: 
   - Se conectează cu token
   - Descarcă últimele tranzacții
   - Returează în format JSON
   ↓
4. APLICAȚIE:
   - Parsează răspunsul
   - Verifică duplicare (external_id)
   - Salvează în bază de date
   ↓
5. BT PAY DETECTION:
   - Detectează "BT Pay" tranzacții
   - Auto-categorizare
   - Crează Transaction record
   ↓
6. DASHBOARD:
   - Afișează "Pending" tranzacții
   - Statistici actualizate
   - Grafice live ✅
```

---

## 📱 API ENDPOINTS (Pentru Devs)

Dacă dorești datele direct în format JSON:

```bash
# Tranzacții recente
curl http://localhost:8000/finance/api/bt-pay/transactions/

# Statistici
curl http://localhost:8000/finance/api/bt-pay/stats/

# Pending
curl http://localhost:8000/finance/api/bt-pay/pending/

# Dashboard complet
curl http://localhost:8000/finance/api/bt-pay/dashboard/
```

---

## ✅ VERIF: Tot E Conectat?

Mergi la: **http://localhost:8000/finance/banks/**

Ar trebui să vezi:
```
┌─────────────────────────────────────┐
│ Connected Bank Accounts             │
├─────────────────────────────────────┤
│                                     │
│ ✅ Revolut                          │
│    Account: Main                    │
│    Balance: 5,250.75 RON            │
│    Last sync: 5 minutes ago         │
│                                     │
│ ✅ Banca Transilvania                │
│    Account: Curent                  │
│    Balance: 12,450.00 RON           │
│    Last sync: 3 minutes ago         │
│                                     │
├─────────────────────────────────────┤
│ [+ Add New Account]                 │
└─────────────────────────────────────┘
```

---

## 🎯 SUMMAR - URL-URI DE MEMORAT

| Scop | URL |
|------|-----|
| **Conectare conturi** | /finance/banks/create/ |
| **Sincronizare** | /finance/banks/sync/ |
| **Tranzacții pending** | /finance/banks/transactions/pending/ |
| **Dashboard live** | /finance/bt-pay/live/ |
| **API JSON** | /api/bt-pay/dashboard/ |

---

## ❓ FAQ

**Q: Unde vad balanța?**
A: /finance/banks/ - afișează balanța din fiecare cont

**Q: Cum șterg o conexiune?**
A: /finance/banks/ → Click cont → Delete

**Q: Pot conecta mai mult de 2 conturi?**
A: DA! Mergi la /finance/banks/create/ și adaugă altele

**Q: Ce se întâmplă cu parolele?**
A: Noi NU stocam parole. Doar tokens OAuth2 criptate

**Q: Cât durează sincronizarea?**
A: 10-30 secunde per cont, depinde de API

**Q: Pot sincroniza manual?**
A: DA! /finance/banks/sync/ - oricând vrei

---

**Acum mergi la: http://localhost:8000/finance/banks/ și conectează-ți conturile!** 🚀
