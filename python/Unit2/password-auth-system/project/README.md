# Secure Password Hashing Authentication System

A production-structured (but learning-friendly) authentication system built with **Flask**, **MySQL**, **bcrypt**, and vanilla **HTML/CSS/JavaScript**. It demonstrates how to correctly hash and verify passwords, protect against common web attacks, and manage sessions safely.

---

## 1. Project Structure

```
project/
├── app.py                  # Flask application: routes, auth logic, bcrypt hashing
├── config.py                # App + database configuration
├── requirements.txt         # Python dependencies
├── templates/
│   ├── login.html           # Login page
│   ├── register.html        # Registration page
│   └── dashboard.html       # Protected dashboard
├── static/
│   ├── css/style.css        # Shared, responsive styling
│   ├── js/
│   │   ├── common.js        # Show/hide password + shared helpers
│   │   ├── login.js         # Login form client-side validation
│   │   └── register.js      # Register form validation + strength meter
│   └── images/              # (placeholder for any icons/logos you add)
└── database/
    └── schema.sql           # MySQL database + table creation
```

### What each file does

| File | Purpose |
|---|---|
| `app.py` | Defines every route (`/`, `/register`, `/login`, `/dashboard`, `/logout`), the bcrypt hashing/verification logic, account lockout logic, session handling, and input validation. |
| `config.py` | Centralizes all configuration (secret key, MySQL credentials, session timeout, lockout policy, bcrypt cost factor) so nothing sensitive is hardcoded inside `app.py`. Reads from environment variables with local dev fallbacks. |
| `database/schema.sql` | Creates the `auth_system` database, a least-privilege MySQL user, and the `users` table with all required columns and indexes. |
| `templates/*.html` | Jinja2 templates rendered server-side. Jinja2 auto-escapes all variables, which is your primary defense against XSS. |
| `static/css/style.css` | One shared stylesheet for a consistent, responsive, centered-card design across all three pages. |
| `static/js/*.js` | Client-side UX only: password show/hide toggle, live field validation, and the password-strength meter. **Never trusted as the sole line of defense** — everything is re-validated server-side. |

---

## 2. Installation & Setup

### Step 1 — Install MySQL and create the database
```bash
mysql -u root -p < database/schema.sql
```
This creates the `auth_system` database, the `users` table, and a dedicated `auth_app_user` MySQL account. **Edit the password in `schema.sql` before running it**, and use the same password in your environment variables (Step 3).

### Step 2 — Create a Python virtual environment
```bash
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
```

### Step 3 — Install dependencies
```bash
pip install -r requirements.txt
```

### Step 4 — Configure environment variables
Create a `.env` file in the project root (or export these in your shell):
```
SECRET_KEY=replace-with-a-long-random-string
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_USER=auth_app_user
MYSQL_PASSWORD=change-this-password
MYSQL_DATABASE=auth_system
SESSION_COOKIE_SECURE=False   # set to True once served over HTTPS
```
Generate a strong `SECRET_KEY` with:
```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

### Step 5 — Run the application
```bash
python app.py
```
Visit **http://127.0.0.1:5000** — you'll be redirected to the login page. Click "Create one" to register a new account.

---

## 3. How bcrypt Password Hashing Works (Registration)

1. The user submits a plaintext password over HTTPS (in production).
2. The server **never stores it as-is**. Instead:
   ```python
   salt = bcrypt.gensalt(rounds=12)
   password_hash = bcrypt.hashpw(password.encode("utf-8"), salt)
   ```
3. `bcrypt.gensalt()` produces a **cryptographically random salt** — this guarantees that two users with the identical password get completely different stored hashes, which defeats precomputed "rainbow table" attacks.
4. `bcrypt.hashpw()` runs the password + salt through the Blowfish-based hashing algorithm **2^rounds times** (here, 2^12 = 4096 iterations). This deliberate slowness makes brute-force and dictionary attacks computationally expensive, even if the database is stolen.
5. The output is a single self-contained string like:
   ```
   $2b$12$KIXQ4z7l3n9s...   (algorithm $ cost $ salt+hash, all in one field)
   ```
   Because the salt is embedded in the hash itself, there's no need for a separate `salt` column — this is why the schema only has `password_hash`.
6. Only this hash is written to the `users.password_hash` column.

## 4. How Login Verification Works

1. The user submits a username/email + password.
2. The server fetches the corresponding `password_hash` from MySQL using a **parameterized query**.
3. ```python
   bcrypt.checkpw(password.encode("utf-8"), stored_hash)
   ```
   `checkpw()` extracts the salt and cost factor from the stored hash, re-hashes the submitted password with those same parameters, and compares the two hashes **in constant time** (to avoid timing-attack leaks). It never "decrypts" anything — bcrypt hashing is one-way by design.
4. If they match, the login succeeds; the failed-attempt counter is reset and a new session is created.
5. If they don't match, a failed-attempt counter increments; after 5 failures the account is locked for 15 minutes (`locked_until` timestamp) — this defeats online brute-force/credential-stuffing attacks.
6. Both "wrong password" and "no such user" return the same generic message ("Invalid username or password") to prevent username enumeration.

---

## 5. Database Design

```sql
users
├── id               INT, PRIMARY KEY, AUTO_INCREMENT
├── username         VARCHAR(50), UNIQUE, NOT NULL
├── email             VARCHAR(100), UNIQUE, NOT NULL
├── password_hash     VARCHAR(255), NOT NULL      -- bcrypt hash only
├── failed_attempts   INT, DEFAULT 0               -- lockout tracking
├── locked_until      DATETIME, NULL               -- lockout expiry
├── last_login        DATETIME, NULL               -- shown on dashboard
└── created_at        TIMESTAMP, DEFAULT NOW()
```

Design decisions:
- `username` and `email` are both `UNIQUE` and indexed — this makes the lookup queries used on every login/register request fast (`O(log n)` instead of a full table scan) and enforces no-duplicate-accounts at the database layer, not just in application code.
- `password_hash VARCHAR(255)` gives generous headroom; a bcrypt hash is ~60 characters, so this comfortably accommodates future algorithm changes (e.g., migrating to Argon2 hashes, which can be longer).
- `failed_attempts` / `locked_until` implement account lockout without needing a separate table.
- The dedicated `auth_app_user` MySQL account only has `SELECT/INSERT/UPDATE/DELETE` on this one database — it cannot `DROP TABLE`, create new users, or touch other databases, limiting blast radius if the app is ever compromised.

---

## 6. Security Features Implemented

| Feature | Where |
|---|---|
| **bcrypt password hashing** (salted, cost-factor 12) | `app.py` → `register()` |
| **Constant-time password verification** | `app.py` → `login()` via `bcrypt.checkpw()` |
| **SQL injection prevention** | Every query uses `%s` parameterized placeholders — user input is always sent as data, never concatenated into SQL strings |
| **CSRF protection** | `Flask-WTF`'s `CSRFProtect` validates a per-session token (`{{ csrf_token() }}`) on every form POST |
| **XSS mitigation** | Jinja2 auto-escapes all template variables; JS also strips `<`/`>` from inputs as a secondary layer |
| **Secure session management** | `HttpOnly`, `SameSite=Lax` cookies; `SECRET_KEY`-signed sessions; `session.clear()` + fresh session on login (prevents session fixation) |
| **Session timeout** | `PERMANENT_SESSION_LIFETIME = 30 minutes`, sliding window via `SESSION_REFRESH_EACH_REQUEST` |
| **Account lockout** | 5 failed attempts → 15-minute lockout (`config.py`: `MAX_FAILED_LOGIN_ATTEMPTS`, `LOCKOUT_DURATION_MINUTES`) |
| **Generic auth error messages** | Prevents attackers from telling whether a username exists |
| **Input sanitization & validation** | `sanitize_input()`, `is_valid_username()`, `is_valid_email()`, `password_strength_errors()` — enforced both client- and server-side |
| **Least-privilege DB account** | `database/schema.sql` creates `auth_app_user` with only the grants the app needs |
| **Protected routes** | `@login_required` decorator redirects unauthenticated users to `/login` |
| **No plaintext/reversible password storage** | Only `password_hash` (bcrypt) is ever persisted |

### Security best practices worth calling out
- **Defense in depth**: client-side JS validation is a UX nicety, never a security boundary — every rule is enforced again in `app.py`.
- **Fail closed**: on any database error during login/register, the user sees a generic error and no session is created.
- **Least privilege**: the app's MySQL user cannot alter schema or access other databases.
- **Constant-time comparison**: bcrypt's `checkpw` avoids leaking timing information that could help an attacker guess a password character-by-character.
- **Cost factor tuning**: `BCRYPT_ROUNDS` in `config.py` should be raised over time as hardware gets faster — re-hash on next successful login if you increase it later.
- **Production hardening you should add**: serve over HTTPS and set `SESSION_COOKIE_SECURE=True`, set `debug=False`, add rate limiting (e.g. Flask-Limiter) at the network/proxy layer in addition to the app-level lockout, and consider adding email verification and password-reset flows.

---

## 7. Testing the App

1. **Register** a new account — try a weak password first to see the strength meter and validation errors in action.
2. **Log in** with the wrong password 5 times — observe the account lockout message and 15-minute countdown.
3. **Log in** correctly — you'll land on `/dashboard`, showing your username and last login time.
4. Try visiting `/dashboard` in a private/incognito window (no session) — you'll be redirected to `/login`.
5. **Log out** — your session is destroyed and you're returned to the login page.
