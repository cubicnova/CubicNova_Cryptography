-- =====================================================================
-- schema.sql
-- MySQL database setup for the PBKDF2 Password Hashing Auth System
-- =====================================================================

CREATE DATABASE IF NOT EXISTS password_hashing_db
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;

USE password_hashing_db;

-- Dedicated, least-privilege application user. Never connect to MySQL
-- as 'root' from application code. Replace the password below with a
-- strong one and keep it in sync with MYSQL_PASSWORD in your .env.
CREATE USER IF NOT EXISTS 'pbkdf2_app_user'@'localhost'
    IDENTIFIED BY 'change-this-password';

GRANT SELECT, INSERT, UPDATE, DELETE ON password_hashing_db.* TO 'pbkdf2_app_user'@'localhost';
FLUSH PRIVILEGES;

-- Users table.
--   password_hash : hex-encoded PBKDF2-HMAC-SHA256 derived key (64 hex
--                    chars for a 32-byte key)
--   salt          : hex-encoded random salt used to derive password_hash
--                    (32 hex chars for a 16-byte salt)
-- Hash and salt are stored in SEPARATE columns here (unlike bcrypt,
-- PBKDF2's output does not embed the salt/parameters, so we must keep
-- them ourselves to be able to recompute the hash at login time).
CREATE TABLE IF NOT EXISTS users (
    id              INT AUTO_INCREMENT PRIMARY KEY,
    username        VARCHAR(50)  NOT NULL UNIQUE,
    email           VARCHAR(100) NOT NULL UNIQUE,
    password_hash   VARCHAR(255) NOT NULL,   -- hex-encoded derived key
    salt            VARCHAR(255) NOT NULL,   -- hex-encoded random salt
    failed_attempts INT          NOT NULL DEFAULT 0,
    locked_until    DATETIME     NULL,
    last_login      DATETIME     NULL,
    created_at      TIMESTAMP    NOT NULL DEFAULT CURRENT_TIMESTAMP,

    INDEX idx_username (username),
    INDEX idx_email (email)
) ENGINE=InnoDB;

-- =====================================================================
-- Notes:
-- * We never store plaintext passwords -- only the PBKDF2 derived key
--   (password_hash) and the random salt used to produce it.
-- * We do NOT store the iteration count per-row in this schema; the
--   iteration count is fixed in config.py (PBKDF2_ITERATIONS). If you
--   later raise the iteration count, either re-hash every user's
--   password on their next successful login, or add an `iterations`
--   column so each row can record the count it was hashed with.
-- * All queries in app.py use parameterized placeholders (%s), which
--   prevents SQL injection regardless of user input.
-- =====================================================================
