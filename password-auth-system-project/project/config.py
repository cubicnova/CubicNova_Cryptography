"""
config.py
---------
Central configuration for the Flask application.

All secrets here are read from environment variables first, with safe
local-development fallbacks. In a real production deployment you should
NEVER commit real secrets to source control -- use a .env file (loaded
via python-dotenv) or your platform's secret manager instead.
"""

import os
from datetime import timedelta

# Load a .env file if present (does nothing if python-dotenv isn't used /
# no .env file exists -- safe to keep in all environments).
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass


class Config:
    # ------------------------------------------------------------------
    # Flask / session security
    # ------------------------------------------------------------------
    # SECRET_KEY signs the session cookie and CSRF tokens. Must be long,
    # random, and kept secret in production (set via environment variable).
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-only-change-this-secret-key-1234567890")

    # Sessions expire after this period of inactivity ("session timeout").
    PERMANENT_SESSION_LIFETIME = timedelta(minutes=30)

    # Refresh the cookie's expiry on every request -> sliding-window timeout
    # (any activity resets the 30-minute clock).
    SESSION_REFRESH_EACH_REQUEST = True

    # Cookie hardening:
    SESSION_COOKIE_HTTPONLY = True     # JS (document.cookie) cannot read it -> mitigates XSS cookie theft
    SESSION_COOKIE_SAMESITE = "Lax"    # mitigates CSRF from cross-site requests
    # Set this to True when serving over HTTPS in production so the cookie
    # is never sent over plain HTTP.
    SESSION_COOKIE_SECURE = os.environ.get("SESSION_COOKIE_SECURE", "False") == "True"

    # ------------------------------------------------------------------
    # MySQL database connection
    # ------------------------------------------------------------------
    MYSQL_HOST = os.environ.get("MYSQL_HOST", "localhost")
    MYSQL_PORT = int(os.environ.get("MYSQL_PORT", 3306))
    MYSQL_USER = os.environ.get("MYSQL_USER", "auth_app_user")
    MYSQL_PASSWORD = os.environ.get("MYSQL_PASSWORD", "change-this-password")
    MYSQL_DATABASE = os.environ.get("MYSQL_DATABASE", "auth_system")

    # ------------------------------------------------------------------
    # Account lockout policy
    # ------------------------------------------------------------------
    MAX_FAILED_LOGIN_ATTEMPTS = 5
    LOCKOUT_DURATION_MINUTES = 15

    # ------------------------------------------------------------------
    # bcrypt
    # ------------------------------------------------------------------
    # Cost factor (aka "rounds"). Each +1 doubles the hashing time.
    # 12 is a solid default in 2026 hardware terms; raise it as hardware
    # gets faster to keep brute-force attacks expensive.
    BCRYPT_ROUNDS = 12
