const API_URL = '/api';

let currentUser = null;

function getCartKey(userId) {
  return `pc_store_cart_${userId}`;
}

function getCart() {
  return JSON.parse(localStorage.getItem(getCartKey(currentUser.id)) || '[]');
}

function clearCart() {
  localStorage.removeItem(getCartKey(currentUser.id));
}

function updateUserUI(user) {
  const welcomeUser = document.getElementById('welcomeUser');
  if (welcomeUser) {
    welcomeUser.textContent = `Hola, ${user.name}`;
  }

  document.getElementById('customer_name').value = user.name || '';
  document.getElementById('customer_email').value = user.email || '';
}

async function requireSession() {
  const response = await fetch(`${API_URL}/auth/session`, {
    credentials: 'include',
  });

  if (!response.ok) {
    localStorage.removeItem('pc_store_user');
    window.location.href = '/login';
    throw new Error('Usuario no autenticado');
  }

  const result = await response.json();
  currentUser = result.user;
  localStorage.setItem('pc_store_user', JSON.stringify(result.user));
  updateUserUI(result.user);
}

async function logout() {
  await fetch(`${API_URL}/auth/logout`, {
    method: 'POST',
    credentials: 'include',
  });
  localStorage.removeItem('pc_store_user');
  window.location.href = '/login';
}

function renderSummary() {
  const cart = getCart();
  const summary = document.getElementById('checkoutSummary');

  if (!cart.length) {
    summary.innerHTML = '<div class="empty">No hay productos en tu carrito.</div>';
    return;
  }

  let total = 0;
  summary.innerHTML = cart.map((item) => {
    const subtotal = item.price * item.quantity;
    total += subtotal;
    return `<p>${item.name} x${item.quantity} - $${subtotal.toFixed(2)}</p>`;
  }).join('') + `<hr><h3>Total: $${total.toFixed(2)}</h3>`;
}

document.getElementById('checkoutForm').addEventListener('submit', async (event) => {
  event.preventDefault();

  const payload = {
    customer_name: document.getElementById('customer_name').value,
    customer_email: document.getElementById('customer_email').value,
    customer_phone: document.getElementById('customer_phone').value,
    items: getCart().map((item) => ({
      product_id: item.product_id,
      quantity: item.quantity,
    })),
  };

  const response = await fetch(`${API_URL}/orders`, {
    method: 'POST',
    credentials: 'include',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload),
  });

  const result = await response.json();
  const message = document.getElementById('checkoutMessage');

  if (!response.ok) {
    message.innerHTML = `<div class="empty">${(result.errors || ['Error al procesar pedido']).join('<br>')}</div>`;
    return;
  }

  clearCart();
  message.innerHTML = `<div class="summary-box"><h3>Pedido #${result.order_id} guardado</h3><p>Total: $${result.total.toFixed(2)}</p></div>`;
  document.getElementById('customer_phone').value = '';
  renderSummary();
});

(async function init() {
  await requireSession();
  document.getElementById('logoutBtn')?.addEventListener('click', logout);
  renderSummary();
})();
