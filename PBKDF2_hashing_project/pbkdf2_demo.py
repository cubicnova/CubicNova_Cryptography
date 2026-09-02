"""
pbkdf2_demo.py
--------------
A standalone, dependency-free walkthrough of everything the main app
does cryptographically -- run this file directly to see PBKDF2 salting,
hashing, verification, and constant-time comparison in action, plus a
demonstration of why the iteration count matters.

Run with:
    python pbkdf2_demo.py
"""

import hashlib
import hmac
import os
import time


# ---------------------------------------------------------------------
# 1. Salt generation
# ---------------------------------------------------------------------
def generate_salt(num_bytes: int = 16) -> bytes:
    """
    os.urandom() pulls bytes from the operating system's cryptographically
    secure random number generator (CSPRNG) -- e.g. /dev/urandom on
    Linux. This is NOT the same as Python's `random` module, which is
    predictable and unsafe for anything security-related.

    A unique, random salt per user means:
      * Two users with the same password get completely different
        stored hashes.
      * Attackers can't use a single precomputed "rainbow table" against
        the whole database -- they'd need one per salt, which is
        infeasible.
    """
    return os.urandom(num_bytes)


# ---------------------------------------------------------------------
# 2. Password hashing
# ---------------------------------------------------------------------
def hash_password(password: str, salt: bytes, iterations: int = 600_000,
                   key_length: int = 32, algorithm: str = "sha256") -> bytes:
    """
    hashlib.pbkdf2_hmac() repeatedly applies HMAC-SHA256 to the password
    and salt `iterations` times, then truncates/expands the result to
    `key_length` bytes. This deliberate, tunable slowness is the whole
    point: it makes brute-force / dictionary attacks against stolen
    hashes computationally expensive, while a legitimate login (which
    only needs to hash once) stays fast enough to be imperceptible.
    """
    return hashlib.pbkdf2_hmac(
        algorithm,
        password.encode("utf-8"),
        salt,
        iterations,
        dklen=key_length,
    )


# ---------------------------------------------------------------------
# 3. Password verification (login-time)
# ---------------------------------------------------------------------
def verify_password(password: str, salt: bytes, stored_hash: bytes,
                     iterations: int = 600_000, key_length: int = 32,
                     algorithm: str = "sha256") -> bool:
    """
    To verify a login attempt, we do NOT "decrypt" the stored hash --
    PBKDF2 is a one-way function, there is nothing to decrypt. Instead
    we recompute the hash from the submitted password using the SAME
    salt, iteration count, and key length that were used at
    registration time, then compare the two hash values.
    """
    candidate_hash = hash_password(password, salt, iterations, key_length, algorithm)
    return constant_time_compare(candidate_hash, stored_hash)


# ---------------------------------------------------------------------
# 4. Constant-time hash comparison
# ---------------------------------------------------------------------
def constant_time_compare(hash_a: bytes, hash_b: bytes) -> bool:
    """
    hmac.compare_digest() compares two byte strings in a way that takes
    the same amount of time regardless of how many leading bytes match.

    Why this matters: a naive `hash_a == hash_b` comparison in Python
    (and most languages) short-circuits at the FIRST mismatched byte.
    An attacker who can measure response times precisely could exploit
    that to guess a hash one byte at a time ("timing attack"). Using
    a constant-time comparison closes that side channel.
    """
    return hmac.compare_digest(hash_a, hash_b)


# ---------------------------------------------------------------------
# 5. Iteration count vs. attack cost
# ---------------------------------------------------------------------
def measure_hashing_time(password: str, iterations: int) -> float:
    """Times a single PBKDF2 hash computation for a given iteration count."""
    salt = generate_salt()
    start = time.perf_counter()
    hash_password(password, salt, iterations=iterations)
    return time.perf_counter() - start


def demonstrate_iteration_impact():
    print("\n--- Iteration count vs. computation time ---")
    print("(Illustrates why a higher iteration count slows down")
    print(" brute-force attacks while remaining fast for one real login.)\n")

    for iterations in (1_000, 100_000, 600_000, 1_000_000):
        elapsed = measure_hashing_time("SamplePassword123!", iterations)
        # Rough estimate: attacker attempts per second on ONE CPU core
        # trying this many candidate passwords against ONE stolen hash.
        attempts_per_second = 1 / elapsed if elapsed > 0 else float("inf")
        print(f"  {iterations:>9,} iterations -> {elapsed*1000:8.2f} ms/hash "
              f"(~{attempts_per_second:,.0f} guesses/sec/core against a stolen hash)")

    print("\n  A single real login only ever pays this cost ONCE per attempt,")
    print("  so higher iteration counts are nearly free for legitimate users")
    print("  but expensive for someone brute-forcing millions of guesses.")


# ---------------------------------------------------------------------
# Full demo walkthrough
# ---------------------------------------------------------------------
def main():
    print("=" * 70)
    print("PBKDF2-HMAC-SHA256 Password Hashing Demonstration")
    print("=" * 70)

    # --- Registration simulation -------------------------------------
    password = "CorrectHorseBattery9!"
    print(f"\n[Registration] Plaintext password (never stored): {password!r}")

    salt = generate_salt(16)
    print(f"[Registration] Generated random salt (hex): {salt.hex()}")

    iterations = 600_000
    derived_key = hash_password(password, salt, iterations=iterations)
    print(f"[Registration] PBKDF2 derived key (hex, {iterations:,} iterations):")
    print(f"                {derived_key.hex()}")
    print("[Registration] -> Only `salt` and `password_hash` (derived key) are")
    print("                  written to the database. The plaintext password")
    print("                  is discarded from memory as soon as possible.")

    # --- Login simulation: correct password ---------------------------
    print("\n[Login attempt #1] User re-enters the CORRECT password.")
    attempt_1 = "CorrectHorseBattery9!"
    result_1 = verify_password(attempt_1, salt, derived_key, iterations=iterations)
    print(f"                    Verification result: {result_1} (expected: True)")

    # --- Login simulation: wrong password ------------------------------
    print("\n[Login attempt #2] User enters an INCORRECT password.")
    attempt_2 = "WrongPassword123!"
    result_2 = verify_password(attempt_2, salt, derived_key, iterations=iterations)
    print(f"                    Verification result: {result_2} (expected: False)")

    # --- Same password, different user -> different hash --------------
    print("\n[Two users, same password] Demonstrates why per-user salts matter.")
    salt_user_a = generate_salt(16)
    salt_user_b = generate_salt(16)
    hash_user_a = hash_password("SharedPassword1!", salt_user_a, iterations=iterations)
    hash_user_b = hash_password("SharedPassword1!", salt_user_b, iterations=iterations)
    print(f"  User A hash: {hash_user_a.hex()}")
    print(f"  User B hash: {hash_user_b.hex()}")
    print(f"  Hashes identical? {hash_user_a == hash_user_b} "
          f"(expected: False, even though the password is identical)")

    # --- Iteration-count impact ----------------------------------------
    demonstrate_iteration_impact()

    print("\n" + "=" * 70)
    print("Demo complete.")
    print("=" * 70)


if __name__ == "__main__":
    main()
