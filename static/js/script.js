function togglePassword() {
  const passwordInput = document.getElementById('password');
  const toggleIcon = document.getElementById('toggle-icon');

  if (passwordInput.type === 'password') {
    passwordInput.type = 'text';
    toggleIcon.classList.remove('bi-eye-fill');
    toggleIcon.classList.add('bi-eye-slash-fill');
  } else {
    passwordInput.type = 'password';
    toggleIcon.classList.remove('bi-eye-slash-fill');
    toggleIcon.classList.add('bi-eye-fill');
  }
}

function getCsrfToken() {
    return document.querySelector('input[name="csrf_token"]').value;
}

document.querySelector(".password-toggle-btn").addEventListener("click", function() {
    togglePassword();
});