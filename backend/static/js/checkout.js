const API_URL = 'http://127.0.0.1:5000/api';

function getCart() {
  return JSON.parse(localStorage.getItem('pc_store_cart') || '[]');
}

function renderSummary() {
  const cart = getCart();
  const summary = document.getElementById('checkoutSummary');

  if (!cart.length) {
    summary.innerHTML = '<div class="empty">No hay productos en el carrito.</div>';
    return;
  }

  let total = 0;
  summary.innerHTML = cart.map(item => {
    const subtotal = item.price * item.quantity;
    total += subtotal;
    return `<p>${item.name} x${item.quantity} - $${subtotal.toFixed(2)}</p>`;
  }).join('') + `<hr><h3>Total: $${total.toFixed(2)}</h3>`;
}

document.getElementById('checkoutForm').addEventListener('submit', async (e) => {
  e.preventDefault();

  const payload = {
    customer_name: document.getElementById('customer_name').value,
    customer_email: document.getElementById('customer_email').value,
    customer_phone: document.getElementById('customer_phone').value,
    items: getCart().map(item => ({
      product_id: item.product_id,
      quantity: item.quantity,
    })),
  };

  const response = await fetch(`${API_URL}/orders`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload),
  });

  const result = await response.json();
  const message = document.getElementById('checkoutMessage');

  if (!response.ok) {
    message.innerHTML = `<div class="empty">${(result.errors || ['Error al procesar pedido']).join('<br>')}</div>`;
    return;
  }

  localStorage.removeItem('pc_store_cart');
  message.innerHTML = `<div class="summary-box"><h3>Pedido #${result.order_id} guardado</h3><p>Total: $${result.total.toFixed(2)}</p></div>`;
  document.getElementById('checkoutForm').reset();
  renderSummary();
});

renderSummary();
