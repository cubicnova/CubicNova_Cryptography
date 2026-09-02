# PBKDF2 Password Hashing Authentication System

A Flask + MySQL authentication system that demonstrates secure password storage using **PBKDF2-HMAC-SHA256** (Password-Based Key Derivation Function 2), the NIST-recommended password hashing algorithm when a dedicated password-hashing library like bcrypt/Argon2 isn't available — built entirely on Python's standard library (`hashlib`, `hmac`, `os`).

---

## 1. Project Structure

```
password_hashing_project/
├── app.py                # Flask app: routes, PBKDF2 hashing/verification, sessions, logging
├── config.py              # Configuration (secrets, DB, PBKDF2 params, lockout policy)
├── pbkdf2_demo.py          # Standalone script demonstrating PBKDF2 concepts in isolation
├── requirements.txt
├── database/
│   └── schema.sql          # password_hashing_db + users table
├── templates/
│   ├── login.html
│   ├── register.html
│   └── dashboard.html
├── static/
│   ├── css/style.css       # Cybersecurity-themed responsive styling
│   ├── js/app.js           # Show/hide password, validation, strength meter
│   └── images/
└── README.md
```

### What each file does

| File | Purpose |
|---|---|
| `app.py` | All Flask routes (`/`, `/register`, `/login`, `/dashboard`, `/logout`), the PBKDF2 hashing/verification functions, account lockout, session handling, and structured logging of auth events. |
| `config.py` | Centralizes every setting — secret key, MySQL credentials, PBKDF2 iteration count/salt length/key length, lockout policy, session timeout — read from environment variables with dev fallbacks. |
| `pbkdf2_demo.py` | A dependency-free script you can run on its own (`python pbkdf2_demo.py`) to see salting, hashing, verification, constant-time comparison, and the iteration-count/attack-cost trade-off explained and printed step by step. |
| `database/schema.sql` | Creates the `password_hashing_db` database, a least-privilege MySQL user, and the `users` table. |
| `templates/*.html` | Jinja2 templates (auto-escaped, defending against XSS) rendered server-side. |
| `static/css/style.css` | One dark, cybersecurity-themed stylesheet shared by all three pages. |
| `static/js/app.js` | Client-side UX only: password show/hide, live validation, strength meter. Every rule is re-checked server-side — this file is convenience, not a security boundary. |

---

## 2. What Is Password Hashing?

Password hashing means storing a **one-way mathematical transformation** of a password instead of the password itself. Given the hash, it should be computationally infeasible to recover the original password. This way, if the database is ever stolen or leaked, attackers get hashes — not usable credentials — and cracking them requires expensive brute-force work rather than a simple read.

Hashing is different from **encryption**: encryption is reversible (with the right key); password hashing is deliberately one-way. There should be no "decrypt" operation for a password hash — verification always works by re-hashing the *candidate* password and comparing hashes, never by reversing the stored one.

## 3. Why PBKDF2?

PBKDF2 (RFC 2898 / NIST SP 800-132) takes a password, a random salt, and an iteration count, and repeatedly applies a pseudorandom function (here, HMAC-SHA256) to produce a fixed-length derived key. Its useful properties:

- **Deliberately slow, and tunably so.** Unlike a single SHA-256 hash (which is *fast*, making it a poor password hash — GPUs can compute billions per second), PBKDF2's iteration count lets you dial up the cost per guess as hardware improves.
- **Standardized and widely audited.** It's specified by NIST, required in many compliance frameworks (PCI-DSS, FIPS 140-2 contexts), and implemented directly in Python's standard library — no third-party dependency required.
- **Salted by design.** The salt parameter is mandatory to the function's construction, encouraging correct usage.
- **Trade-off to be aware of:** PBKDF2 is CPU-hard but not *memory*-hard, so it's more parallelizable on GPUs/ASICs than memory-hard alternatives like Argon2 or bcrypt. This project uses a high iteration count (600,000, per current OWASP guidance) to compensate; if you control your dependency stack, Argon2id is the strongest current recommendation.

## 4. How Salts Work

A salt is random data mixed into the password before hashing. It solves two problems:

1. **Rainbow tables.** Without a salt, an attacker can precompute hashes for common passwords once and reuse that table against every stolen database. A unique salt per user makes precomputed tables useless — the attacker would need one table per salt.
2. **Identical passwords → identical hashes.** Without a salt, two users with the password `Password123!` would have identical hash values, immediately revealing to anyone with database access that they share a password. A random salt makes their stored hashes completely different.

In this project: `generate_salt()` calls `os.urandom(16)` — the OS's cryptographically secure random number generator — for every new registration, and the salt is stored (hex-encoded) alongside the hash in its own `salt` column, since PBKDF2's raw output doesn't embed the salt the way some other schemes do.

## 5. Registration Workflow

1. User submits username, email, password, confirm password.
2. Server sanitizes and validates all fields (format, length, password complexity) — **again**, even though the browser already checked, because server-side validation is the only validation that can't be bypassed.
3. `generate_salt()` produces a fresh random 16-byte salt.
4. `hash_password(password, salt)` runs `hashlib.pbkdf2_hmac("sha256", password, salt, 600_000, dklen=32)`.
5. The resulting 32-byte derived key and the 16-byte salt are hex-encoded and written to `users.password_hash` and `users.salt`. **The plaintext password is never written to disk or logged anywhere.**

## 6. Login Verification Workflow

1. User submits username/email + password.
2. Server looks up the user by parameterized query and retrieves the stored `password_hash` and `salt`.
3. If the account is currently locked (`locked_until` in the future), the login is rejected immediately without touching the password at all.
4. `verify_password()` recomputes PBKDF2 over the *submitted* password using the *stored* salt and the *same* iteration count/key length used at registration.
5. The freshly computed hash is compared to the stored hash using `hmac.compare_digest()` — a **constant-time** comparison, so the time taken doesn't leak how many leading bytes matched (which would otherwise let an attacker guess the hash byte-by-byte via timing analysis).
6. Match → session created, `failed_attempts` reset, `last_login` updated. No match → `failed_attempts` incremented; after 5 failures the account locks for 15 minutes.

---

## 7. Database Schema

```sql
users
├── id               INT, PRIMARY KEY, AUTO_INCREMENT
├── username         VARCHAR(50), UNIQUE, NOT NULL
├── email             VARCHAR(100), UNIQUE, NOT NULL
├── password_hash     VARCHAR(255), NOT NULL   -- hex-encoded PBKDF2 derived key
├── salt              VARCHAR(255), NOT NULL   -- hex-encoded random salt
├── failed_attempts   INT, DEFAULT 0            -- lockout tracking
├── locked_until      DATETIME, NULL            -- lockout expiry
├── last_login        DATETIME, NULL
└── created_at        TIMESTAMP, DEFAULT NOW()
```

Design notes:
- `salt` is a **separate column** from `password_hash` — this is the key structural difference from bcrypt-based systems, where the salt is embedded inside the hash string itself. PBKDF2's raw output is just derived key bytes, so the application must persist the salt (and, implicitly, agree on the iteration count/algorithm via `config.py`) to be able to recompute the hash later.
- `username`/`email` are `UNIQUE` and indexed for fast, safe lookups on every login/register request.
- `failed_attempts`/`locked_until` implement account lockout without a separate table.
- The dedicated `pbkdf2_app_user` MySQL account only has `SELECT/INSERT/UPDATE/DELETE` on `password_hashing_db` — no schema-altering privileges, limiting damage if the app is ever compromised.

---

## 8. Security Features Implemented

| Feature | Where |
|---|---|
| **PBKDF2-HMAC-SHA256 hashing**, 600,000 iterations | `app.py` → `hash_password()`, `config.py` |
| **Secure random salt generation** (`os.urandom`) | `app.py` → `generate_salt()` |
| **Constant-time hash comparison** (`hmac.compare_digest`) | `app.py` → `verify_password()` |
| **SQL injection prevention** | All queries use `%s` parameterized placeholders |
| **CSRF protection** | `Flask-WTF`'s `CSRFProtect`, `{{ csrf_token() }}` in every form |
| **XSS mitigation** | Jinja2 auto-escaping + JS input stripping of `<`/`>` |
| **Secure session management** | `HttpOnly`, `SameSite=Lax` cookies, session cleared/regenerated on login |
| **Session timeout** | 30-minute sliding window (`PERMANENT_SESSION_LIFETIME`, `SESSION_REFRESH_EACH_REQUEST`) |
| **Account lockout** | 5 failed attempts → 15-minute lockout |
| **Password complexity enforcement** | `password_strength_errors()`, both client- and server-side |
| **Input validation & sanitization** | `sanitize_input()`, `is_valid_username()`, `is_valid_email()` |
| **Exception handling & logging** | Every DB operation wrapped in try/except; auth events logged via `app.logger` |
| **Least-privilege DB account** | `database/schema.sql` |
| **Protected routes** | `@login_required` decorator |

### Common password storage mistakes this project avoids
- ❌ Storing plaintext passwords — this project stores only a PBKDF2 derived key.
- ❌ Using a fast general-purpose hash like plain MD5/SHA-256 for passwords — those are *designed to be fast*, which is exactly wrong for password storage; PBKDF2's iteration count intentionally slows things down.
- ❌ Reusing one global salt for all users — defeats the purpose of salting; this project generates a unique salt per user.
- ❌ Comparing hashes with `==` — vulnerable to timing attacks; this project uses `hmac.compare_digest()`.
- ❌ No limit on login attempts — this project locks accounts after repeated failures.
- ❌ Revealing whether a username exists via different error messages — this project uses one generic message for both cases.

---

## 9. Installation Guide (Kali Linux)

Kali ships with Python 3 and MySQL client tools, but MariaDB/MySQL server usually needs to be installed and started manually.

### Step 1 — Update packages and install MySQL/MariaDB server
```bash
sudo apt update
sudo apt install -y mariadb-server python3-venv python3-pip
```

### Step 2 — Start and enable the database service
```bash
sudo service mariadb start
# Optional, to auto-start on boot if you're using systemd:
sudo systemctl enable mariadb
```

### Step 3 — Secure the installation (recommended)
```bash
sudo mysql_secure_installation
```
Follow the prompts to set a root password and remove anonymous users.

### Step 4 — Create the database and app user
```bash
sudo mysql -u root -p < database/schema.sql
```
**Edit the password inside `database/schema.sql` first** (replace `change-this-password`), and use the same value for `MYSQL_PASSWORD` in Step 6.

### Step 5 — Set up a Python virtual environment
```bash
cd password_hashing_project
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Step 6 — Configure environment variables
Create a `.env` file in the project root:
```
SECRET_KEY=replace-with-a-long-random-string
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_USER=pbkdf2_app_user
MYSQL_PASSWORD=change-this-password
MYSQL_DATABASE=password_hashing_db
SESSION_COOKIE_SECURE=False
```
Generate a strong `SECRET_KEY`:
```bash
python3 -c "import secrets; print(secrets.token_hex(32))"
```

### Step 7 — Run the PBKDF2 concept demo (optional but recommended)
```bash
python3 pbkdf2_demo.py
```
This prints a full walkthrough of salting, hashing, verification, and iteration-count timing — useful for understanding the concepts before touching the web app.

### Step 8 — Run the Flask application
```bash
python3 app.py
```
Visit **http://127.0.0.1:5000** in your browser. Register a new account, then log in.

---

## 10. Security Best Practices for Production Deployment

- Serve over HTTPS and set `SESSION_COOKIE_SECURE=True`.
- Set `debug=False` in `app.py` — Flask's debugger exposes an interactive shell to anyone who can trigger a 500 error.
- Add network/proxy-level rate limiting (e.g., Flask-Limiter, or nginx `limit_req`) in addition to the application-level account lockout.
- Consider email verification and a password-reset flow (with time-limited, single-use tokens) for a complete system.
- Periodically re-hash: if you raise `PBKDF2_ITERATIONS` later, re-hash each user's password (with the new iteration count) the next time they log in successfully.
- Keep the MySQL app account least-privilege, as configured in `schema.sql` — never point the app at a `root` database account.

---

## 11. Testing the App

1. **Run `pbkdf2_demo.py`** first to see the hashing mechanics printed out in isolation.
2. **Register** a new account — try a weak password to see the strength meter and validation react live.
3. **Log in** with the wrong password 5 times — observe the lockout message and countdown.
4. **Log in** correctly — you'll land on `/dashboard`, showing your username, email, account creation date, and last login.
5. Visit `/dashboard` in a private window with no session — you're redirected to `/login`.
6. **Log out** — the session is destroyed and you return to the login page.
