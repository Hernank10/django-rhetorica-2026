/* Módulo 10: sintaxis — evaluación AJAX de ejercicios */
(function() {
  "use strict";

  function getCsrf() {
    const m = document.cookie.match(/csrftoken=([^;]+)/);
    return m ? m[1] : "";
  }

  function leerRespuesta(card, tipo) {
    if (tipo === 1) {
      const radio = card.querySelector('input[type=radio]:checked');
      const just = card.querySelector('.justificacion');
      if (!radio) return null;
      return {
        opcion_id: radio.value,
        justificacion: just ? just.value : "",
      };
    }
    if (tipo === 2 || tipo === 4) {
      const input = card.querySelector('.respuesta-texto');
      return input ? { texto: input.value } : null;
    }
    if (tipo === 3) {
      const selects = card.querySelectorAll('.select-categoria');
      const clasificacion = Array.from(selects).map(s => s.value);
      if (clasificacion.some(v => !v)) return null;
      return { clasificacion };
    }
    if (tipo === 5) {
      const err = card.querySelector('.respuesta-error');
      const regla = card.querySelector('.select-regla');
      if (!err || !regla || !regla.value) return null;
      // Para tipo 5 el motor espera posicion + regla. Usamos error_texto como
      // posicion simplificada: enviamos error_texto y el motor lo compara con
      // el esperado. Si el motor usa posicion numerica, fallback a null.
      return {
        error_texto: err.value,
        regla: regla.value,
        posicion: null, // el motor de prueba usa posicion; ajustar si es necesario
      };
    }
    return null;
  }

  function renderFeedback(container, data) {
    container.style.display = "block";
    if (data.ok) {
      container.className = "feedback mt-3 alert alert-success";
      container.innerHTML = '<i class="fas fa-check-circle"></i> <strong>' +
        data.feedback + '</strong>' +
        (data.regla ? '<br><small>Regla: ' + data.regla + '</small>' : '');
    } else {
      container.className = "feedback mt-3 alert alert-danger";
      container.innerHTML = '<i class="fas fa-times-circle"></i> <strong>' +
        data.feedback + '</strong>' +
        (data.ejemplo_correcto ? '<br><small>Ejemplo correcto: <em>' +
          data.ejemplo_correcto + '</em></small>' : '');
    }
  }

  document.querySelectorAll('.ejercicio-card').forEach(card => {
    const btn = card.querySelector('.btn-evaluar');
    const fb = card.querySelector('.feedback');
    const ejId = card.dataset.ejercicioId;
    const tipo = parseInt(card.dataset.tipo, 10);

    btn.addEventListener('click', () => {
      const respuesta = leerRespuesta(card, tipo);
      if (!respuesta) {
        renderFeedback(fb, {
          ok: false,
          feedback: "Completa todos los campos antes de evaluar",
        });
        return;
      }

      btn.disabled = true;
      btn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Evaluando...';

      fetch('/gramatica/evaluar/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': getCsrf(),
        },
        body: JSON.stringify({
          ejercicio_id: ejId,
          respuesta: respuesta,
        }),
      })
        .then(r => r.json())
        .then(data => {
          renderFeedback(fb, data);
          btn.disabled = false;
          btn.innerHTML = '<i class="fas fa-redo"></i> Reintentar';
        })
        .catch(err => {
          renderFeedback(fb, {
            ok: false,
            feedback: "Error de red: " + err,
          });
          btn.disabled = false;
          btn.innerHTML = '<i class="fas fa-check"></i> Evaluar';
        });
    });
  });
})();
/* --- Badge navbar: dominadas count --- */
(function() {
  "use strict";
  const badge = document.getElementById("gramatica-badge");
  if (!badge) return;

  function fetchBadge() {
    fetch("/gramatica/ajax/contador/")
      .then(r => r.json())
      .then(d => {
        if (d.dominadas > 0) {
          badge.textContent = d.dominadas;
          badge.style.display = "";
        } else {
          badge.style.display = "none";
        }
      })
      .catch(() => {});
  }

  fetchBadge();
  setInterval(fetchBadge, 60000);
})();
