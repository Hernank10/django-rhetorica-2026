# -*- coding: utf-8 -*-
"""Rellena los .po con polib (maneja msgid multi-linea)."""
from pathlib import Path
import polib

BASE = Path(r"E:\02_proyectos\django-rhetorica")
PO_DIR = BASE / "locale"

T = {
  "es": {
    "Iniciar Sesión": "Iniciar Sesión",
    "Registrarse": "Registrarse",
    "Aprende y practica retórica con ejercicios interactivos y cursos diseñados para mejorar tus habilidades comunicativas.":
      "Aprende y practica retórica con ejercicios interactivos y cursos diseñados para mejorar tus habilidades comunicativas.",
    "Plataforma de aprendizaje retórico basada en IA":
      "Plataforma de aprendizaje retórico basada en IA",
    "Accede a todos los cursos y ejercicios":
      "Accede a todos los cursos y ejercicios",
  },
  "en": {
    "Iniciar Sesión": "Sign In",
    "Registrarse": "Sign Up",
    "Aprende y practica retórica con ejercicios interactivos y cursos diseñados para mejorar tus habilidades comunicativas.":
      "Learn and practice rhetoric with interactive exercises and courses designed to improve your communication skills.",
    "Plataforma de aprendizaje retórico basada en IA":
      "AI-powered rhetoric learning platform",
    "Accede a todos los cursos y ejercicios":
      "Access all courses and exercises",
  },
  "pt": {
    "Iniciar Sesión": "Entrar",
    "Registrarse": "Registar",
    "Aprende y practica retórica con ejercicios interactivos y cursos diseñados para mejorar tus habilidades comunicativas.":
      "Aprenda e pratique retórica com exercícios interativos e cursos concebidos para melhorar as suas habilidades de comunicação.",
    "Plataforma de aprendizaje retórico basada en IA":
      "Plataforma de aprendizagem retórica baseada em IA",
    "Accede a todos los cursos y ejercicios":
      "Acesse todos os cursos e exercícios",
  },
  "fr": {
    "Iniciar Sesión": "Se connecter",
    "Registrarse": "S'inscrire",
    "Aprende y practica retórica con ejercicios interactivos y cursos diseñados para mejorar tus habilidades comunicativas.":
      "Apprenez et pratiquez la rhétorique avec des exercices interactifs et des cours conçus pour améliorer vos compétences en communication.",
    "Plataforma de aprendizaje retórico basada en IA":
      "Plateforme d'apprentissage de la rhétorique basée sur l'IA",
    "Accede a todos los cursos y ejercicios":
      "Accédez à tous les cours et exercices",
  },
  "de": {
    "Iniciar Sesión": "Anmelden",
    "Registrarse": "Registrieren",
    "Aprende y practica retórica con ejercicios interactivos y cursos diseñados para mejorar tus habilidades comunicativas.":
      "Lernen und üben Sie Rhetorik mit interaktiven Übungen und Kursen, die Ihre Kommunikationsfähigkeiten verbessern.",
    "Plataforma de aprendizaje retórico basada en IA":
      "KI-gestützte Rhetorik-Lernplattform",
    "Accede a todos los cursos y ejercicios":
      "Zugriff auf alle Kurse und Übungen",
  },
  "it": {
    "Iniciar Sesión": "Accedi",
    "Registrarse": "Registrati",
    "Aprende y practica retórica con ejercicios interactivos y cursos diseñados para mejorar tus habilidades comunicativas.":
      "Impara e pratica la retorica con esercizi interattivi e corsi progettati per migliorare le tue capacità comunicative.",
    "Plataforma de aprendizaje retórico basada en IA":
      "Piattaforma di apprendimento retorico basata sull'IA",
    "Accede a todos los cursos y ejercicios":
      "Accedi a tutti i corsi ed esercizi",
  },
  "ca": {
    "Iniciar Sesión": "Inicia sessió",
    "Registrarse": "Registra't",
    "Aprende y practica retórica con ejercicios interactivos y cursos diseñados para mejorar tus habilidades comunicativas.":
      "Aprèn i practica retòrica amb exercicis interactius i cursos dissenyats per millorar les teves habilitats comunicatives.",
    "Plataforma de aprendizaje retórico basada en IA":
      "Plataforma d'aprenentatge retòric basada en IA",
    "Accede a todos los cursos y ejercicios":
      "Accedeix a tots els cursos i exercicis",
  },
  "gl": {
    "Iniciar Sesión": "Iniciar sesión",
    "Registrarse": "Rexistrarse",
    "Aprende y practica retórica con ejercicios interactivos y cursos diseñados para mejorar tus habilidades comunicativas.":
      "Aprende e practica retórica con exercicios interactivos e cursos deseñados para mellorar as túas habilidades comunicativas.",
    "Plataforma de aprendizaje retórico basada en IA":
      "Plataforma de aprendizaxe retórica baseada en IA",
    "Accede a todos los cursos y ejercicios":
      "Accede a todos os cursos e exercicios",
  },
  "eu": {
    "Iniciar Sesión": "Hasi saioa",
    "Registrarse": "Eman izena",
    "Aprende y practica retórica con ejercicios interactivos y cursos diseñados para mejorar tus habilidades comunicativas.":
      "Ikasi eta praktikatu erretorika ariketa interaktiboen eta zure komunikazio-trebetasunak hobetzeko diseinatutako ikastaroen bidez.",
    "Plataforma de aprendizaje retórico basada en IA":
      "AAan oinarritutako erretorika ikaskuntza-plataforma",
    "Accede a todos los cursos y ejercicios":
      "Ikastaro eta ariketa guztietara sartu",
  },
  "zh_Hans": {
    "Iniciar Sesión": "登录",
    "Registrarse": "注册",
    "Aprende y practica retórica con ejercicios interactivos y cursos diseñados para mejorar tus habilidades comunicativas.":
      "通过互动练习和专为提升沟通技巧而设计的课程，学习和练习修辞学。",
    "Plataforma de aprendizaje retórico basada en IA":
      "基于人工智能的修辞学习平台",
    "Accede a todos los cursos y ejercicios":
      "访问所有课程和练习",
  },
  "ja": {
    "Iniciar Sesión": "ログイン",
    "Registrarse": "新規登録",
    "Aprende y practica retórica con ejercicios interactivos y cursos diseñados para mejorar tus habilidades comunicativas.":
      "インタラクティブな演習と、コミュニケーション能力を高めるために設計されたコースで、修辞学を学び、実践しましょう。",
    "Plataforma de aprendizaje retórico basada en IA":
      "AIを活用した修辞学学習プラットフォーム",
    "Accede a todos los cursos y ejercicios":
      "すべてのコースと演習にアクセス",
  },
  "ko": {
    "Iniciar Sesión": "로그인",
    "Registrarse": "회원가입",
    "Aprende y practica retórica con ejercicios interactivos y cursos diseñados para mejorar tus habilidades comunicativas.":
      "대화형 연습과 의사소통 능력을 향상시키기 위해 설계된 코스로 수사학을 배우고 연습하세요.",
    "Plataforma de aprendizaje retórico basada en IA":
      "AI 기반 수사학 학습 플랫폼",
    "Accede a todos los cursos y ejercicios":
      "모든 코스와 연습에 액세스",
  },
  "ar": {
    "Iniciar Sesión": "تسجيل الدخول",
    "Registrarse": "التسجيل",
    "Aprende y practica retórica con ejercicios interactivos y cursos diseñados para mejorar tus habilidades comunicativas.":
      "تعلم وتدرب على البلاغة من خلال تمارين تفاعلية ودورات مصممة لتحسين مهاراتك التواصلية.",
    "Plataforma de aprendizaje retórico basada en IA":
      "منصة تعلم البلاغة المدعومة بالذكاء الاصطناعي",
    "Accede a todos los cursos y ejercicios":
      "الوصول إلى جميع الدورات والتمارين",
  },
  "ru": {
    "Iniciar Sesión": "Войти",
    "Registrarse": "Регистрация",
    "Aprende y practica retórica con ejercicios interactivos y cursos diseñados para mejorar tus habilidades comunicativas.":
      "Изучайте и практикуйте риторику с интерактивными упражнениями и курсами, разработанными для улучшения ваших коммуникативных навыков.",
    "Plataforma de aprendizaje retórico basada en IA":
      "Платформа изучения риторики на основе ИИ",
    "Accede a todos los cursos y ejercicios":
      "Доступ ко всем курсам и упражнениям",
  },
  "hi": {
    "Iniciar Sesión": "साइन इन करें",
    "Registrarse": "साइन अप करें",
    "Aprende y practica retórica con ejercicios interactivos y cursos diseñados para mejorar tus habilidades comunicativas.":
      "इंटरैक्टिव अभ्यासों और आपके संचार कौशल को बेहतर बनाने के लिए डिज़ाइन किए गए पाठ्यक्रमों के साथ अलंकारिकता सीखें और अभ्यास करें।",
    "Plataforma de aprendizaje retórico basada en IA":
      "एआई-आधारित अलंकारिकता सीखने का मंच",
    "Accede a todos los cursos y ejercicios":
      "सभी पाठ्यक्रमों और अभ्यासों तक पहुंचें",
  },
  "tr": {
    "Iniciar Sesión": "Giriş Yap",
    "Registrarse": "Kayıt Ol",
    "Aprende y practica retórica con ejercicios interactivos y cursos diseñados para mejorar tus habilidades comunicativas.":
      "Etkileşimli alıştırmalar ve iletişim becerilerinizi geliştirmek için tasarlanmış kurslarla retoriği öğrenin ve pratik yapın.",
    "Plataforma de aprendizaje retórico basada en IA":
      "Yapay zeka destekli retorik öğrenme platformu",
    "Accede a todos los cursos y ejercicios":
      "Tüm kurslara ve alıştırmalara erişin",
  },
}

for lang, mapping in T.items():
    po_path = PO_DIR / lang / "LC_MESSAGES" / "django.po"
    if not po_path.exists():
        print(f"[!] No existe {po_path}")
        continue
    po = polib.pofile(str(po_path))
    n_ok = 0
    n_miss = 0
    for entry in po:
        if entry.msgid in mapping:
            entry.msgstr = mapping[entry.msgid]
            n_ok += 1
        elif entry.msgid and entry.msgid not in mapping:
            pass
    # detectar faltantes
    for msgid in mapping:
        if not any(e.msgid == msgid for e in po):
            n_miss += 1
            print(f"[!] {lang}: no encontrado -> {msgid[:50]}...")
    po.save(str(po_path))
    print(f"[OK] {lang}: {n_ok} traducidos, {n_miss} faltantes")

print("\n[FIN] Ahora ejecuta:  python manage.py compilemessages")