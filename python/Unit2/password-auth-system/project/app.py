"""
app.py
------
Main Flask application: routes, authentication logic, bcrypt password
hashing/verification, account lockout, session management, and input
validation.

Route map
    GET/POST  /            -> Home page (redirects based on login state)
    GET/POST  /register    -> Registration page
    GET/POST  /login       -> Login page
    GET       /dashboard   -> Protected dashboard (login required)
    GET       /logout      -> Destroys the session

Run with:  python app.py
"""

import re
from datetime import datetime, timedelta

import bcrypt
import mysql.connector
from flask import (
    Flask, render_template, request, redirect,
    url_for, session, flash, g
)
from flask_wtf import CSRFProtect
from mysql.connector import errorcode

from config import Config

# --------------------------------------------------------------------
# App setup
# --------------------------------------------------------------------
app = Flask(__name__)
app.config.from_object(Config)

# CSRFProtect automatically validates a csrf_token on every POST/PUT/
# PATCH/DELETE request submitted via a standard HTML form. Every form
# in templates/*.html includes {{ csrf_token() }} in a hidden field.
csrf = CSRFProtect(app)


# --------------------------------------------------------------------
# Database helpers
# --------------------------------------------------------------------
def get_db_connection():
    """
    Open a new MySQL connection using credentials from config.py.
    A fresh connection per request is simple and safe for a learning /
    small-scale app; for higher traffic, swap this for a connection
    pool (mysql.connector.pooling.MySQLConnectionPool).
    """
    return mysql.connector.connect(
        host=app.config["MYSQL_HOST"],
        port=app.config["MYSQL_PORT"],
        user=app.config["MYSQL_USER"],
        password=app.config["MYSQL_PASSWORD"],
        database=app.config["MYSQL_DATABASE"],
    )


def get_db():
    """
    Store one connection per request on Flask's `g` object so multiple
    helper functions in the same request reuse it instead of opening
    several connections.
    """
    if "db" not in g:
        g.db = get_db_connection()
    return g.db


@app.teardown_appcontext
def close_db(exception=None):
    """Automatically close the DB connection at the end of every request."""
    db = g.pop("db", None)
    if db is not None and db.is_connected():
        db.close()


# --------------------------------------------------------------------
# Validation / sanitization helpers
# --------------------------------------------------------------------
USERNAME_RE = re.compile(r"^[A-Za-z0-9_]{3,30}$")
EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


def sanitize_input(value: str) -> str:
    """
    Basic input sanitization: trims whitespace and strips characters
    that have no legitimate use in a username/email but are common in
    injection/XSS payloads. This is a defense-in-depth layer -- the
    REAL SQL-injection defense is the parameterized queries below, and
    the real XSS defense is Jinja2's autoescaping in the templates.
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
    Server-side password strength validation (mirrors the client-side
    JS checks in static/js/register.js). We NEVER trust client-side
    validation alone -- it can be bypassed, so every rule is re-checked
    here before a password is ever hashed and stored.
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
from functools import wraps


def login_required(view_func):
    """
    Protects a route: if there's no logged-in user in the session,
    redirect to the login page instead of running the view.
    """
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
    """Landing route: send logged-in users to their dashboard, others to login."""
    if "user_id" in session:
        return redirect(url_for("dashboard"))
    return redirect(url_for("login"))


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")

    # ---- Collect + sanitize input -----------------------------------
    username = sanitize_input(request.form.get("username", ""))
    email = sanitize_input(request.form.get("email", "")).lower()
    password = request.form.get("password", "")
    confirm_password = request.form.get("confirm_password", "")

    # ---- Server-side validation (defense in depth) -------------------
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
        # Re-render with previously entered (safe) values so the user
        # doesn't have to retype everything.
        return render_template("register.html", username=username, email=email), 400

    db = get_db()
    cursor = db.cursor(dictionary=True)
    try:
        # Check for existing username/email using a PARAMETERIZED query.
        # The %s placeholders mean user input is always sent to MySQL as
        # data, never concatenated into the SQL string -- this is what
        # prevents SQL injection (e.g. entering `' OR '1'='1`).
        cursor.execute(
            "SELECT id FROM users WHERE username = %s OR email = %s",
            (username, email),
        )
        if cursor.fetchone():
            flash("That username or email is already registered.", "error")
            return render_template("register.html", username=username, email=email), 409

        # ---- bcrypt hashing workflow ----------------------------------
        # 1. bcrypt.gensalt() generates a fresh, random salt (bcrypt
        #    embeds the salt + cost factor inside the resulting hash
        #    string itself, so we don't need a separate salt column).
        # 2. bcrypt.hashpw() combines the salt with the password and
        #    runs it through the Blowfish-based hash function
        #    `rounds` times (2^rounds), making brute force expensive.
        salt = bcrypt.gensalt(rounds=app.config["BCRYPT_ROUNDS"])
        password_hash = bcrypt.hashpw(password.encode("utf-8"), salt)

        cursor.execute(
            """INSERT INTO users (username, email, password_hash)
               VALUES (%s, %s, %s)""",
            (username, email, password_hash.decode("utf-8")),
        )
        db.commit()

    except mysql.connector.Error as err:
        db.rollback()
        if err.errno == errorcode.ER_DUP_ENTRY:
            flash("That username or email is already registered.", "error")
            return render_template("register.html", username=username, email=email), 409
        app.logger.error(f"Database error during registration: {err}")
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
        # Parameterized lookup -- safe against SQL injection.
        cursor.execute(
            """SELECT id, username, password_hash, failed_attempts, locked_until
               FROM users WHERE username = %s OR email = %s""",
            (username, username),
        )
        user = cursor.fetchone()

        # Use one generic error message for "no such user" and "wrong
        # password" so attackers can't enumerate valid usernames.
        generic_error = "Invalid username or password."

        if not user:
            flash(generic_error, "error")
            return render_template("login.html", username=username), 401

        # ---- Account lockout check -------------------------------------
        if user["locked_until"] and user["locked_until"] > datetime.now():
            minutes_left = int((user["locked_until"] - datetime.now()).total_seconds() // 60) + 1
            flash(f"Account locked due to too many failed attempts. "
                  f"Try again in {minutes_left} minute(s).", "error")
            return render_template("login.html", username=username), 423

        # ---- bcrypt verification -----------------------------------------
        # bcrypt.checkpw() re-derives the hash using the SAME salt that
        # is embedded in the stored hash string, then compares the
        # result to the stored hash in constant time. We never decrypt
        # the stored hash (it's one-way) -- we only ever re-hash the
        # candidate password and compare hashes.
        stored_hash = user["password_hash"].encode("utf-8")
        password_ok = bcrypt.checkpw(password.encode("utf-8"), stored_hash)

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
                flash("Too many failed attempts. Your account has been "
                      f"locked for {app.config['LOCKOUT_DURATION_MINUTES']} minutes.", "error")
            else:
                remaining = app.config["MAX_FAILED_LOGIN_ATTEMPTS"] - new_failed
                flash(f"{generic_error} ({remaining} attempt(s) remaining before lockout)", "error")

            params.append(user["id"])
            cursor.execute(
                f"UPDATE users SET failed_attempts = %s{lock_update} WHERE id = %s",
                tuple(params),
            )
            db.commit()
            return render_template("login.html", username=username), 401

        # ---- Successful login: reset lockout counters, record last_login --
        previous_login_row_cursor = db.cursor(dictionary=True)
        previous_login_row_cursor.execute(
            "SELECT last_login FROM users WHERE id = %s", (user["id"],)
        )
        previous_login = previous_login_row_cursor.fetchone()["last_login"]
        previous_login_row_cursor.close()

        cursor.execute(
            """UPDATE users
               SET failed_attempts = 0, locked_until = NULL, last_login = %s
               WHERE id = %s""",
            (datetime.now(), user["id"]),
        )
        db.commit()

        # ---- Establish the session ---------------------------------------
        # Regenerate/clear the session first to prevent session fixation
        # (never reuse a session identifier a pre-login visitor may have
        # been assigned).
        session.clear()
        session["user_id"] = user["id"]
        session["username"] = user["username"]
        session["last_login"] = previous_login.strftime("%Y-%m-%d %H:%M:%S") if previous_login else "First login"
        session.permanent = True  # activates PERMANENT_SESSION_LIFETIME timeout

        flash(f"Welcome back, {user['username']}!", "success")
        return redirect(url_for("dashboard"))

    except mysql.connector.Error as err:
        app.logger.error(f"Database error during login: {err}")
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
        last_login=session.get("last_login"),
    )


@app.route("/logout")
def logout():
    session.clear()
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
    app.logger.error(f"Server error: {e}")
    flash("An unexpected error occurred. Please try again.", "error")
    return render_template("login.html"), 500


@app.errorhandler(400)
def bad_request(e):
    """
    Handles rejected requests, including CSRF validation failures
    raised by Flask-WTF (invalid/missing csrf_token).
    """
    flash("Your session expired or the request was invalid. Please try again.", "error")
    return render_template("login.html"), 400


if __name__ == "__main__":
    # debug=True is for local development ONLY -- never run with debug
    # mode enabled in production (it exposes an interactive debugger
    # and stack traces to anyone who can trigger an error).
    app.run(debug=True, host="127.0.0.1", port=5000)
