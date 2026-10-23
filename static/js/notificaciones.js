/* Campana de notificaciones: contador + dropdown + marcar leídas */
(function() {
  "use strict";
  const bell = document.getElementById('notif-bell');
  const badge = document.getElementById('notif-badge');
  const menu = document.getElementById('notif-menu');
  if (!bell || !badge || !menu) return;

  function getCsrf() {
    const m = document.cookie.match(/csrftoken=([^;]+)/);
    return m ? m[1] : '';
  }

  function updateBadge(count) {
    if (count > 0) {
      badge.textContent = count > 99 ? '99+' : String(count);
      badge.style.display = '';
    } else {
      badge.style.display = 'none';
    }
  }

  function fetchContador() {
    fetch('/notificaciones/ajax/contador/')
      .then(r => r.json())
      .then(d => updateBadge(d.count || 0))
      .catch(() => {});
  }

  function renderMenu(data) {
    const items = data.notificaciones || [];
    if (items.length === 0) {
      menu.innerHTML = '<li><span class="dropdown-item text-muted">Sin notificaciones</span></li>';
      return;
    }
    let html = '';
    items.forEach(n => {
      const unread = !n.leida ? 'bg-light fw-bold' : '';
      const href = n.url_destino || '#';
      html += '<li><a class="dropdown-item ' + unread + '" href="' + href + '" data-notif-id="' + n.id + '">';
      html += '<i class="fas fa-' + (n.icono || 'bell') + ' me-2 text-primary"></i>';
      html += '<span class="small">' + n.titulo + '</span>';
      html += '</a></li>';
    });
    html += '<li><hr class="dropdown-divider"></li>';
    html += '<li><a class="dropdown-item text-center small" href="/notificaciones/">Ver todas</a></li>';
    menu.innerHTML = html;

    menu.querySelectorAll('a[data-notif-id]').forEach(a => {
      a.addEventListener('click', function() {
        const id = this.dataset.notifId;
        fetch('/notificaciones/ajax/marcar/' + id + '/', {
          method: 'POST',
          headers: {'X-CSRFToken': getCsrf()},
        }).then(() => fetchContador()).catch(() => {});
      });
    });
  }

  function fetchUltimas() {
    fetch('/notificaciones/ajax/ultimas/')
      .then(r => r.json())
      .then(d => {
        updateBadge(d.count || 0);
        renderMenu(d);
      })
      .catch(() => {});
  }

  fetchContador();
  setInterval(fetchContador, 60000);

  bell.addEventListener('click', function() { fetchUltimas(); });
})();