const API_URL = '/api';

function getStoredUser() {
  return JSON.parse(localStorage.getItem('pc_store_user') || 'null');
}

function getCartKey(userId) {
  return `pc_store_cart_${userId}`;
}

function getCart(userId) {
  return JSON.parse(localStorage.getItem(getCartKey(userId)) || '[]');
}

function saveCart(userId, cart) {
  localStorage.setItem(getCartKey(userId), JSON.stringify(cart));
}

function updateUserUI(user) {
  const welcomeUser = document.getElementById('welcomeUser');
  if (welcomeUser) {
    welcomeUser.textContent = `Bienvenido, ${user.name}`;
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
  localStorage.setItem('pc_store_user', JSON.stringify(result.user));
  updateUserUI(result.user);
  return result.user;
}

async function logout() {
  await fetch(`${API_URL}/auth/logout`, {
    method: 'POST',
    credentials: 'include',
  });
  localStorage.removeItem('pc_store_user');
  window.location.href = '/login';
}

async function loadCategories() {
  const response = await fetch(`${API_URL}/categories`, {
    credentials: 'include',
  });
  const result = await response.json();
  const select = document.getElementById('categorySelect');

  result.data.forEach((category) => {
    const option = document.createElement('option');
    option.value = category.id;
    option.textContent = category.name;
    select.appendChild(option);
  });
}

function addToCart(user, product) {
  const cart = getCart(user.id);
  const existing = cart.find((item) => item.product_id === product.id);

  if (existing) {
    existing.quantity += 1;
  } else {
    cart.push({
      product_id: product.id,
      name: product.name,
      price: product.price,
      quantity: 1,
    });
  }

  saveCart(user.id, cart);
  alert('Producto agregado a tu carrito.');
}

function renderProducts(products, user) {
  const grid = document.getElementById('productGrid');
  grid.innerHTML = '';

  if (!products.length) {
    grid.innerHTML = '<div class="empty">No hay productos para esta categoria.</div>';
    return;
  }

  products.forEach((product) => {
    const card = document.createElement('article');
    card.className = 'product-card';
    card.innerHTML = `
      <img src="${product.image}" alt="${product.name}">
      <div class="content">
        <p class="small">${product.category}</p>
        <h3>
          <a href="${product.product_url}" target="_blank" rel="noopener noreferrer">
            ${product.name}
          </a>
        </h3>
        <p>${product.description}</p>
        <div class="price">$${product.price.toFixed(2)}</div>
        <button class="btn" data-id="${product.id}">Agregar al carrito</button>
      </div>
    `;
    grid.appendChild(card);
  });

  document.querySelectorAll('[data-id]').forEach((button) => {
    button.addEventListener('click', () => {
      const product = products.find((item) => item.id === Number(button.dataset.id));
      addToCart(user, product);
    });
  });
}

async function loadProducts(user, categoryId = '') {
  const url = categoryId ? `${API_URL}/products?category_id=${categoryId}` : `${API_URL}/products`;
  const response = await fetch(url, {
    credentials: 'include',
  });
  const result = await response.json();
  renderProducts(result.data, user);
}

(async function init() {
  const user = await requireSession();
  document.getElementById('logoutBtn')?.addEventListener('click', logout);
  await loadCategories();
  await loadProducts(user);

  document.getElementById('categorySelect').addEventListener('change', (event) => {
    loadProducts(user, event.target.value);
  });
})();
