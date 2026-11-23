"""Casos unitarios de la fase 1 para el motor SI-ENTONCES."""

from motor_inferencia import _cumple, diagnosticar, validar_kb


def kb_minima(reglas):
    """Construye una KB mínima para aislar una prueba de motor."""
    return {
        "umbral_reporte": 0.3,
        "niveles": {"baja": 0.3, "media": 0.5, "alta": 0.75},
        "diagnosticos": {
            "D_TEST": {
                "nombre": "Diagnostico de prueba",
                "subsistema": "Prueba",
                "accion": "Verificar.",
                "seguridad": "Sin riesgos especiales.",
            }
        },
        "reglas": reglas,
    }


def casos_operadores():
    """Verifica cada operador usado por las reglas SI-ENTONCES."""
    hechos = {"v": 12.0, "estado": "ok"}
    return [
        ("igualdad", _cumple(["estado", "==", "ok"], hechos), True),
        ("desigualdad", _cumple(["estado", "!=", "no"], hechos), True),
        ("menor", _cumple(["v", "<", 13], hechos), True),
        ("mayor", _cumple(["v", ">", 11], hechos), True),
        ("entre", _cumple(["v", "entre", [11.4, 12.6]], hechos), True),
        ("indefinido", _cumple(["faltante", "indefinido", None], hechos), True),
        ("ausente", _cumple(["faltante", "==", "ok"], hechos), False),
    ]


def casos_encadenamiento():
    """Demuestra que un hecho derivado puede activar una segunda regla."""
    kb = kb_minima([
        {
            "id": "H1",
            "prioridad": 10,
            "tipo": "hecho",
            "si": [["v_ac", ">", 100]],
            "hecho": {"nombre": "derivado", "valor": "si"},
            "porque": "Se derivo el hecho.",
        },
        {
            "id": "R1",
            "prioridad": 20,
            "tipo": "diagnostico",
            "si": [["derivado", "==", "si"]],
            "diagnostico": {"id": "D_TEST", "cf": 0.8},
            "porque": "El hecho derivado activo el diagnostico.",
        },
    ])

    resultado = diagnosticar({"v_ac": 127}, kb=kb)
    ids = [item["regla"] for item in resultado["traza"]]

    return [
        ("encadenamiento directo", resultado["ok"], True),
        ("hecho derivado", resultado["hechos_derivados"].get("derivado"), "si"),
        ("diagnostico principal", resultado["diagnosticos"][0]["id"], "D_TEST"),
        ("traza completa", ids, ["H1", "R1"]),
        ("regla una vez", ids.count("R1"), 1),
    ]


def casos_cf():
    """Verifica la combinación CF = CF1 + CF2(1 - CF1)."""
    kb = kb_minima([
        {
            "id": "R1",
            "prioridad": 10,
            "tipo": "diagnostico",
            "si": [["led_encendido", "==", "si"]],
            "diagnostico": {"id": "D_TEST", "cf": 0.5},
            "porque": "Primera evidencia.",
        },
        {
            "id": "R2",
            "prioridad": 10,
            "tipo": "diagnostico",
            "si": [["ventiladores", "==", "si"]],
            "diagnostico": {"id": "D_TEST", "cf": 0.5},
            "porque": "Segunda evidencia.",
        },
    ])
    resultado = diagnosticar({"led_encendido": "si", "ventiladores": "si"}, kb=kb)
    cf = resultado["diagnosticos"][0]["cf"]
    return [
        ("combinacion CF", cf, 0.75),
        ("razones CF", len(resultado["diagnosticos"][0]["razones"]), 2),
    ]


def casos_validacion():
    """Genera KB válidas e inválidas para comprobar el contrato estructural."""
    reglas = [{
        "id": "R1",
        "prioridad": 10,
        "tipo": "diagnostico",
        "si": [["entrada", "==", "si"]],
        "diagnostico": {"id": "D_TEST", "cf": 0.8},
        "porque": "Evidencia.",
    }]

    kb_valida = kb_minima(reglas)
    kb_id_duplicado = kb_minima([
        reglas[0],
        dict(reglas[0]),
    ])
    kb_cf_invalida = kb_minima([{
        **reglas[0],
        "diagnostico": {"id": "D_TEST", "cf": 1.5},
    }])
    kb_operador_invalido = kb_minima([{
        **reglas[0],
        "si": [["entrada", "como", "si"]],
    }])

    return [
        ("KB valida", validar_kb(kb_valida), []),
        ("id duplicado", any("id duplicado" in e for e in validar_kb(kb_id_duplicado)), True),
        ("CF invalida", any("CF debe estar" in e for e in validar_kb(kb_cf_invalida)), True),
        ("operador invalido", any("operador invalido" in e for e in validar_kb(kb_operador_invalido)), True),
    ]
