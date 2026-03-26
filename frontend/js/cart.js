function getCart() {
  return JSON.parse(localStorage.getItem('pc_store_cart') || '[]');
}

function saveCart(cart) {
  localStorage.setItem('pc_store_cart', JSON.stringify(cart));
}

function removeItem(productId) {
  const cart = getCart().filter(item => item.product_id !== productId);
  saveCart(cart);
  renderCart();
}

function changeQuantity(productId, value) {
  const cart = getCart();
  const item = cart.find(entry => entry.product_id === productId);
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
    container.innerHTML = '<div class="empty">Tu carrito está vacío.</div>';
    return;
  }

  let total = 0;
  container.innerHTML = '';

  cart.forEach(item => {
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

renderCart();
