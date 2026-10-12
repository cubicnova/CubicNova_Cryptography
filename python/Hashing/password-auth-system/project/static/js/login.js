/**
 * login.js
 * Lightweight client-side validation for the login form. The real
 * verification (bcrypt.checkpw against the stored hash, lockout
 * checks) happens server-side in app.py -- this is UX-only.
 */

document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("login-form");
  if (!form) return;

  const username = document.getElementById("username");
  const password = document.getElementById("password");
  const usernameError = document.getElementById("username-error");
  const passwordError = document.getElementById("password-error");

  form.addEventListener("submit", (e) => {
    let valid = true;

    if (!username.value.trim()) {
      showFieldError(username, usernameError, "Username or email is required.");
      valid = false;
    } else {
      clearFieldError(username, usernameError);
    }

    if (!password.value) {
      showFieldError(password, passwordError, "Password is required.");
      valid = false;
    } else {
      clearFieldError(password, passwordError);
    }

    if (!valid) {
      e.preventDefault();
    }
  });
});
