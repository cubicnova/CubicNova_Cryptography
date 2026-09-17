/**
 * common.js
 * Shared helpers used by both login.js and register.js:
 *  - togglePasswordVisibility(): show/hide password functionality
 *  - showFieldError() / clearFieldError(): inline validation messages
 */

function togglePasswordVisibility(inputId, btn) {
  const input = document.getElementById(inputId);
  if (!input) return;
  const isHidden = input.type === "password";
  input.type = isHidden ? "text" : "password";
  btn.textContent = isHidden ? "🙈" : "👁️";
  btn.setAttribute("aria-label", isHidden ? "Hide password" : "Show password");
}

function showFieldError(inputEl, errorEl, message) {
  inputEl.classList.add("is-invalid");
  inputEl.classList.remove("is-valid");
  if (errorEl) {
    errorEl.textContent = message;
    errorEl.classList.add("show");
  }
}

function clearFieldError(inputEl, errorEl) {
  inputEl.classList.remove("is-invalid");
  inputEl.classList.add("is-valid");
  if (errorEl) {
    errorEl.textContent = "";
    errorEl.classList.remove("show");
  }
}

// Wire up every [data-toggle-password] button on the page.
document.addEventListener("DOMContentLoaded", () => {
  document.querySelectorAll("[data-toggle-password]").forEach((btn) => {
    btn.addEventListener("click", () => {
      togglePasswordVisibility(btn.getAttribute("data-toggle-password"), btn);
    });
  });
});
