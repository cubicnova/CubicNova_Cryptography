-- =====================================================================
-- schema.sql
-- MySQL database setup for the Password Hashing Authentication System
-- =====================================================================

-- 1. Create the database
CREATE DATABASE IF NOT EXISTS auth_system
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;

USE auth_system;

-- 2. Create a dedicated, least-privilege application user.
--    (Never use the MySQL 'root' account from your application code.)
--    Replace 'change-this-password' with a strong password and keep it
--    in sync with MYSQL_PASSWORD in your environment / config.py.
CREATE USER IF NOT EXISTS 'auth_app_user'@'localhost'
    IDENTIFIED BY 'change-this-password';

GRANT SELECT, INSERT, UPDATE, DELETE ON auth_system.* TO 'auth_app_user'@'localhost';
FLUSH PRIVILEGES;

-- 3. Users table
--    - password_hash stores the bcrypt hash ONLY. Plaintext passwords
--      are never written to disk anywhere in this system.
--    - failed_attempts / locked_until implement account lockout after
--      repeated bad login attempts.
--    - last_login is shown on the dashboard.
CREATE TABLE IF NOT EXISTS users (
    id              INT AUTO_INCREMENT PRIMARY KEY,
    username        VARCHAR(50)  NOT NULL UNIQUE,
    email           VARCHAR(100) NOT NULL UNIQUE,
    password_hash   VARCHAR(255) NOT NULL,        -- bcrypt hashes are ~60 chars; 255 gives headroom
    failed_attempts INT          NOT NULL DEFAULT 0,
    locked_until    DATETIME     NULL,
    last_login      DATETIME     NULL,
    created_at      TIMESTAMP    NOT NULL DEFAULT CURRENT_TIMESTAMP,

    -- Indexes speed up the lookups the app performs on every
    -- login/register request (WHERE username = ? / WHERE email = ?).
    INDEX idx_username (username),
    INDEX idx_email (email)
) ENGINE=InnoDB;

-- =====================================================================
-- Notes:
-- * We never store plaintext passwords, "hint" answers derived from
--   passwords, or reversible-encrypted passwords -- only one-way
--   bcrypt hashes (see app.py for the hashing workflow).
-- * All queries against this table in app.py use parameterized
--   placeholders (%s) via mysql-connector-python, which prevents
--   SQL injection regardless of what a user types into a form field.
-- =====================================================================
