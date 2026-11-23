"""Demostracion rapida por consola con tres escenarios tipicos.

Los datos ya están estructurados. Esta demostración no prueba conversación
humana ni extracción automática de mediciones desde texto libre.
"""
from motor_inferencia import diagnosticar, formatear_resultado

EJEMPLOS = [
    (
        "Caso 1: Fallo de memoria RAM (pitidos cortos)",
        {"v_ac": 127, "v_12": 12.05, "v_5": 5.01, "v_3_3": 3.31,
         "ventiladores": "si", "video": "no", "beeps": "cortos_repetitivos"},
        "tiene todas las rams instaladas"
    ),
    (
        "Caso 2: Toma AC sin voltaje adecuado",
        {"v_ac": 85, "led_encendido": "no", "ventiladores": "no"},
        ""
    ),
    (
        "Caso 3: Datos contradictorios (2V en pared pero ventiladores girando)",
        {"v_ac": 2, "v_12": 3, "v_5": 4, "v_3_3": 3, "ventiladores": "si", "led_encendido": "si"},
        ""
    ),
]

if __name__ == "__main__":
    for titulo, datos, obs in EJEMPLOS:
        print("=" * 60)
        print(titulo)
        print("=" * 60)
        print(formatear_resultado(diagnosticar(datos, obs)))
        print()
