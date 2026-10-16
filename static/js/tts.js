/**
 * Wrapper minimalista de Web Speech API para Rhetorica+.
 *
 * Contrato HTML:
 *   <button class="tts-play"
 *           data-tts-text="Texto a leer"
 *           data-tts-lang="es-ES">Escuchar</button>
 *
 * Sin dependencias. Degrada a botón deshabilitado si el navegador no soporta.
 */
(function () {
  "use strict";

  var synth = window.speechSynthesis;
  var disponible =
    !!synth && typeof window.SpeechSynthesisUtterance === "function";

  function hablar(texto, lang) {
    if (!disponible) return false;
    synth.cancel();
    var u = new window.SpeechSynthesisUtterance(texto);
    u.lang = lang || "es-ES";
    u.rate = 0.95;
    u.pitch = 1;
    synth.speak(u);
    return true;
  }

  function manejarClick(event) {
    var boton = event.currentTarget;
    var texto = boton.getAttribute("data-tts-text") || "";
    var lang = boton.getAttribute("data-tts-lang") || "es-ES";
    if (!texto.trim()) return;

    boton.classList.add("tts-playing");
    window.setTimeout(function () {
      boton.classList.remove("tts-playing");
    }, 1500);

    hablar(texto, lang);
  }

  function init() {
    var botones = document.querySelectorAll(".tts-play");
    for (var i = 0; i < botones.length; i++) {
      var b = botones[i];
      b.addEventListener("click", manejarClick);
      if (!disponible) {
        b.disabled = true;
        b.setAttribute("title", "Tu navegador no soporta síntesis de voz");
      }
    }
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();