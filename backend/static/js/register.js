const API = '/api';

function storeUser(user) {
  localStorage.setItem('pc_store_user', JSON.stringify(user));
}

document.getElementById('register-form')?.addEventListener('submit', async (event) => {
  event.preventDefault();

  const name = document.getElementById('register-name').value.trim();
  const email = document.getElementById('register-email').value.trim();
  const password = document.getElementById('register-password').value.trim();
  const passwordConfirm = document.getElementById('register-password2').value.trim();

  if (!name || !email || !password || !passwordConfirm) {
    alert('Completa todos los campos.');
    return;
  }

  if (password !== passwordConfirm) {
    alert('Las contrasenas no coinciden.');
    return;
  }

  if (password.length < 6) {
    alert('La contrasena debe tener al menos 6 caracteres.');
    return;
  }

  try {
    const response = await fetch(`${API}/auth/register`, {
      method: 'POST',
      credentials: 'include',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ name, email, password }),
    });

    const result = await response.json().catch(() => ({}));

    if (!response.ok) {
      alert(result.error || 'No se pudo crear la cuenta.');
      return;
    }

    storeUser(result.user);
    alert('Cuenta creada correctamente. Ya puedes empezar a comprar.');
    window.location.href = '/index';
  } catch (error) {
    console.error(error);
    alert('Error conectando con el servidor.');
  }
});
