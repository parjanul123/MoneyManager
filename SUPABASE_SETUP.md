# Configurare Supabase pentru MoneyManager

## 1. Creează .env File

Copiază `.env.example` în `.env` și actualizează cu credențialele Supabase:

```bash
copy .env.example .env
```

## 2. Obține Credențialele Supabase

### Din Supabase Dashboard:

1. Mergi pe [supabase.com](https://supabase.com)
2. Selectează proiectul `shwbounuzknxjvvebyym`
3. Mergi la **Settings → Database → Connection string**
4. Selectează **URI** format

URL-ul va arăta așa:
```
postgresql://postgres:[PASSWORD]@db.shwbounuzknxjvvebyym.supabase.co:5432/postgres
```

### Completează .env cu:
```env
SUPABASE_DB_ENABLED=True
SUPABASE_DB_HOST=db.shwbounuzknxjvvebyym.supabase.co
SUPABASE_DB_PORT=5432
SUPABASE_DB_NAME=postgres
SUPABASE_DB_USER=postgres
SUPABASE_DB_PASSWORD=[PASSWORD_DIN_CONNECTION_STRING]
```

## 3. Instalează Dependențe

```bash
pip install -r requirements.txt
```

## 4. Migrează Baza de Date

```bash
py manage.py migrate
```

## 5. Creeaza Super User (Admin)

```bash
py manage.py createsuperuser
```

## 6. Rulează Serverul

```bash
py manage.py runserver
```

---

## SQL INSTRUCTIONS PENTRU SUPABASE SQL EDITOR

Execută aceste comenzi în **Supabase → SQL Editor** pentru configurare avansată:

### A. Activează Row Level Security (RLS)

```sql
-- Activează extensii necesare
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- Creează tabel pentru audit
CREATE TABLE IF NOT EXISTS public.audit_log (
    id BIGSERIAL PRIMARY KEY,
    user_id UUID REFERENCES auth.users(id),
    table_name TEXT,
    operation TEXT,
    old_data JSONB,
    new_data JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Activează RLS pe audit_log
ALTER TABLE public.audit_log ENABLE ROW LEVEL SECURITY;
```

### B. Configurează Auth Policy

```sql
-- Politică: userii vad doar datele lor
CREATE POLICY "Users can view own data" ON public.finance_account
    FOR SELECT USING (
        auth.uid()::text = user_id::text
    );

-- Politică: userii pot insera doar pentru ei
CREATE POLICY "Users can insert own accounts" ON public.finance_account
    FOR INSERT WITH CHECK (
        auth.uid()::text = user_id::text
    );
```

### C. Creează Triggers pentru Audit

```sql
-- Trigger pentru audit_log
CREATE OR REPLACE FUNCTION public.audit_trigger()
RETURNS TRIGGER AS $$
BEGIN
    INSERT INTO public.audit_log (user_id, table_name, operation, old_data, new_data)
    VALUES (
        auth.uid(),
        TG_TABLE_NAME,
        TG_OP,
        CASE WHEN TG_OP = 'DELETE' THEN row_to_json(OLD) ELSE NULL END,
        CASE WHEN TG_OP IN ('INSERT', 'UPDATE') THEN row_to_json(NEW) ELSE NULL END
    );
    RETURN COALESCE(NEW, OLD);
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;
```

### D. Optimizează Performance

```sql
-- Indexuri pentru căutări rapide
CREATE INDEX IF NOT EXISTS idx_finance_account_user_id 
    ON public.finance_account(user_id);

CREATE INDEX IF NOT EXISTS idx_finance_transaction_account_id 
    ON public.finance_transaction(account_id);

CREATE INDEX IF NOT EXISTS idx_finance_transaction_date 
    ON public.finance_transaction(date);

-- Statistici vakuum
VACUUM ANALYZE;
```

### E. Configurare Backup

```sql
-- Checks și constraints automatice
ALTER TABLE public.finance_account 
ADD CONSTRAINT check_balance_not_negative 
CHECK (balance >= 0);

ALTER TABLE public.finance_transaction
ADD CONSTRAINT check_amount_positive
CHECK (amount > 0);
```

---

## Verificare Conexiune

După setup, rulează în terminal:

```bash
py manage.py dbshell
```

Dacă se conectează la Supabase (nu la SQLite), e totul ok!

---

## Troubleshooting

### Eroare: "psycopg2 module not found"
```bash
pip install psycopg2-binary
```

### Eroare: "ssl certificate problem"
Supabase necesită SSL. Dacă ai probleme, adaugă în `.env`:
```env
# Doar pentru testing (NOT recommended for production)
SUPABASE_DB_OPTIONS=sslmode disabled
```

### Eroare: "password authentication failed"
- Verifică că `.env` are parola corectă
- Reseteaza parola în Supabase Dashboard → Settings → Database → Reset password

---

## Documentație

- [Supabase Docs](https://supabase.com/docs)
- [Django PostgreSQL Backend](https://docs.djangoproject.com/en/6.0/ref/databases/#postgresql-notes)
- [Psycopg2 Docs](https://www.psycopg.org/)
