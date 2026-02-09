-- ========================================
-- MONEY MANAGER - Supabase SQL Setup
-- ========================================

-- 1. Creează tabel pentru conturi (Accounts)
CREATE TABLE IF NOT EXISTS finance_account (
    id BIGSERIAL PRIMARY KEY,
    user_id UUID NOT NULL REFERENCES auth.users(id),
    name VARCHAR(255) NOT NULL,
    type VARCHAR(50) NOT NULL,
    balance NUMERIC(10, 2) NOT NULL DEFAULT 0,
    currency VARCHAR(10) NOT NULL DEFAULT 'RON',
    bank_name VARCHAR(255),
    account_number VARCHAR(255),
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE(user_id, account_number)
);

-- 2. Creează tabel pentru categorii
CREATE TABLE IF NOT EXISTS finance_category (
    id BIGSERIAL PRIMARY KEY,
    user_id UUID REFERENCES auth.users(id),
    name VARCHAR(255) NOT NULL,
    color VARCHAR(7) NOT NULL DEFAULT '#0D6EFD',
    icon VARCHAR(50),
    is_default BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 3. Creează tabel pentru tranzacții
CREATE TABLE IF NOT EXISTS finance_transaction (
    id BIGSERIAL PRIMARY KEY,
    user_id UUID NOT NULL REFERENCES auth.users(id),
    account_id BIGINT NOT NULL REFERENCES finance_account(id) ON DELETE CASCADE,
    category_id BIGINT REFERENCES finance_category(id),
    type VARCHAR(50) NOT NULL, -- 'income', 'expense'
    amount NUMERIC(10, 2) NOT NULL,
    description TEXT,
    date DATE NOT NULL DEFAULT CURRENT_DATE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    is_recurring BOOLEAN NOT NULL DEFAULT FALSE,
    merchant_name VARCHAR(255)
);

-- 4. Creează tabel pentru bugete
CREATE TABLE IF NOT EXISTS finance_budget (
    id BIGSERIAL PRIMARY KEY,
    user_id UUID NOT NULL REFERENCES auth.users(id),
    category_id BIGINT REFERENCES finance_category(id),
    month DATE NOT NULL,
    limit_amount NUMERIC(10, 2) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 5. Creează tabel pentru economii (Savings)
CREATE TABLE IF NOT EXISTS finance_savings (
    id BIGSERIAL PRIMARY KEY,
    user_id UUID NOT NULL REFERENCES auth.users(id),
    account_id BIGINT NOT NULL REFERENCES finance_account(id) ON DELETE CASCADE,
    goal_name VARCHAR(255) NOT NULL,
    target_amount NUMERIC(10, 2) NOT NULL,
    current_amount NUMERIC(10, 2) NOT NULL DEFAULT 0,
    target_date DATE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 6. Creează tabel pentru conexiuni bancii (Bank Integration)
CREATE TABLE IF NOT EXISTS finance_bankconnection (
    id BIGSERIAL PRIMARY KEY,
    user_id UUID NOT NULL REFERENCES auth.users(id),
    bank_name VARCHAR(255) NOT NULL,
    account_id VARCHAR(255),
    access_token VARCHAR(500),
    refresh_token VARCHAR(500),
    is_connected BOOLEAN NOT NULL DEFAULT FALSE,
    last_sync TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 7. Creează tabel pentru tranzacții bancare sync
CREATE TABLE IF NOT EXISTS finance_banktransaction (
    id BIGSERIAL PRIMARY KEY,
    user_id UUID NOT NULL REFERENCES auth.users(id),
    bank_connection_id BIGINT REFERENCES finance_bankconnection(id),
    account_id BIGINT REFERENCES finance_account(id),
    bank_transaction_id VARCHAR(255) NOT NULL,
    amount NUMERIC(10, 2) NOT NULL,
    description TEXT,
    date DATE NOT NULL,
    merchant_name VARCHAR(255),
    status VARCHAR(50) NOT NULL DEFAULT 'pending', -- pending, accepted, ignored
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE(user_id, bank_transaction_id)
);

-- 8. Creează tabel pentru User Profile (Discord și alte date)
CREATE TABLE IF NOT EXISTS finance_userprofile (
    id BIGSERIAL PRIMARY KEY,
    user_id UUID NOT NULL UNIQUE REFERENCES auth.users(id) ON DELETE CASCADE,
    avatar_url TEXT,
    bio TEXT,
    preferred_currency VARCHAR(10) NOT NULL DEFAULT 'RON',
    notifications_enabled BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- ========================================
-- INDEXES (Pentru performanță)
-- ========================================

CREATE INDEX idx_finance_account_user_id ON finance_account(user_id);
CREATE INDEX idx_finance_transaction_user_id ON finance_transaction(user_id);
CREATE INDEX idx_finance_transaction_account_id ON finance_transaction(account_id);
CREATE INDEX idx_finance_transaction_date ON finance_transaction(date);
CREATE INDEX idx_finance_transaction_category_id ON finance_transaction(category_id);
CREATE INDEX idx_finance_budget_user_id ON finance_budget(user_id);
CREATE INDEX idx_finance_savings_user_id ON finance_savings(user_id);
CREATE INDEX idx_finance_bankconnection_user_id ON finance_bankconnection(user_id);
CREATE INDEX idx_finance_banktransaction_user_id ON finance_banktransaction(user_id);

-- ========================================
-- ROW LEVEL SECURITY (RLS) - Optional
-- ========================================

-- Activează RLS pe tabele
ALTER TABLE finance_account ENABLE ROW LEVEL SECURITY;
ALTER TABLE finance_transaction ENABLE ROW LEVEL SECURITY;
ALTER TABLE finance_category ENABLE ROW LEVEL SECURITY;
ALTER TABLE finance_budget ENABLE ROW LEVEL SECURITY;
ALTER TABLE finance_savings ENABLE ROW LEVEL SECURITY;
ALTER TABLE finance_bankconnection ENABLE ROW LEVEL SECURITY;
ALTER TABLE finance_banktransaction ENABLE ROW LEVEL SECURITY;
ALTER TABLE finance_userprofile ENABLE ROW LEVEL SECURITY;

-- Politici RLS: Userii pot vedea doar datele lor
CREATE POLICY "Users can view own accounts" ON finance_account
    FOR SELECT USING (user_id = auth.uid());

CREATE POLICY "Users can view own transactions" ON finance_transaction
    FOR SELECT USING (user_id = auth.uid());

CREATE POLICY "Users can view own categories" ON finance_category
    FOR SELECT USING (user_id = auth.uid() OR is_default = TRUE);

CREATE POLICY "Users can view own budgets" ON finance_budget
    FOR SELECT USING (user_id = auth.uid());

CREATE POLICY "Users can view own savings" ON finance_savings
    FOR SELECT USING (user_id = auth.uid());

-- Politici INSERT: Userii pot insera doar datele lor
CREATE POLICY "Users can insert own accounts" ON finance_account
    FOR INSERT WITH CHECK (user_id = auth.uid());

CREATE POLICY "Users can insert own transactions" ON finance_transaction
    FOR INSERT WITH CHECK (user_id = auth.uid());

CREATE POLICY "Users can insert own categories" ON finance_category
    FOR INSERT WITH CHECK (user_id = auth.uid());

CREATE POLICY "Users can insert own budgets" ON finance_budget
    FOR INSERT WITH CHECK (user_id = auth.uid());

CREATE POLICY "Users can insert own savings" ON finance_savings
    FOR INSERT WITH CHECK (user_id = auth.uid());

CREATE POLICY "Users can insert own bank connections" ON finance_bankconnection
    FOR INSERT WITH CHECK (user_id = auth.uid());

CREATE POLICY "Users can insert own bank transactions" ON finance_banktransaction
    FOR INSERT WITH CHECK (user_id = auth.uid());

-- Politici UPDATE: Userii pot actualiza doar datele lor
CREATE POLICY "Users can update own accounts" ON finance_account
    FOR UPDATE USING (user_id = auth.uid());

CREATE POLICY "Users can update own transactions" ON finance_transaction
    FOR UPDATE USING (user_id = auth.uid());

CREATE POLICY "Users can update own categories" ON finance_category
    FOR UPDATE USING (user_id = auth.uid());

CREATE POLICY "Users can update own budgets" ON finance_budget
    FOR UPDATE USING (user_id = auth.uid());

CREATE POLICY "Users can update own savings" ON finance_savings
    FOR UPDATE USING (user_id = auth.uid());

-- Politici DELETE: Userii pot sterge doar datele lor
CREATE POLICY "Users can delete own accounts" ON finance_account
    FOR DELETE USING (user_id = auth.uid());

CREATE POLICY "Users can delete own transactions" ON finance_transaction
    FOR DELETE USING (user_id = auth.uid());

CREATE POLICY "Users can delete own categories" ON finance_category
    FOR DELETE USING (user_id = auth.uid());

CREATE POLICY "Users can delete own budgets" ON finance_budget
    FOR DELETE USING (user_id = auth.uid());

CREATE POLICY "Users can delete own savings" ON finance_savings
    FOR DELETE USING (user_id = auth.uid());

-- ========================================
-- TRIGGERS - Set user_id automatically
-- ========================================

-- Trigger pentru finance_account
CREATE OR REPLACE FUNCTION set_user_id_account()
RETURNS TRIGGER AS $$
BEGIN
    IF NEW.user_id IS NULL THEN
        NEW.user_id = auth.uid();
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

CREATE TRIGGER trigger_set_user_id_account
BEFORE INSERT ON finance_account
FOR EACH ROW
EXECUTE FUNCTION set_user_id_account();

-- Trigger pentru finance_transaction
CREATE OR REPLACE FUNCTION set_user_id_transaction()
RETURNS TRIGGER AS $$
BEGIN
    IF NEW.user_id IS NULL THEN
        NEW.user_id = auth.uid();
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

CREATE TRIGGER trigger_set_user_id_transaction
BEFORE INSERT ON finance_transaction
FOR EACH ROW
EXECUTE FUNCTION set_user_id_transaction();

-- Trigger pentru finance_category
CREATE OR REPLACE FUNCTION set_user_id_category()
RETURNS TRIGGER AS $$
BEGIN
    IF NEW.user_id IS NULL THEN
        NEW.user_id = auth.uid();
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

CREATE TRIGGER trigger_set_user_id_category
BEFORE INSERT ON finance_category
FOR EACH ROW
EXECUTE FUNCTION set_user_id_category();

-- Trigger pentru finance_budget
CREATE OR REPLACE FUNCTION set_user_id_budget()
RETURNS TRIGGER AS $$
BEGIN
    IF NEW.user_id IS NULL THEN
        NEW.user_id = auth.uid();
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

CREATE TRIGGER trigger_set_user_id_budget
BEFORE INSERT ON finance_budget
FOR EACH ROW
EXECUTE FUNCTION set_user_id_budget();

-- Trigger pentru finance_savings
CREATE OR REPLACE FUNCTION set_user_id_savings()
RETURNS TRIGGER AS $$
BEGIN
    IF NEW.user_id IS NULL THEN
        NEW.user_id = auth.uid();
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

CREATE TRIGGER trigger_set_user_id_savings
BEFORE INSERT ON finance_savings
FOR EACH ROW
EXECUTE FUNCTION set_user_id_savings();

-- Trigger pentru finance_bankconnection
CREATE OR REPLACE FUNCTION set_user_id_bankconnection()
RETURNS TRIGGER AS $$
BEGIN
    IF NEW.user_id IS NULL THEN
        NEW.user_id = auth.uid();
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

CREATE TRIGGER trigger_set_user_id_bankconnection
BEFORE INSERT ON finance_bankconnection
FOR EACH ROW
EXECUTE FUNCTION set_user_id_bankconnection();

-- Trigger pentru finance_banktransaction
CREATE OR REPLACE FUNCTION set_user_id_banktransaction()
RETURNS TRIGGER AS $$
BEGIN
    IF NEW.user_id IS NULL THEN
        NEW.user_id = auth.uid();
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

CREATE TRIGGER trigger_set_user_id_banktransaction
BEFORE INSERT ON finance_banktransaction
FOR EACH ROW
EXECUTE FUNCTION set_user_id_banktransaction();

-- ========================================
-- SAMPLE DATA (Optional)
-- ========================================

-- Inserează categorii default
INSERT INTO finance_category (user_id, name, color, is_default) VALUES
(NULL, 'Groceries', '#FF6B6B', TRUE),
(NULL, 'Transport', '#4ECDC4', TRUE),
(NULL, 'Entertainment', '#FFE66D', TRUE),
(NULL, 'Utilities', '#95E1D3', TRUE),
(NULL, 'Healthcare', '#F38181', TRUE),
(NULL, 'Salary', '#2ECC71', TRUE),
(NULL, 'Freelance', '#3498DB', TRUE),
(NULL, 'Returns', '#9B59B6', TRUE);
