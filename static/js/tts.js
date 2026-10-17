/**
 * Wrapper TTS para Rhetorica+.
 *
 * 1. Si el navegador soporta Web Speech API → usa speechSynthesis (offline, instantaneo).
 * 2. Si NO → fallback a /tts/?text=...&lang=... (gTTS server-side, cacheado en disco).
 *
 * Contrato HTML:
 *   <button class="tts-play"
 *           data-tts-text="Texto a leer"
 *           data-tts-lang="es-ES">Escuchar</button>
 */
(function () {
  "use strict";

  var TTS_URL = "/tts/";
  var synth = window.speechSynthesis;
  var webSpeechOK =
    !!synth && typeof window.SpeechSynthesisUtterance === "function";
  var audioActual = null;

  function langParaGtts(lang) {
    // "es-ES" -> "es", "en-US" -> "en". gTTS no soporta latin -> cae a es.
    var l = (lang || "es").toLowerCase().split("-")[0];
    if (l === "en" || l === "es") return l;
    return "es";
  }

  function hablarWebSpeech(texto, lang) {
    synth.cancel();
    var u = new window.SpeechSynthesisUtterance(texto);
    u.lang = lang || "es-ES";
    u.rate = 0.95;
    u.pitch = 1;
    synth.speak(u);
  }

  function hablarGtts(boton, texto, lang) {
    if (audioActual) {
      audioActual.pause();
      audioActual = null;
    }
    var url =
      TTS_URL +
      "?text=" +
      encodeURIComponent(texto) +
      "&lang=" +
      langParaGtts(lang);

    var audio = new Audio(url);
    audioActual = audio;

    boton.classList.add("tts-playing");

    audio.addEventListener("ended", function () {
      boton.classList.remove("tts-playing");
      audioActual = null;
    });
    audio.addEventListener("error", function () {
      boton.classList.remove("tts-playing");
      audioActual = null;
    });

    audio.play().catch(function () {
      boton.classList.remove("tts-playing");
      audioActual = null;
    });
  }

  function manejarClick(event) {
    var boton = event.currentTarget;
    var texto = boton.getAttribute("data-tts-text") || "";
    var lang = boton.getAttribute("data-tts-lang") || "es-ES";
    if (!texto.trim()) return;

    if (webSpeechOK) {
      boton.classList.add("tts-playing");
      window.setTimeout(function () {
        boton.classList.remove("tts-playing");
      }, 1500);
      hablarWebSpeech(texto, lang);
    } else {
      hablarGtts(boton, texto, lang);
    }
  }

  function init() {
    var botones = document.querySelectorAll(".tts-play");
    for (var i = 0; i < botones.length; i++) {
      botones[i].addEventListener("click", manejarClick);
    }
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();