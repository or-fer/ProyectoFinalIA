"""Contrato de informacion separado por etapa del razonamiento.

Este archivo congela la fase 0 sin modificar el motor ni la interfaz.
Las clases solo describen los datos que el sistema puede recibir hoy.
"""

DATOS_MEDIDOS = {
    "v_ac": {"tipo": "numero", "unidad": "V", "ejemplo": 127},
    "v_12": {"tipo": "numero", "unidad": "V", "ejemplo": 12.05},
    "v_5": {"tipo": "numero", "unidad": "V", "ejemplo": 5.01},
    "v_3_3": {"tipo": "numero", "unidad": "V", "ejemplo": 3.31},
    "temp_cpu": {"tipo": "numero", "unidad": "°C", "ejemplo": 98},
}

DATOS_CATEGORICOS = {
    "fusible_continuidad": {"tipo": "si_no", "ejemplo": "si"},
    "led_encendido": {"tipo": "si_no", "ejemplo": "si"},
    "ventiladores": {"tipo": "si_no", "ejemplo": "si"},
    "video": {"tipo": "si_no", "ejemplo": "si"},
    "beeps": {
        "tipo": "patron",
        "ejemplo": "cortos_repetitivos",
        "valores": ["ninguno", "cortos_repetitivos", "uno_largo_dos_cortos", "continuo"],
    },
    "olor_quemado": {"tipo": "si_no", "ejemplo": "no"},
    "red_detectada": {"tipo": "si_no", "ejemplo": "si"},
    "led_puerto_red": {"tipo": "si_no", "ejemplo": "si"},
    "continuidad_cable_red": {"tipo": "si_no", "ejemplo": "si"},
    "usb_responde": {"tipo": "si_no", "ejemplo": "si"},
}

OBSERVACIONES_HOY = {
    "chispazo": ["chispazo", "chispazos", "chispa", "corto"],
    "reinicios": ["reinicia", "reinicios", "reiniciando", "se reinicia"],
    "apagado_solo": ["apaga solo", "se apaga", "apagado repentino"],
    "pantalla_azul": ["pantalla azul", "BSOD", "pantallazo azul"],
    "ram_instalada": [
        "tiene ram",
        "tiene todas las rams",
        "ram instalada",
        "memoria instalada",
    ],
    "pila_bios_ok": ["pila de la bios", "pila nueva", "bateria CMOS OK"],
}

HECHOS_DERIVADOS = {
    "ac_ok": {"valores": ["si", "no"]},
    "entrada_ac_valida": {"valores": ["si", "no"]},
    "riel_12": {"valores": ["bajo", "ok", "alto"]},
    "riel_5": {"valores": ["bajo", "ok", "alto"]},
    "riel_3_3": {"valores": ["bajo", "ok", "alto"]},
    "alimentacion_ok": {"valores": ["si", "no"]},
    "psu_alimentacion_ok": {"valores": ["si", "no"]},
    "sin_actividad": {"valores": ["si", "no"]},
    "fusionado_o_sobrecalentado": {"valores": ["si", "no"]},
}

CONCLUSIONES = {
    "diagnosticos": "Resultado generado por reglas SI-ENTONCES.",
    "advertencias": "Contradiccion fisica o logica detectada por congruencia.",
    "sugerencias": "Datos adicionales necesarios para continuar el diagnostico.",
    "razones": "Reglas que apoyaron cada conclusion.",
}
