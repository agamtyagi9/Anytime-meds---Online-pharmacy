const cart = JSON.parse(localStorage.getItem('cart')||'[]');
function addToCart(pid, name, price){
  const idx = cart.findIndex(c=>c.product_id===pid);
  if(idx>-1) cart[idx].qty += 1; else cart.push({product_id: pid, name, price, qty:1});
  localStorage.setItem('cart', JSON.stringify(cart));
  alert('Added to cart');
}
async function checkout(user_id){
  const items = cart.map(c=>({product_id:c.product_id, qty:c.qty}));
  const res = await fetch('/api/cart/checkout',{
    method:'POST',headers:{'Content-Type':'application/json'},
    body: JSON.stringify({user_id, items})
  });
  const data = await res.json();
  localStorage.removeItem('cart');
  alert('Order placed: ' + data.order_id);
}
