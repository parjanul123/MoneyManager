-- ============================================================
-- Supabase SQL Script - User Activity Tracking
-- Copy this SQL dans le Supabase SQL Editor et exécute-le
-- ============================================================

-- 1. Create User Activity Table (pentru a urmări ce face utilizatorul)
CREATE TABLE IF NOT EXISTS user_activity (
  id BIGINT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
  user_id INTEGER NOT NULL,
  email VARCHAR(255),
  username VARCHAR(150),
  action VARCHAR(100) NOT NULL, -- 'registered', 'logged_in', 'transaction_created', 'bank_connected', etc.
  timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  details JSONB, -- Additional details like transaction ID, amount, etc.
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 2. Create indices for better performance
CREATE INDEX IF NOT EXISTS idx_user_activity_user_id ON user_activity(user_id);
CREATE INDEX IF NOT EXISTS idx_user_activity_action ON user_activity(action);
CREATE INDEX IF NOT EXISTS idx_user_activity_timestamp ON user_activity(timestamp);

-- 3. Enable RLS (Row Level Security) - optional for security
ALTER TABLE user_activity ENABLE ROW LEVEL SECURITY;

-- 4. Create a public access policy (adjust based on your security needs)
CREATE POLICY "Allow public read access" ON user_activity
  FOR SELECT USING (true);

CREATE POLICY "Allow authenticated insert" ON user_activity
  FOR INSERT WITH CHECK (true);

-- 5. Grant permissions
GRANT ALL ON user_activity TO anon, authenticated;

-- ============================================================
-- Optional: Create Django Users Table (if you want to mirror Django auth)
-- ============================================================

CREATE TABLE IF NOT EXISTS django_users (
  id BIGINT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
  django_user_id INTEGER UNIQUE,
  email VARCHAR(255),
  username VARCHAR(150) UNIQUE,
  first_name VARCHAR(150),
  last_name VARCHAR(150),
  date_joined TIMESTAMP,
  is_active BOOLEAN DEFAULT true,
  discord_id VARCHAR(100),
  discord_username VARCHAR(255),
  avatar_url VARCHAR(500),
  bio TEXT,
  synced_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_django_users_email ON django_users(email);
CREATE INDEX IF NOT EXISTS idx_django_users_username ON django_users(username);

ALTER TABLE django_users ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Allow public read access" ON django_users
  FOR SELECT USING (true);

GRANT ALL ON django_users TO anon, authenticated;

-- ============================================================
-- Test Data (opcional - pentru testare)
-- ============================================================

-- Uncomment the lines below to insert test data

-- INSERT INTO user_activity (user_id, email, username, action, details)
-- VALUES (
--   1,
--   'test@example.com',
--   'testuser',
--   'user_registered',
--   '{"signup_method": "email"}'::jsonb
-- );

-- INSERT INTO django_users (django_user_id, email, username, first_name, is_active)
-- VALUES (
--   1,
--   'test@example.com',
--   'testuser',
--   'Test',
--   true
-- );

-- ============================================================
-- Verification (check if tables were created)
-- ============================================================

-- SELECT 'user_activity' as table_name, COUNT(*) as row_count FROM user_activity
-- UNION ALL
-- SELECT 'django_users' as table_name, COUNT(*) as row_count FROM django_users;
