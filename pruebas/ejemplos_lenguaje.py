"""Ejemplos humanos congelados para la fase 0.

Los ejemplos correctos documentan el comportamiento deseado.
Los casos conocidos incompletos identifican limitaciones que no se corregiran
en esta fase.
"""

EJEMPLOS_CORRECTOS = [
    # Línea base positiva: cada frase debe producir exactamente el hecho indicado.
    ("hubo un chispazo", {"chispazo": "si"}),
    ("se reinicia cada rato", {"reinicios": "si"}),
    ("el equipo se apaga solo", {"apagado_solo": "si"}),
    ("me sale pantalla azul", {"pantalla_azul": "si"}),
    ("tiene todas las rams instaladas", {"ram_instalada": "si"}),
    ("la pila de la bios ya es nueva", {"pila_bios_ok": "si"}),
]

CASOS_CONOCIDOS_INCOMPLETOS = [
    # Deuda documentada de fase 0; no son casos aprobados ni deben ocultarse.
    {
        "texto": "no hubo chispazo",
        "problema": "Falta manejo de negacion.",
        "resultado_actual": "Detecta chispazo positivo.",
    },
    {
        "texto": "no me sale pantalla azul",
        "problema": "Falta manejo de negacion.",
        "resultado_actual": "Detecta pantalla azul positiva.",
    },
    {
        "texto": "medí 95 volts y los ventiladores sí giran",
        "problema": "No extrae mediciones ni variaciones humanas.",
        "resultado_actual": "No genera datos estructurados.",
    },
    {
        "texto": "no arranca, no enciende el LED ni giran los ventiladores",
        "problema": "No interpreta sintomas compuestos.",
        "resultado_actual": "No genera datos estructurados.",
    },
    {
        "texto": "127 V",
        "problema": "Los campos numericos no aceptan unidades.",
        "resultado_actual": "Rechaza el valor como no numerico.",
    },
]
