(() => {
  const toastRoot = document.getElementById('toasts');
  const showToast = (message) => {
    if (!toastRoot) return;
    const item = document.createElement('div');
    item.className = 'kawaii-toast';
    item.setAttribute('role', 'status');
    item.textContent = `💖 ${message}`;
    toastRoot.appendChild(item);
    window.setTimeout(() => {
      item.classList.add('out');
      window.setTimeout(() => item.remove(), 240);
    }, 2600);
  };

  document.addEventListener('submit', async (event) => {
    const form = event.target;
    if (!(form instanceof HTMLFormElement) || !form.matches('[data-ajax-cart]')) return;
    event.preventDefault();
    const button = form.querySelector('button[type="submit"]');
    if (button) button.disabled = true;
    try {
      const response = await fetch(form.action, {
        method: 'POST', body: new FormData(form),
        headers: { 'X-Requested-With': 'fetch' }, credentials: 'same-origin'
      });
      if (!response.ok) throw new Error('Request failed');
      const result = await response.json();
      document.querySelectorAll('[data-cart-badge]').forEach((badge) => {
        badge.textContent = String(result.count || 0);
        badge.hidden = !result.count;
      });
      showToast(`«${result.name}» добавлен в предзаказ`);
    } catch (_) {
      showToast('Не удалось добавить товар. Попробуйте ещё раз.');
    } finally {
      if (button) button.disabled = false;
    }
  });
})();
