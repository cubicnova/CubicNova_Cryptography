"""
config.py
---------
Central configuration for the Flask application. All secrets are read
from environment variables first, with safe local-development
fallbacks. Never commit real production secrets to source control.
"""

import os
from datetime import timedelta

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass


class Config:
    # ------------------------------------------------------------------
    # Flask / session security
    # ------------------------------------------------------------------
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-only-change-this-secret-key-1234567890")

    # Session ("account") timeout: user is logged out after this many
    # minutes of inactivity.
    PERMANENT_SESSION_LIFETIME = timedelta(minutes=30)
    SESSION_REFRESH_EACH_REQUEST = True  # sliding window: activity resets the clock

    SESSION_COOKIE_HTTPONLY = True    # JS cannot read the cookie -> mitigates XSS cookie theft
    SESSION_COOKIE_SAMESITE = "Lax"   # mitigates CSRF
    SESSION_COOKIE_SECURE = os.environ.get("SESSION_COOKIE_SECURE", "False") == "True"

    # ------------------------------------------------------------------
    # MySQL database connection
    # ------------------------------------------------------------------
    MYSQL_HOST = os.environ.get("MYSQL_HOST", "localhost")
    MYSQL_PORT = int(os.environ.get("MYSQL_PORT", 3306))
    MYSQL_USER = os.environ.get("MYSQL_USER", "pbkdf2_app_user")
    MYSQL_PASSWORD = os.environ.get("MYSQL_PASSWORD", "change-this-password")
    MYSQL_DATABASE = os.environ.get("MYSQL_DATABASE", "password_hashing_db")

    # ------------------------------------------------------------------
    # Account lockout policy
    # ------------------------------------------------------------------
    MAX_FAILED_LOGIN_ATTEMPTS = 5
    LOCKOUT_DURATION_MINUTES = 15

    # ------------------------------------------------------------------
    # PBKDF2 parameters
    # ------------------------------------------------------------------
    # NIST SP 800-132 / OWASP (2023+) recommend >= 600,000 iterations
    # for PBKDF2-HMAC-SHA256. Raise this over time as hardware speeds up.
    PBKDF2_ALGORITHM = "sha256"
    PBKDF2_ITERATIONS = 600_000
    PBKDF2_SALT_BYTES = 16     # 128-bit random salt
    PBKDF2_KEY_LENGTH = 32     # 256-bit derived key
