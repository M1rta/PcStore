const API = '/api';

function storeUser(user) {
  localStorage.setItem('pc_store_user', JSON.stringify(user));
}

async function loadSession() {
  try {
    const response = await fetch(`${API}/auth/session`, {
      credentials: 'include',
    });

    if (!response.ok) {
      return;
    }

    const result = await response.json();
    if (result.user) {
      storeUser(result.user);
      window.location.href = '/index';
    }
  } catch (error) {
    console.error(error);
  }
}

loadSession();

document.getElementById('login-form')?.addEventListener('submit', async (event) => {
  event.preventDefault();

  const email = document.getElementById('email').value.trim();
  const password = document.getElementById('password').value;

  if (!email || !password) {
    alert('Completa todos los campos.');
    return;
  }

  try {
    const response = await fetch(`${API}/auth/login`, {
      method: 'POST',
      credentials: 'include',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email, password }),
    });

    const result = await response.json().catch(() => ({}));

    if (!response.ok) {
      alert(result.error || 'No se pudo iniciar sesion.');
      return;
    }

    storeUser(result.user);
    window.location.href = '/index';
  } catch (error) {
    console.error(error);
    alert('Error conectando con el servidor.');
  }
});
