const API_URL = 'http://127.0.0.1:5000/api';

async function loadCategories() {
  const response = await fetch(`${API_URL}/categories`);
  const result = await response.json();
  const select = document.getElementById('categorySelect');

  result.data.forEach(category => {
    const option = document.createElement('option');
    option.value = category.id;
    option.textContent = category.name;
    select.appendChild(option);
  });
}

function getCart() {
  return JSON.parse(localStorage.getItem('pc_store_cart') || '[]');
}

function saveCart(cart) {
  localStorage.setItem('pc_store_cart', JSON.stringify(cart));
}

function addToCart(product) {
  const cart = getCart();
  const existing = cart.find(item => item.product_id === product.id);

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

  saveCart(cart);
  alert('Producto agregado al carrito');
}

function renderProducts(products) {
  const grid = document.getElementById('productGrid');
  grid.innerHTML = '';

  if (!products.length) {
    grid.innerHTML = '<div class="empty">No hay productos para esta categoría.</div>';
    return;
  }

  products.forEach(product => {
    const card = document.createElement('article');
    card.className = 'product-card';
    card.innerHTML = `
      <img src="${product.image}" alt="${product.name}">
      <div class="content">
        <p class="small">${product.category}</p>
        <h3>${product.name}</h3>
        <p>${product.description}</p>
        <div class="price">$${product.price.toFixed(2)}</div>
        <button class="btn" data-id="${product.id}">Agregar al carrito</button>
      </div>
    `;
    grid.appendChild(card);
  });

  document.querySelectorAll('[data-id]').forEach(button => {
    button.addEventListener('click', () => {
      const product = products.find(p => p.id === Number(button.dataset.id));
      addToCart(product);
    });
  });
}

async function loadProducts(categoryId = '') {
  const url = categoryId ? `${API_URL}/products?category_id=${categoryId}` : `${API_URL}/products`;
  const response = await fetch(url);
  const result = await response.json();
  renderProducts(result.data);
}

(async function init() {
  await loadCategories();
  await loadProducts();

  document.getElementById('categorySelect').addEventListener('change', (e) => {
    loadProducts(e.target.value);
  });
})();
