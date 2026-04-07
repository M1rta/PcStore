const API_URL = '/api';

let currentUser = null;

function getCartKey(userId) {
  return `pc_store_cart_${userId}`;
}

function getCart() {
  return JSON.parse(localStorage.getItem(getCartKey(currentUser.id)) || '[]');
}

function saveCart(cart) {
  localStorage.setItem(getCartKey(currentUser.id), JSON.stringify(cart));
}

function updateUserUI(user) {
  const welcomeUser = document.getElementById('welcomeUser');
  if (welcomeUser) {
    welcomeUser.textContent = `Hola, ${user.name}`;
  }
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

function removeItem(productId) {
  const cart = getCart().filter((item) => item.product_id !== productId);
  saveCart(cart);
  renderCart();
}

function changeQuantity(productId, value) {
  const cart = getCart();
  const item = cart.find((entry) => entry.product_id === productId);
  if (!item) return;

  item.quantity += value;
  if (item.quantity <= 0) {
    removeItem(productId);
    return;
  }

  saveCart(cart);
  renderCart();
}

function renderCart() {
  const container = document.getElementById('cartContainer');
  const cart = getCart();

  if (!cart.length) {
    container.innerHTML = '<div class="empty">Tu carrito esta vacio.</div>';
    return;
  }

  let total = 0;
  container.innerHTML = '';

  cart.forEach((item) => {
    const subtotal = item.price * item.quantity;
    total += subtotal;

    const article = document.createElement('article');
    article.className = 'cart-item';
    article.innerHTML = `
      <h3>${item.name}</h3>
      <p>Cantidad: ${item.quantity}</p>
      <p>Precio: $${item.price.toFixed(2)}</p>
      <p>Subtotal: $${subtotal.toFixed(2)}</p>
      <button class="btn" onclick="changeQuantity(${item.product_id}, 1)">+</button>
      <button class="btn" onclick="changeQuantity(${item.product_id}, -1)">-</button>
      <button class="btn" onclick="removeItem(${item.product_id})">Eliminar</button>
    `;
    container.appendChild(article);
  });

  const totalBox = document.createElement('div');
  totalBox.className = 'summary-box';
  totalBox.innerHTML = `<h3>Total: $${total.toFixed(2)}</h3>`;
  container.appendChild(totalBox);
}

window.removeItem = removeItem;
window.changeQuantity = changeQuantity;

(async function init() {
  await requireSession();
  document.getElementById('logoutBtn')?.addEventListener('click', logout);
  renderCart();
})();
