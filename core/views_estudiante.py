"""
Panel del Estudiante: dashboard personal, cursos, evaluaciones,
logros, certificados, estadísticas y ranking.
"""
from datetime import timedelta

from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.db.models import Avg, Count, Q, Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from .models import (
    Certificacion,
    CertificacionObtenida,
    Logro,
    LogroObtenido,
    Respuesta,
)
from .models_cursos import (
    Curso,
    EvaluacionCurso,
    Leccion,
    Modulo,
    PreguntaEvaluacion,
    ProgresoUsuario,
    ResultadoEvaluacionCurso,
)

User = get_user_model()


def _get_user(request):
    return request.user


# ============================================================
# DASHBOARD PRINCIPAL
# ============================================================
def _mcer_progreso(user):
    """Devuelve el progreso MCER (A1-C2) del estudiante.

    Returns:
        dict: {
            "niveles": {"A1": {"total": 100, "dominadas": 0, "pct": 0}, ...},
            "total_mcer": int,       # t?cnicas MCER totales (610)
            "dominadas_mcer": int,   # t?cnicas MCER dominadas por el user
            "pct_mcer": int,         # porcentaje redondeado
        }
    """
    from core.models_gramatica import TecnicaGramatical, ProgresoGramatical

    modulos = ["a1", "a2", "b1", "b2", "c1", "c2"]
    niveles = {}
    total_mcer = 0
    dominadas_mcer = 0

    for mod in modulos:
        qs = TecnicaGramatical.objects.filter(modulo=mod)
        total = qs.count()
        dominadas = ProgresoGramatical.objects.filter(
            usuario=user, tecnica__in=qs, estado="dominada"
        ).count()
        pct = round(100 * dominadas / total) if total else 0
        niveles[mod.upper()] = {"total": total, "dominadas": dominadas, "pct": pct}
        total_mcer += total
        dominadas_mcer += dominadas

    pct_mcer = round(100 * dominadas_mcer / total_mcer) if total_mcer else 0
    return {
        "niveles": niveles,
        "total_mcer": total_mcer,
        "dominadas_mcer": dominadas_mcer,
        "pct_mcer": pct_mcer,
    }

@login_required
def dashboard(request):
    u = _get_user(request)

    # KPIs
    cursos_activos = ProgresoUsuario.objects.filter(
        usuario=u
    ).values("leccion__modulo__curso").distinct().count()

    lecciones_completadas = ProgresoUsuario.objects.filter(
        usuario=u, completado=True
    ).count()

    certificados = CertificacionObtenida.objects.filter(user=u).count()
    logros = LogroObtenido.objects.filter(user=u).count()

    total_resp = Respuesta.objects.filter(user=u).count()
    correctas = Respuesta.objects.filter(user=u, es_correcta=True).count()
    tasa = round((correctas / total_resp) * 100, 1) if total_resp else 0

    # Progreso por curso (para gráfico de barras)
    cursos_progreso = []
    cursos_ids = ProgresoUsuario.objects.filter(usuario=u).values_list(
        "leccion__modulo__curso_id", flat=True
    ).distinct()
    for cid in cursos_ids:
        curso = Curso.objects.filter(id=cid).first()
        if not curso:
            continue
        total = Leccion.objects.filter(modulo__curso=curso).count()
        completadas = ProgresoUsuario.objects.filter(
            usuario=u, leccion__modulo__curso=curso, completado=True
        ).count()
        pct = round((completadas / total) * 100, 1) if total else 0
        cursos_progreso.append({
            "curso": curso,
            "completadas": completadas,
            "total": total,
            "pct": pct,
    })
    cursos_progreso.sort(key=lambda x: x["pct"], reverse=True)
    cursos_progreso = cursos_progreso[:8]

    # Actividad últimos 30 días
    hoy = timezone.now()
    actividad = []
    for i in range(30):
        dia = hoy - timedelta(days=29 - i)
        inicio = dia.replace(hour=0, minute=0, second=0, microsecond=0)
        fin = inicio + timedelta(days=1)
        n = ProgresoUsuario.objects.filter(
            usuario=u, completado=True,
            completado_en__gte=inicio, completado_en__lt=fin
        ).count()
        actividad.append({"dia": inicio.strftime("%d/%m"), "count": n})

    # Aciertos por tipo de ejercicio
    aciertos_por_tipo = (
        Respuesta.objects.filter(user=u)
        .values("tipo_ejercicio")
        .annotate(
            total=Count("id"),
            correctas=Count("id", filter=Q(es_correcta=True)),
        )
        .order_by("-total")[:6]
    )
    aciertos_data = [
        {"tipo": a["tipo_ejercicio"], "correctas": a["correctas"], "total": a["total"]}
        for a in aciertos_por_tipo
    ]

    # Últimos logros
    ultimos_logros = LogroObtenido.objects.filter(user=u).select_related(
        "logro"
    ).order_by("-fecha_obtenida")[:5]

    # Últimos certificados
    ultimos_certs = CertificacionObtenida.objects.filter(user=u).select_related(
        "certificacion"
    ).order_by("-fecha_obtenida")[:3]

    # Próximas lecciones sugeridas (no completadas)
    proximas = Leccion.objects.filter(
        modulo__curso__estado="publicado"
    ).exclude(
        id__in=ProgresoUsuario.objects.filter(
            usuario=u, completado=True
        ).values_list("leccion_id", flat=True)
    ).select_related("modulo__curso")[:5]

    from core.services.notificaciones import contar_no_leidas, ultimas_notificaciones
    from core.services.tareas import (
        evaluaciones_disponibles, evaluaciones_programadas, lecciones_pendientes,
    )
    notif_recientes = list(ultimas_notificaciones(u, n=5))
    notif_count = contar_no_leidas(u)

    tareas_pendientes = list(lecciones_pendientes(u, limit=5))
    evals_disponibles = list(evaluaciones_disponibles(u, limit=5))
    evals_programadas = list(evaluaciones_programadas(u, limit=5))

    context = {
        "kpis": {
            "cursos_activos": cursos_activos,
            "lecciones": lecciones_completadas,
            "certificados": certificados,
            "logros": logros,
            "tasa": tasa,
        },
        "cursos_progreso": cursos_progreso,
        "actividad": actividad,
        "aciertos_data": aciertos_data,
        "ultimos_logros": ultimos_logros,
        "ultimos_certs": ultimos_certs,
        "proximas": proximas,
        "notificaciones_recientes": notif_recientes,
        "notif_count": notif_count,
        "tareas_pendientes": tareas_pendientes,
        "evals_disponibles": evals_disponibles,
        "evals_programadas": evals_programadas,
    }
    context["mcer_progreso"] = _mcer_progreso(request.user)

    # ??? MCER como curso + lecciones (fix v2.2.15) ???
    try:
        from core.models_gramatica import ProgresoGramatical as _PG, TecnicaGramatical as _TG
        _mcer_ids = list(_TG.objects.filter(modulo__in=["a1","a2","b1","b2","c1","c2"]).values_list("id", flat=True))
        _mcer_dom = _PG.objects.filter(usuario=u, tecnica_id__in=_mcer_ids, estado="dominada").count()
    except Exception:
        _mcer_dom = 0
    if _mcer_dom > 0:
        if isinstance(context.get("kpis"), dict):
            context["kpis"]["cursos_activos"] = context["kpis"].get("cursos_activos", 0) + 1
            context["kpis"]["lecciones"] = context["kpis"].get("lecciones", 0) + _mcer_dom
        context["cursos_activos"] = context.get("cursos_activos", 0) + 1
        context["lecciones_completadas"] = context.get("lecciones_completadas", 0) + _mcer_dom

    return render(request, "core/estudiante/dashboard.html", context)


# ============================================================
# MIS CURSOS
# ============================================================
@login_required
def mis_cursos(request):
    u = _get_user(request)
    cursos = Curso.objects.filter(estado="publicado").order_by("titulo")

    data = []
    for curso in cursos:
        total = Leccion.objects.filter(modulo__curso=curso).count()
        completadas = ProgresoUsuario.objects.filter(
            usuario=u, leccion__modulo__curso=curso, completado=True
        ).count()
        pct = round((completadas / total) * 100, 1) if total else 0
        modulos = Modulo.objects.filter(curso=curso).count()
        data.append({
            "curso": curso,
            "total": total,
            "completadas": completadas,
            "pct": pct,
            "modulos": modulos,
        })

    # Ordenar: en progreso primero, luego sin empezar, luego completados
    data.sort(key=lambda x: (-x["pct"] if 0 < x["pct"] < 100 else 0, x["curso"].titulo))

    return render(request, "core/estudiante/mis_cursos.html", {
        "cursos_data": data,
        })


# ============================================================
# MIS EVALUACIONES
# ============================================================
@login_required
def mis_evaluaciones(request):
    u = _get_user(request)

    # Todas las evaluaciones de cursos en los que tiene progreso
    cursos_ids = ProgresoUsuario.objects.filter(usuario=u).values_list(
        "leccion__modulo__curso_id", flat=True
    ).distinct()

    evaluaciones = EvaluacionCurso.objects.filter(
        curso_id__in=cursos_ids
    ).select_related("curso", "modulo").order_by("curso__titulo", "modulo__orden")

    pendientes = []
    completadas = []

    for ev in evaluaciones:
        resultados = ResultadoEvaluacionCurso.objects.filter(
            evaluacion=ev, usuario=u
        ).order_by("-fecha_inicio")
        if resultados.exists():
            mejor = resultados.order_by("-puntaje_obtenido").first()
            completadas.append({
                "ev": ev,
                "intentos": resultados.count(),
                "mejor": mejor.puntaje_obtenido,
                "max": ev.puntaje_maximo,
                "ultimo": resultados.first().fecha_inicio,
            })
        else:
            pendientes.append({"ev": ev})

    return render(request, "core/estudiante/mis_evaluaciones.html", {
        "pendientes": pendientes,
        "completadas": completadas,
        "total": evaluaciones.count(),
    })


# ============================================================
# MIS LOGROS
# ============================================================
@login_required
def mis_logros(request):
    u = _get_user(request)

    obtenidos_ids = LogroObtenido.objects.filter(user=u).values_list(
        "logro_id", flat=True
    )
    obtenidos = LogroObtenido.objects.filter(user=u).select_related("logro").order_by(
        "-fecha_obtenida"
    )
    # Filtrar solo los 6 logros MCER (ids 31-36, no hay campo diferenciador)
    MCER_FILTER = Q(nombre__icontains="MCER") | Q(nombre__regex=r"^(B1|B2|C1|C2) alcanzado$")
    logros_mcer = Logro.objects.filter(MCER_FILTER)
    obtenidos = LogroObtenido.objects.filter(user=u, logro__in=logros_mcer).select_related("logro").order_by("logro__puntos_requeridos")
    por_obtener = logros_mcer.exclude(id__in=obtenidos_ids).order_by(
        "puntos_requeridos", "nivel_requerido"
    )

    return render(request, "core/estudiante/mis_logros.html", {
        "obtenidos": obtenidos,
        "por_obtener": por_obtener,
        "total_obtenidos": obtenidos.count(),
        "total_logros": logros_mcer.count(),
    })


# ============================================================
# MIS CERTIFICADOS
# ============================================================
@login_required
def mis_certificados(request):
    u = _get_user(request)

    obtenidos = CertificacionObtenida.objects.filter(user=u).select_related(
        "certificacion"
    ).order_by("-fecha_obtenida")

    # Certificaciones disponibles que aún no tiene
    obtenidos_ids = obtenidos.values_list("certificacion_id", flat=True)
    disponibles = Certificacion.objects.filter(activa=True).exclude(
        id__in=obtenidos_ids
    )

    return render(request, "core/estudiante/mis_certificados.html", {
        "obtenidos": obtenidos,
        "disponibles": disponibles,
        "total": obtenidos.count(),
    })


# ============================================================
# MIS ESTADÍSTICAS
# ============================================================
@login_required
def mis_estadisticas(request):
    u = _get_user(request)

    total_resp = Respuesta.objects.filter(user=u).count()
    correctas = Respuesta.objects.filter(user=u, es_correcta=True).count()
    tasa = round((correctas / total_resp) * 100, 1) if total_resp else 0

    # Promedio por curso
    cursos_stats = []
    cursos_ids = ProgresoUsuario.objects.filter(usuario=u).values_list(
        "leccion__modulo__curso_id", flat=True
    ).distinct()
    for cid in cursos_ids:
        curso = Curso.objects.filter(id=cid).first()
        if not curso:
            continue
        prom = ProgresoUsuario.objects.filter(
            usuario=u, leccion__modulo__curso=curso, completado=True
        ).aggregate(p=Avg("puntaje_obtenido"))["p"] or 0
        completadas = ProgresoUsuario.objects.filter(
            usuario=u, leccion__modulo__curso=curso, completado=True
        ).count()
        cursos_stats.append({
            "curso": curso,
            "promedio": round(prom, 1),
            "completadas": completadas,
        })

    # Progreso por categoría (por tipo de ejercicio)
    por_tipo = (
        Respuesta.objects.filter(user=u)
        .values("tipo_ejercicio")
        .annotate(
            total=Count("id"),
            correctas=Count("id", filter=Q(es_correcta=True)),
        )
        .order_by("-total")
    )
    tipos_data = [
        {
            "tipo": t["tipo_ejercicio"],
            "total": t["total"],
            "correctas": t["correctas"],
            "tasa": round((t["correctas"] / t["total"]) * 100, 1) if t["total"] else 0,
        }
        for t in por_tipo
    ]

    # Actividad
    hoy = timezone.now()
    actividad = []
    for i in range(30):
        dia = hoy - timedelta(days=29 - i)
        inicio = dia.replace(hour=0, minute=0, second=0, microsecond=0)
        fin = inicio + timedelta(days=1)
        n = ProgresoUsuario.objects.filter(
            usuario=u, completado=True,
            completado_en__gte=inicio, completado_en__lt=fin
        ).count()
        actividad.append({"dia": inicio.strftime("%d/%m"), "count": n})


    # ??? Comparativas vs cohorte (v2.2.17) ???
    _COHORTE = "testest"
    _raw_class = list(
        Respuesta.objects
        .filter(user__username__startswith=_COHORTE)
        .exclude(user=u)
        .values("user")
        .annotate(total=Count("id"), correctas=Count("id", filter=Q(es_correcta=True)))
        .filter(total__gte=10)
    )
    _class_tasas = [r["correctas"] / r["total"] * 100 for r in _raw_class]
    _class_tasa_avg = round(sum(_class_tasas) / len(_class_tasas), 1) if _class_tasas else 0
    _top10_tasas = sorted(_class_tasas, reverse=True)[:10]
    _top10_tasa_avg = round(sum(_top10_tasas) / len(_top10_tasas), 1) if _top10_tasas else 0

    _user_lecciones = ProgresoUsuario.objects.filter(usuario=u, completado=True).count()
    _raw_lec = list(
        ProgresoUsuario.objects
        .filter(completado=True, usuario__username__startswith=_COHORTE)
        .exclude(usuario=u)
        .values("usuario")
        .annotate(n=Count("id"))
    )
    _class_lec_vals = [r["n"] for r in _raw_lec]
    _class_lec_avg = round(sum(_class_lec_vals) / len(_class_lec_vals), 1) if _class_lec_vals else 0
    _top10_lec_vals = sorted(_class_lec_vals, reverse=True)[:10]
    _top10_lec_avg = round(sum(_top10_lec_vals) / len(_top10_lec_vals), 1) if _top10_lec_vals else 0

    _cohorte_tasas = _class_tasas + [tasa]
    _percentil = round(sum(1 for t in _cohorte_tasas if t < tasa) / len(_cohorte_tasas) * 100) if _cohorte_tasas else 0

    _tipos_user = (
        Respuesta.objects.filter(user=u)
        .values("tipo_ejercicio")
        .annotate(total=Count("id"), correctas=Count("id", filter=Q(es_correcta=True)))
        .order_by("-total")
    )
    _class_tipos_map = {}
    for _r in (Respuesta.objects
        .filter(user__username__startswith=_COHORTE)
        .exclude(user=u)
        .values("tipo_ejercicio", "user")
        .annotate(total=Count("id"), correctas=Count("id", filter=Q(es_correcta=True)))
        .filter(total__gte=5)
    ):
        _class_tipos_map.setdefault(_r["tipo_ejercicio"], []).append(_r["correctas"] / _r["total"] * 100)

    _comparativa_tipos = []
    for _t in _tipos_user:
        _tipo = _t["tipo_ejercicio"]
        _tu_tasa = round(_t["correctas"] / _t["total"] * 100, 1) if _t["total"] else 0
        _vals = _class_tipos_map.get(_tipo, [])
        _cavg = round(sum(_vals) / len(_vals), 1) if _vals else 0
        _comparativa_tipos.append({"tipo": _tipo, "tu_tasa": _tu_tasa, "class_tasa": _cavg})

    _comparativa = {
        "user_tasa": tasa,
        "class_tasa_avg": _class_tasa_avg,
        "top10_tasa_avg": _top10_tasa_avg,
        "user_lecciones": _user_lecciones,
        "class_lecciones_avg": _class_lec_avg,
        "top10_lecciones_avg": _top10_lec_avg,
        "percentil": _percentil,
        "cohorte_size": len(_class_tasas),
    }


    # --- Enriquecimiento comparativa v2.2.18 ---
    _comparativa["delta_tasa"] = round(tasa - _comparativa["class_tasa_avg"], 1)
    _comparativa["percentil_inv"] = 100 - _comparativa["percentil"]
    _comparativa["delta_lecciones"] = _user_lecciones - _comparativa["class_lecciones_avg"]
    if _comparativa_tipos:
        _with_delta = [dict(t, delta=round(t["tu_tasa"] - t["class_tasa"], 1)) for t in _comparativa_tipos]
        _comparativa["mejor_tipo"] = max(_with_delta, key=lambda x: x["delta"])
        _comparativa["peor_tipo"] = min(_with_delta, key=lambda x: x["delta"])
    else:
        _comparativa["mejor_tipo"] = None
        _comparativa["peor_tipo"] = None

    return render(request, "core/estudiante/mis_estadisticas.html", {
        "total_resp": total_resp,
        "correctas": correctas,
        "tasa": tasa,
        "cursos_stats": cursos_stats,
        "tipos_data": tipos_data,
        "actividad": actividad,
        "comparativa": _comparativa,
        "comparativa_tipos": _comparativa_tipos,
    })


# ============================================================
# MI RANKING
# ============================================================
@login_required
def mi_ranking(request):
    u = _get_user(request)

    from core.models_gramatica import ProgresoGramatical, TecnicaGramatical

    # Ranking global (añadimos total_respuestas para tasa)
    from django.db.models import Q as _Q
    estudiantes_qs = User.objects.filter(
        _Q(groups__name="Estudiante") | _Q(username__startswith="testest")
    ).annotate(
        num_progresos=Count(
            "progreso_lecciones",
            filter=Q(progreso_lecciones__completado=True),
            distinct=True,
        ),
        correctas=Count(
            "respuestas",
            filter=Q(respuestas__es_correcta=True),
            distinct=True,
        ),
        total_respuestas=Count("respuestas", distinct=True),
    ).order_by("-num_progresos", "-correctas")

    estudiantes = list(estudiantes_qs)
    total_estudiantes = len(estudiantes)

    # MCER dominadas por estudiante (una sola query)
    mcer_ids = list(
        TecnicaGramatical.objects
        .filter(modulo__in=["a1", "a2", "b1", "b2", "c1", "c2"])
        .values_list("id", flat=True)
    )
    mcer_map = dict(
        ProgresoGramatical.objects
        .filter(estado="dominada", tecnica_id__in=mcer_ids,
                usuario_id__in=[e.id for e in estudiantes])
        .values_list("usuario_id")
        .annotate(n=Count("id"))
        .values_list("usuario_id", "n")
    )
    for e in estudiantes:
        e.mcer_dominadas = mcer_map.get(e.id, 0)

    mi_posicion = None
    mi_fila = None
    top10 = []
    for i, est in enumerate(estudiantes, start=1):
        row = {
            "pos": i,
            "user": est,
            "progresos": est.num_progresos,
            "correctas": est.correctas,
            "total_respuestas": est.total_respuestas,
            "mcer": getattr(est, "mcer_dominadas", 0),
        }
        if i <= 10:
            top10.append(row)
        if est.id == u.id:
            mi_posicion = i
            mi_fila = row

    # --- Agregados para gráficas (v2.2.20) ---
    max_lec = max((e.num_progresos for e in estudiantes), default=0) or 1
    max_corr = max((e.correctas for e in estudiantes), default=0) or 1

    def _tasa(correctas, total):
        return round(correctas / total * 100, 1) if total else 0

    # Promedios clase
    prom_lec = round(sum(e.num_progresos for e in estudiantes) / total_estudiantes, 1) if total_estudiantes else 0
    prom_corr = round(sum(e.correctas for e in estudiantes) / total_estudiantes, 1) if total_estudiantes else 0
    prom_tasa = round(
        sum(_tasa(e.correctas, e.total_respuestas) for e in estudiantes) / total_estudiantes, 1
    ) if total_estudiantes else 0

    # Top 10 promedios
    top10_objs = estudiantes[:10]
    t10_lec = round(sum(e.num_progresos for e in top10_objs) / len(top10_objs), 1) if top10_objs else 0
    t10_corr = round(sum(e.correctas for e in top10_objs) / len(top10_objs), 1) if top10_objs else 0
    t10_tasa = round(
        sum(_tasa(e.correctas, e.total_respuestas) for e in top10_objs) / len(top10_objs), 1
    ) if top10_objs else 0

    # Mi tasa
    mi_tasa = _tasa(mi_fila["correctas"], mi_fila["total_respuestas"]) if mi_fila else 0

    # Percentil por lecciones (cuántos tienen MENOS que yo)
    if mi_fila and total_estudiantes > 1:
        inferiores = sum(1 for e in estudiantes if e.num_progresos < mi_fila["progresos"])
        percentil = round(inferiores / (total_estudiantes - 1) * 100)
    else:
        percentil = 0

    # Cuartiles por lecciones
    q_counts = {"q1": 0, "q2": 0, "q3": 0, "q4": 0}
    mi_q = None
    for e in estudiantes:
        ratio = e.num_progresos / max_lec
        if ratio >= 0.75:
            q_counts["q1"] += 1
            if mi_fila and e.id == u.id: mi_q = "q1"
        elif ratio >= 0.50:
            q_counts["q2"] += 1
            if mi_fila and e.id == u.id: mi_q = "q2"
        elif ratio >= 0.25:
            q_counts["q3"] += 1
            if mi_fila and e.id == u.id: mi_q = "q3"
        else:
            q_counts["q4"] += 1
            if mi_fila and e.id == u.id: mi_q = "q4"

    # Radar: mi, clase, top 10 (4 dims normalizadas 0-100)
    def _norm_lec(n):
        return round(min(100, n / max_lec * 100)) if max_lec else 0
    def _norm_corr(n):
        return round(min(100, n / max_corr * 100)) if max_corr else 0
    def _norm_mcer(n):
        return round(min(100, n / 610 * 100)) if 610 else 0

    radar_mi = {
        "lecciones": _norm_lec(mi_fila["progresos"]) if mi_fila else 0,
        "tasa": mi_tasa,
        "correctas": _norm_corr(mi_fila["correctas"]) if mi_fila else 0,
        "mcer": _norm_mcer(mi_fila["mcer"]) if mi_fila else 0,
    }
    radar_clase = {
        "lecciones": _norm_lec(prom_lec),
        "tasa": prom_tasa,
        "correctas": _norm_corr(prom_corr),
        "mcer": _norm_mcer(
            sum(e.mcer_dominadas for e in estudiantes) / total_estudiantes if total_estudiantes else 0
        ),
    }
    radar_top10 = {
        "lecciones": _norm_lec(t10_lec),
        "tasa": t10_tasa,
        "correctas": _norm_corr(t10_corr),
        "mcer": _norm_mcer(
            sum(e.mcer_dominadas for e in top10_objs) / len(top10_objs) if top10_objs else 0
        ),
    }

    # Top 10 para el gráfico de barras
    top10_chart = [
        {"username": r["user"].username, "lecciones": r["progresos"], "es_tu": r["user"].id == u.id}
        for r in top10
    ]

    return render(request, "core/estudiante/mi_ranking.html", {
        "top10": top10,
        "mi_posicion": mi_posicion,
        "mi_fila": mi_fila,
        "total_estudiantes": total_estudiantes,
        "resumen_ranking": {
            "mi_tasa": mi_tasa,
            "mi_percentil": percentil,
            "mi_cuartil": mi_q,
            "prom_lecciones": prom_lec,
            "prom_correctas": prom_corr,
            "prom_tasa": prom_tasa,
            "top10_lecciones": t10_lec,
            "top10_correctas": t10_corr,
            "top10_tasa": t10_tasa,
        },
        "cuartiles": q_counts,
        "radar": {
            "mi": radar_mi,
            "clase": radar_clase,
            "top10": radar_top10,
        },
        "top10_chart": top10_chart,
    })


# ============================================================
# DESCARGAS DE CERTIFICADOS (solo los propios)
# ============================================================
@login_required
def descargar_certificado_pdf(request, certificado_id):
    from .utils_certificados import generar_certificado_pdf
    cert = get_object_or_404(CertificacionObtenida, id=certificado_id, user=request.user)
    try:
        pdf_bytes = generar_certificado_pdf(cert, request.user)
    except Exception as e:
        messages.error(request, f"Error: {e}")
        return redirect("estudiante:certificados")
    response = HttpResponse(pdf_bytes, content_type="application/pdf")
    response["Content-Disposition"] = f'attachment; filename="certificado_{cert.codigo_verificacion}.pdf"'
    return response


@login_required
def descargar_certificado_docx(request, certificado_id):
    from .utils_certificados import generar_certificado_docx
    cert = get_object_or_404(CertificacionObtenida, id=certificado_id, user=request.user)
    try:
        docx_bytes = generar_certificado_docx(cert, request.user)
    except Exception as e:
        messages.error(request, f"Error: {e}")
        return redirect("estudiante:certificados")
    response = HttpResponse(
        docx_bytes,
        content_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    )
    response["Content-Disposition"] = f'attachment; filename="certificado_{cert.codigo_verificacion}.docx"'
    return response


def _diag(request):
    """Diagn?stico temporal: conteos de datos para gr?ficas. Borrar tras usar."""
    from django.http import JsonResponse
    from django.apps import apps
    u = request.user
    Respuesta = apps.get_model("core", "Respuesta")
    ProgresoUsuario = apps.get_model("core", "ProgresoUsuario")
    ProgresoGramatical = apps.get_model("core", "ProgresoGramatical")
    return JsonResponse({
        "user": u.username,
        "respuesta_count": Respuesta.objects.filter(user=u).count(),
        "progreso_usuario_count": ProgresoUsuario.objects.filter(usuario=u, completado=True).count(),
        "mcer_dominadas": ProgresoGramatical.objects.filter(usuario=u, estado="dominada").count(),
        "cursos_activos": ProgresoUsuario.objects.filter(usuario=u).values("leccion__modulo__curso").distinct().count(),
    })
