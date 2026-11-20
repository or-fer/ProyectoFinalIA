"""Motor de inferencia basado en reglas SI-ENTONCES.

Aplica encadenamiento hacia adelante (forward chaining) sobre la base de
conocimiento y combina factores de certeza (CF) cuando varias reglas apuntan
al mismo diagnostico.
"""
import json
import os
from collections import defaultdict

from normalizar import extraer_hechos

RUTA_KB = os.path.join(os.path.dirname(os.path.abspath(__file__)), "base_conocimiento.json")

SI_NO = ["si", "no"]

CATEGORICOS = {
    "led_encendido": SI_NO,
    "ventiladores": SI_NO,
    "video": SI_NO,
    "beeps": ["ninguno", "cortos_repetitivos", "uno_largo_dos_cortos", "continuo"],
    "olor_quemado": SI_NO,
    "fusible_continuidad": SI_NO,
    "red_detectada": SI_NO,
    "led_puerto_red": SI_NO,
    "continuidad_cable_red": SI_NO,
    "usb_responde": SI_NO,
}

# campo: (minimo fisico, maximo fisico, unidad)
NUMERICOS = {
    "v_ac": (0, 300, "V"),
    "v_12": (0, 20, "V"),
    "v_5": (0, 10, "V"),
    "v_3_3": (0, 6, "V"),
    "temp_cpu": (0, 150, "°C"),
}

OPERADORES = {
    "==": lambda v, r: v == r,
    "!=": lambda v, r: v != r,
    "<": lambda v, r: v < r,
    ">": lambda v, r: v > r,
    "<=": lambda v, r: v <= r,
    ">=": lambda v, r: v >= r,
    "entre": lambda v, r: r[0] <= v <= r[1],
    "en": lambda v, r: v in r,
}


class _Faltante(dict):
    def __missing__(self, clave):
        return "?"


def cargar_kb(ruta=RUTA_KB):
    with open(ruta, encoding="utf-8") as f:
        kb = json.load(f)
    kb["reglas"].sort(key=lambda r: r["prioridad"])
    return kb


def validar_entrada(entrada):
    """Valida tipos y rangos fisicos. Los campos vacios se omiten (dato no medido)."""
    hechos, errores = {}, []
    for campo, valor in entrada.items():
        if valor is None or str(valor).strip() == "":
            continue
        if campo in CATEGORICOS:
            v = str(valor).strip().lower()
            if v not in CATEGORICOS[campo]:
                errores.append(f"{campo}: valor '{valor}' no valido.")
            else:
                hechos[campo] = v
        elif campo in NUMERICOS:
            minimo, maximo, unidad = NUMERICOS[campo]
            try:
                v = float(str(valor).replace(",", "."))
            except ValueError:
                errores.append(f"{campo}: '{valor}' no es un numero.")
                continue
            if not (minimo <= v <= maximo):
                errores.append(f"{campo}: {v} {unidad} fuera de rango ({minimo} a {maximo} {unidad}).")
            else:
                hechos[campo] = v
        else:
            errores.append(f"Campo desconocido: '{campo}'.")
    return hechos, errores


def revisar_congruencia(hechos):
    """Detecta contradicciones fisicas o logicas evidentes entre los datos capturados."""
    avisos = []
    v_ac = hechos.get("v_ac")
    v_12 = hechos.get("v_12")
    hay_dc = any(hechos.get(r, 0) > 1.0 for r in ("v_12", "v_5", "v_3_3"))
    hay_actividad = hechos.get("led_encendido") == "si" or hechos.get("ventiladores") == "si"

    if v_ac is not None and v_ac < 90 and (hay_dc or hay_actividad):
        avisos.append(
            f"Con {v_ac} V en la toma AC no deberia haber voltaje DC ni ventiladores/LED activos "
            "(verifique la escala del multimetro o los datos)."
        )

    if hechos.get("fusible_continuidad") == "no" and (hay_dc or hay_actividad):
        avisos.append(
            "Si el fusible no tiene continuidad, no deberia haber salida DC ni giro de ventiladores."
        )

    if v_12 is not None and v_12 < 10.0 and hechos.get("ventiladores") == "si":
        avisos.append(
            f"Los ventiladores giran pero el riel de 12 V marca {v_12} V; confirme la medicion."
        )

    if hechos.get("red_detectada") == "si" and hechos.get("continuidad_cable_red") == "no":
        avisos.append(
            "Se reporta red detectada pero sin continuidad en el cable (verifique si usa Wi-Fi)."
        )

    return avisos


def _cumple(condicion, hechos):
    hecho, op, referencia = condicion
    if op == "indefinido":
        return hecho not in hechos
    if hecho not in hechos:
        return False
    try:
        return OPERADORES[op](hechos[hecho], referencia)
    except TypeError:
        return False


def _nivel(cf, kb):
    if cf >= kb["niveles"]["alta"]:
        return "alta"
    if cf >= kb["niveles"]["media"]:
        return "media"
    return "baja"


def diagnosticar(entrada, texto_libre="", kb=None):
    """Ejecuta el encadenamiento hacia adelante y devuelve los diagnosticos ordenados."""
    kb = kb or cargar_kb()

    hechos, errores = validar_entrada(entrada)
    if errores:
        return {"ok": False, "errores": errores}

    for hecho, valor in extraer_hechos(texto_libre).items():
        hechos.setdefault(hecho, valor)
    hechos_entrada = dict(hechos)
    advertencias = revisar_congruencia(hechos_entrada)

    pendientes = list(kb["reglas"])
    contribuciones = defaultdict(list)
    traza = []
    hubo_cambio = True

    while hubo_cambio:
        hubo_cambio = False
        for regla in list(pendientes):
            if all(_cumple(c, hechos) for c in regla["si"]):
                pendientes.remove(regla)
                hubo_cambio = True
                texto = regla["porque"].format_map(_Faltante(hechos))
                traza.append({"regla": regla["id"], "tipo": regla["tipo"], "texto": texto})
                if regla["tipo"] == "hecho":
                    hechos[regla["hecho"]["nombre"]] = regla["hecho"]["valor"]
                else:
                    d = regla["diagnostico"]
                    contribuciones[d["id"]].append((d["cf"], regla["id"], texto))

    # Si hay contradicciones graves, reducimos ligeramente la confianza general
    factor = 0.85 if advertencias else 1.0

    diagnosticos = []
    for did, aportes in contribuciones.items():
        cf = 0.0
        for valor, _, _ in aportes:
            cf = cf + valor * (1 - cf)
        cf *= factor
        if cf < kb["umbral_reporte"]:
            continue
        info = kb["diagnosticos"][did]
        diagnosticos.append({
            "id": did,
            "nombre": info["nombre"],
            "subsistema": info["subsistema"],
            "cf": round(cf, 3),
            "nivel": _nivel(cf, kb),
            "accion": info["accion"],
            "seguridad": info["seguridad"],
            "razones": [{"regla": r, "texto": t} for _, r, t in aportes],
        })
    diagnosticos.sort(key=lambda d: (-d["cf"], d["id"]))

    sugerencias = []
    if not diagnosticos:
        for campo, (_, _, unidad) in NUMERICOS.items():
            if campo not in hechos_entrada:
                sugerencias.append(f"Mida o capture {campo} ({unidad}).")
        sugerencias.append("Complete los sintomas basicos (LED, ventiladores, video, pitidos).")

    return {
        "ok": True,
        "diagnosticos": diagnosticos,
        "indeterminado": not diagnosticos,
        "advertencias": advertencias,
        "sugerencias": sugerencias,
        "hechos_entrada": hechos_entrada,
        "hechos_derivados": {k: v for k, v in hechos.items() if k not in hechos_entrada},
        "traza": traza,
    }


def formatear_resultado(res):
    """Convierte el resultado del diagnostico a texto legible."""
    if not res["ok"]:
        return "ENTRADA NO VÁLIDA:\n" + "\n".join(f"  - {e}" for e in res["errores"])

    lineas = []
    if res.get("advertencias"):
        lineas.append("ADVERTENCIAS DE CONGRUENCIA:")
        for a in res["advertencias"]:
            lineas.append(f"  - {a}")
        lineas.append("")

    if res["indeterminado"]:
        lineas.append("No hay evidencia suficiente para un diagnóstico.")
        lineas.extend(f"  - {s}" for s in res["sugerencias"])
        return "\n".join(lineas)

    for i, d in enumerate(res["diagnosticos"][:3]):
        etiqueta = "DIAGNÓSTICO PRINCIPAL" if i == 0 else f"ALTERNATIVA {i}"
        lineas.append(f"{etiqueta}: {d['nombre']}")
        lineas.append(f"  Confianza: {d['cf'] * 100:.0f}% ({d['nivel']})  |  Subsistema: {d['subsistema']}")
        lineas.append("  Por qué:")
        lineas += [f"    - [{r['regla']}] {r['texto']}" for r in d["razones"]]
        lineas.append(f"  Acción sugerida: {d['accion']}")
        lineas.append(f"  Seguridad: {d['seguridad']}")
        lineas.append("")
    return "\n".join(lineas).rstrip()
