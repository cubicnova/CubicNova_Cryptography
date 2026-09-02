"""
app.py
------
Main Flask application: routes, authentication logic, PBKDF2 password
hashing/verification, account lockout, session management, logging,
and input validation.

Route map
    GET       /            -> Redirects based on login state
    GET/POST  /register    -> Registration page
    GET/POST  /login       -> Login page
    GET       /dashboard   -> Protected dashboard (login required)
    GET       /logout      -> Destroys the session
"""

import hashlib
import hmac
import logging
import os
import re
from datetime import datetime, timedelta
from functools import wraps

import mysql.connector
from flask import (
    Flask, render_template, request, redirect,
    url_for, session, flash, g
)
from flask_wtf import CSRFProtect
from mysql.connector import errorcode

from config import Config

# --------------------------------------------------------------------
# App setup + logging
# --------------------------------------------------------------------
app = Flask(__name__)
app.config.from_object(Config)

# Log to both console and a rotating-free simple file. In production,
# swap this for a proper handler (RotatingFileHandler, syslog, etc.)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
logger = app.logger

csrf = CSRFProtect(app)  # validates csrf_token on every form POST


# --------------------------------------------------------------------
# Database helpers
# --------------------------------------------------------------------
def get_db_connection():
    """Open a new MySQL connection using credentials from config.py."""
    return mysql.connector.connect(
        host=app.config["MYSQL_HOST"],
        port=app.config["MYSQL_PORT"],
        user=app.config["MYSQL_USER"],
        password=app.config["MYSQL_PASSWORD"],
        database=app.config["MYSQL_DATABASE"],
    )


def get_db():
    """One connection per request, stored on Flask's `g` object."""
    if "db" not in g:
        g.db = get_db_connection()
    return g.db


@app.teardown_appcontext
def close_db(exception=None):
    db = g.pop("db", None)
    if db is not None and db.is_connected():
        db.close()


# --------------------------------------------------------------------
# PBKDF2 password hashing helpers
# --------------------------------------------------------------------
def generate_salt() -> bytes:
    """
    os.urandom() draws from the OS's cryptographically secure random
    number generator. Each user gets a fresh, unpredictable salt so
    identical passwords never produce identical stored hashes.
    """
    return os.urandom(app.config["PBKDF2_SALT_BYTES"])


def hash_password(password: str, salt: bytes) -> bytes:
    """
    Derives a key from the password + salt using PBKDF2-HMAC-SHA256,
    iterated hundreds of thousands of times. The high iteration count
    is what makes brute-forcing a stolen hash database slow, even
    though verifying one real login stays fast (a few hundred ms).
    """
    return hashlib.pbkdf2_hmac(
        app.config["PBKDF2_ALGORITHM"],
        password.encode("utf-8"),
        salt,
        app.config["PBKDF2_ITERATIONS"],
        dklen=app.config["PBKDF2_KEY_LENGTH"],
    )


def verify_password(password: str, salt_hex: str, stored_hash_hex: str) -> bool:
    """
    Recomputes the PBKDF2 hash for the submitted password using the
    user's stored salt, then compares it to the stored hash using
    hmac.compare_digest() -- a CONSTANT-TIME comparison. A naive `==`
    comparison exits as soon as it finds a mismatched byte, which can
    leak timing information an attacker could exploit to guess the
    hash byte-by-byte. compare_digest() always takes the same amount
    of time regardless of where (or whether) a mismatch occurs.
    """
    salt = bytes.fromhex(salt_hex)
    stored_hash = bytes.fromhex(stored_hash_hex)
    candidate_hash = hash_password(password, salt)
    return hmac.compare_digest(candidate_hash, stored_hash)


# --------------------------------------------------------------------
# Validation / sanitization helpers
# --------------------------------------------------------------------
USERNAME_RE = re.compile(r"^[A-Za-z0-9_]{3,30}$")
EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


def sanitize_input(value: str) -> str:
    """
    Trims whitespace and strips characters with no legitimate use in a
    username/email but common in injection/XSS payloads. This is a
    defense-in-depth layer -- the actual SQL-injection defense is the
    parameterized queries below, and the actual XSS defense is Jinja2's
    autoescaping in the templates.
    """
    if value is None:
        return ""
    value = value.strip()
    value = value.replace("<", "").replace(">", "")
    return value


def is_valid_username(username: str) -> bool:
    return bool(USERNAME_RE.match(username))


def is_valid_email(email: str) -> bool:
    return bool(EMAIL_RE.match(email)) and len(email) <= 100


def password_strength_errors(password: str) -> list:
    """
    Server-side password complexity enforcement (mirrors the
    client-side JS checks). Client-side checks can always be bypassed,
    so every rule is re-verified here before a password is ever hashed.
    """
    errors = []
    if len(password) < 8:
        errors.append("Password must be at least 8 characters long.")
    if not re.search(r"[a-z]", password):
        errors.append("Password must include a lowercase letter.")
    if not re.search(r"[A-Z]", password):
        errors.append("Password must include an uppercase letter.")
    if not re.search(r"[0-9]", password):
        errors.append("Password must include a number.")
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>_\-]", password):
        errors.append("Password must include a special character.")
    return errors


# --------------------------------------------------------------------
# Auth decorator
# --------------------------------------------------------------------
def login_required(view_func):
    """Redirects to /login if there's no authenticated user in the session."""
    @wraps(view_func)
    def wrapped(*args, **kwargs):
        if "user_id" not in session:
            flash("Please log in to access that page.", "error")
            return redirect(url_for("login"))
        return view_func(*args, **kwargs)
    return wrapped


# --------------------------------------------------------------------
# Routes
# --------------------------------------------------------------------
@app.route("/")
def home():
    if "user_id" in session:
        return redirect(url_for("dashboard"))
    return redirect(url_for("login"))


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")

    username = sanitize_input(request.form.get("username", ""))
    email = sanitize_input(request.form.get("email", "")).lower()
    password = request.form.get("password", "")
    confirm_password = request.form.get("confirm_password", "")

    errors = []
    if not is_valid_username(username):
        errors.append("Username must be 3-30 characters: letters, numbers, underscore only.")
    if not is_valid_email(email):
        errors.append("Please enter a valid email address.")
    if password != confirm_password:
        errors.append("Passwords do not match.")
    errors.extend(password_strength_errors(password))

    if errors:
        for e in errors:
            flash(e, "error")
        return render_template("register.html", username=username, email=email), 400

    db = get_db()
    cursor = db.cursor(dictionary=True)
    try:
        cursor.execute(
            "SELECT id FROM users WHERE username = %s OR email = %s",
            (username, email),
        )
        if cursor.fetchone():
            flash("That username or email is already registered.", "error")
            return render_template("register.html", username=username, email=email), 409

        # ---- PBKDF2 hashing workflow ------------------------------------
        # 1. Generate a fresh, random 16-byte salt for this user.
        # 2. Derive a 32-byte key from the password + salt using
        #    600,000 rounds of HMAC-SHA256 (PBKDF2).
        # 3. Store the salt and derived key as hex strings -- PBKDF2's
        #    output does not embed the salt or parameters the way
        #    bcrypt does, so we must persist the salt ourselves to be
        #    able to recompute the hash at login time.
        salt = generate_salt()
        derived_key = hash_password(password, salt)

        cursor.execute(
            """INSERT INTO users (username, email, password_hash, salt)
               VALUES (%s, %s, %s, %s)""",
            (username, email, derived_key.hex(), salt.hex()),
        )
        db.commit()
        logger.info(f"New user registered: username={username}")

    except mysql.connector.Error as err:
        db.rollback()
        if err.errno == errorcode.ER_DUP_ENTRY:
            flash("That username or email is already registered.", "error")
            return render_template("register.html", username=username, email=email), 409
        logger.error(f"Database error during registration: {err}")
        flash("Something went wrong. Please try again later.", "error")
        return render_template("register.html"), 500
    finally:
        cursor.close()

    flash("Account created successfully! Please log in.", "success")
    return redirect(url_for("login"))


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")

    username = sanitize_input(request.form.get("username", ""))
    password = request.form.get("password", "")

    if not username or not password:
        flash("Please enter both username and password.", "error")
        return render_template("login.html", username=username), 400

    db = get_db()
    cursor = db.cursor(dictionary=True)
    try:
        cursor.execute(
            """SELECT id, username, email, password_hash, salt,
                      failed_attempts, locked_until, created_at, last_login
               FROM users WHERE username = %s OR email = %s""",
            (username, username),
        )
        user = cursor.fetchone()

        # Same generic message for "no such user" and "wrong password"
        # so attackers can't enumerate valid usernames.
        generic_error = "Invalid username or password."

        if not user:
            logger.warning(f"Login attempt for unknown user: {username}")
            flash(generic_error, "error")
            return render_template("login.html", username=username), 401

        # ---- Account lockout check ---------------------------------------
        if user["locked_until"] and user["locked_until"] > datetime.now():
            minutes_left = int((user["locked_until"] - datetime.now()).total_seconds() // 60) + 1
            flash(f"Account locked due to too many failed attempts. "
                  f"Try again in {minutes_left} minute(s).", "error")
            return render_template("login.html", username=username), 423

        # ---- PBKDF2 verification -------------------------------------------
        password_ok = verify_password(password, user["salt"], user["password_hash"])

        if not password_ok:
            new_failed = user["failed_attempts"] + 1
            lock_update = ""
            params = [new_failed]

            if new_failed >= app.config["MAX_FAILED_LOGIN_ATTEMPTS"]:
                lock_until = datetime.now() + timedelta(
                    minutes=app.config["LOCKOUT_DURATION_MINUTES"]
                )
                lock_update = ", locked_until = %s"
                params.append(lock_until)
                logger.warning(f"Account locked after repeated failures: username={username}")
                flash("Too many failed attempts. Your account has been "
                      f"locked for {app.config['LOCKOUT_DURATION_MINUTES']} minutes.", "error")
            else:
                remaining = app.config["MAX_FAILED_LOGIN_ATTEMPTS"] - new_failed
                logger.warning(f"Failed login attempt for username={username}")
                flash(f"{generic_error} ({remaining} attempt(s) remaining before lockout)", "error")

            params.append(user["id"])
            cursor.execute(
                f"UPDATE users SET failed_attempts = %s{lock_update} WHERE id = %s",
                tuple(params),
            )
            db.commit()
            return render_template("login.html", username=username), 401

        # ---- Successful login ------------------------------------------------
        previous_last_login = user["last_login"]

        cursor.execute(
            """UPDATE users
               SET failed_attempts = 0, locked_until = NULL, last_login = %s
               WHERE id = %s""",
            (datetime.now(), user["id"]),
        )
        db.commit()
        logger.info(f"Successful login: username={username}")

        # Prevent session fixation: wipe any pre-login session data and
        # start a brand-new session identifier.
        session.clear()
        session["user_id"] = user["id"]
        session["username"] = user["username"]
        session["email"] = user["email"]
        session["created_at"] = user["created_at"].strftime("%Y-%m-%d %H:%M:%S")
        session["last_login"] = (
            previous_last_login.strftime("%Y-%m-%d %H:%M:%S")
            if previous_last_login else "First login"
        )
        session.permanent = True  # activates PERMANENT_SESSION_LIFETIME timeout

        flash(f"Welcome back, {user['username']}!", "success")
        return redirect(url_for("dashboard"))

    except mysql.connector.Error as err:
        logger.error(f"Database error during login: {err}")
        flash("Something went wrong. Please try again later.", "error")
        return render_template("login.html"), 500
    finally:
        cursor.close()


@app.route("/dashboard")
@login_required
def dashboard():
    return render_template(
        "dashboard.html",
        username=session.get("username"),
        email=session.get("email"),
        created_at=session.get("created_at"),
        last_login=session.get("last_login"),
    )


@app.route("/logout")
def logout():
    username = session.get("username", "unknown")
    session.clear()
    logger.info(f"User logged out: username={username}")
    flash("You have been logged out.", "success")
    return redirect(url_for("login"))


# --------------------------------------------------------------------
# Error handlers
# --------------------------------------------------------------------
@app.errorhandler(404)
def not_found(e):
    return render_template("login.html"), 404


@app.errorhandler(500)
def server_error(e):
    logger.error(f"Server error: {e}")
    flash("An unexpected error occurred. Please try again.", "error")
    return render_template("login.html"), 500


@app.errorhandler(400)
def bad_request(e):
    """Also catches Flask-WTF CSRF validation failures (invalid/missing token)."""
    flash("Your session expired or the request was invalid. Please try again.", "error")
    return render_template("login.html"), 400


if __name__ == "__main__":
    # debug=True is for local development ONLY.
    app.run(debug=True, host="127.0.0.1", port=5000)
