/**
 * app.js
 * Client-side behavior for the login and registration pages:
 *   - Show/Hide password toggle
 *   - Live field validation
 *   - Password strength meter (registration only)
 *
 * IMPORTANT: none of this is a security boundary. Every rule here is
 * re-enforced server-side in app.py (Flask), because JavaScript can
 * always be disabled, edited, or bypassed by a direct HTTP request.
 */

// ---------------------------------------------------------------------
// Shared helpers
// ---------------------------------------------------------------------
function togglePasswordVisibility(inputId, btn) {
  const input = document.getElementById(inputId);
  if (!input) return;
  const isHidden = input.type === "password";
  input.type = isHidden ? "text" : "password";
  btn.textContent = isHidden ? "🙈" : "👁️";
  btn.setAttribute("aria-label", isHidden ? "Hide password" : "Show password");
}

function showFieldError(inputEl, errorEl, message) {
  if (!inputEl) return;
  inputEl.classList.add("is-invalid");
  inputEl.classList.remove("is-valid");
  if (errorEl) {
    errorEl.textContent = message;
    errorEl.classList.add("show");
  }
}

function clearFieldError(inputEl, errorEl) {
  if (!inputEl) return;
  inputEl.classList.remove("is-invalid");
  inputEl.classList.add("is-valid");
  if (errorEl) {
    errorEl.textContent = "";
    errorEl.classList.remove("show");
  }
}

const USERNAME_RE = /^[A-Za-z0-9_]{3,30}$/;
const EMAIL_RE = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

function validatePasswordRules(pwd) {
  const rules = [];
  if (pwd.length < 8) rules.push("At least 8 characters");
  if (!/[a-z]/.test(pwd)) rules.push("A lowercase letter");
  if (!/[A-Z]/.test(pwd)) rules.push("An uppercase letter");
  if (!/[0-9]/.test(pwd)) rules.push("A number");
  if (!/[!@#$%^&*(),.?":{}|<>_\-]/.test(pwd)) rules.push("A special character");
  return rules;
}

function evaluatePasswordStrength(pwd) {
  let score = 0;
  if (pwd.length >= 8) score++;
  if (pwd.length >= 12) score++;
  if (/[a-z]/.test(pwd)) score++;
  if (/[A-Z]/.test(pwd)) score++;
  if (/[0-9]/.test(pwd)) score++;
  if (/[!@#$%^&*(),.?":{}|<>_\-]/.test(pwd)) score++;
  return score; // 0-6
}

// ---------------------------------------------------------------------
// Wire up password show/hide toggles on any page that has them
// ---------------------------------------------------------------------
document.addEventListener("DOMContentLoaded", () => {
  document.querySelectorAll("[data-toggle-password]").forEach((btn) => {
    btn.addEventListener("click", () => {
      togglePasswordVisibility(btn.getAttribute("data-toggle-password"), btn);
    });
  });

  initLoginForm();
  initRegisterForm();
});

// ---------------------------------------------------------------------
// Login page behavior
// ---------------------------------------------------------------------
function initLoginForm() {
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

    if (!valid) e.preventDefault();
  });
}

// ---------------------------------------------------------------------
// Registration page behavior
// ---------------------------------------------------------------------
function initRegisterForm() {
  const form = document.getElementById("register-form");
  if (!form) return;

  const username = document.getElementById("username");
  const email = document.getElementById("email");
  const password = document.getElementById("password");
  const confirmPassword = document.getElementById("confirm_password");

  const usernameError = document.getElementById("username-error");
  const emailError = document.getElementById("email-error");
  const passwordError = document.getElementById("password-error");
  const confirmError = document.getElementById("confirm-error");

  const strengthFill = document.getElementById("strength-fill");
  const strengthLabel = document.getElementById("strength-label");

  function renderStrength(pwd) {
    if (!strengthFill) return;
    const score = evaluatePasswordStrength(pwd);
    const pct = Math.min((score / 6) * 100, 100);
    strengthFill.style.width = pwd.length ? `${pct}%` : "0%";

    let label = "";
    let color = "";
    if (pwd.length === 0) {
      label = "";
    } else if (score <= 2) {
      label = "Weak";
      color = "var(--weak)";
    } else if (score <= 3) {
      label = "Fair";
      color = "var(--fair)";
    } else if (score <= 4) {
      label = "Good";
      color = "var(--good)";
    } else {
      label = "Strong";
      color = "var(--strong)";
    }
    strengthFill.style.background = color;
    if (strengthLabel) {
      strengthLabel.textContent = label;
      strengthLabel.style.color = color;
    }
  }

  username.addEventListener("input", () => {
    if (!USERNAME_RE.test(username.value.trim())) {
      showFieldError(username, usernameError, "3-30 characters: letters, numbers, underscore only.");
    } else {
      clearFieldError(username, usernameError);
    }
  });

  email.addEventListener("input", () => {
    if (!EMAIL_RE.test(email.value.trim())) {
      showFieldError(email, emailError, "Please enter a valid email address.");
    } else {
      clearFieldError(email, emailError);
    }
  });

  password.addEventListener("input", () => {
    renderStrength(password.value);
    const missing = validatePasswordRules(password.value);
    if (missing.length) {
      showFieldError(password, passwordError, "Missing: " + missing.join(", "));
    } else {
      clearFieldError(password, passwordError);
    }
    if (confirmPassword.value) {
      confirmPassword.dispatchEvent(new Event("input"));
    }
  });

  confirmPassword.addEventListener("input", () => {
    if (confirmPassword.value !== password.value) {
      showFieldError(confirmPassword, confirmError, "Passwords do not match.");
    } else {
      clearFieldError(confirmPassword, confirmError);
    }
  });

  form.addEventListener("submit", (e) => {
    let valid = true;

    if (!USERNAME_RE.test(username.value.trim())) {
      showFieldError(username, usernameError, "3-30 characters: letters, numbers, underscore only.");
      valid = false;
    }
    if (!EMAIL_RE.test(email.value.trim())) {
      showFieldError(email, emailError, "Please enter a valid email address.");
      valid = false;
    }
    const missing = validatePasswordRules(password.value);
    if (missing.length) {
      showFieldError(password, passwordError, "Missing: " + missing.join(", "));
      valid = false;
    }
    if (confirmPassword.value !== password.value) {
      showFieldError(confirmPassword, confirmError, "Passwords do not match.");
      valid = false;
    }

    if (!valid) e.preventDefault();
  });
}
