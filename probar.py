"""Bateria de pruebas automaticas para el sistema experto.

    python probar.py
    python probar.py -v
"""
import sys
from motor_inferencia import diagnosticar
from pruebas.casos_falla import CASOS
from pruebas.casos_motor import (
    casos_cf,
    casos_encadenamiento,
    casos_operadores,
    casos_validacion,
)
from pruebas.ejemplos_lenguaje import (
    CASOS_CONOCIDOS_INCOMPLETOS,
    EJEMPLOS_CORRECTOS,
)
from pruebas.matriz_informacion import (
    DATOS_CATEGORICOS,
    DATOS_MEDIDOS,
    HECHOS_DERIVADOS,
    OBSERVACIONES_HOY,
)
from normalizar import extraer_hechos


def validar_contrato_fase_0():
    """Fase 0: verifica datos conocidos y ejemplos humanos congelados."""
    errores = []

    for nombre, entrada, _, _, _ in CASOS:
        for campo in entrada:
            permitido = campo in DATOS_MEDIDOS or campo in DATOS_CATEGORICOS
            if not permitido:
                errores.append(f"{nombre}: campo de entrada desconocido '{campo}'")

    hechos_disponibles = set(DATOS_MEDIDOS) | set(DATOS_CATEGORICOS)
    hechos_disponibles |= set(HECHOS_DERIVADOS) | set(OBSERVACIONES_HOY)
    for nombre, _, observaciones, _, _ in CASOS:
        for hecho in extraer_hechos(observaciones):
            if hecho not in hechos_disponibles:
                errores.append(f"{nombre}: observacion desconocida '{hecho}'")

    for texto, esperado in EJEMPLOS_CORRECTOS:
        obtenido = extraer_hechos(texto)
        if obtenido != esperado:
            errores.append(
                f"Ejemplo humano '{texto}': esperado={esperado}, obtenido={obtenido}"
            )

    return errores


def main(verbose=False):
    """Ejecuta fases 0 y 1 y devuelve 0 únicamente si todo permanece aprobado."""
    ok = 0
    fallas = []
    contrato = validar_contrato_fase_0()

    pruebas_motor = []
    pruebas_motor.extend(casos_operadores())
    pruebas_motor.extend(casos_encadenamiento())
    pruebas_motor.extend(casos_cf())
    pruebas_motor.extend(casos_validacion())
    motor_ok = 0
    for nombre, obtenido, esperado in pruebas_motor:
        bien = obtenido == esperado
        motor_ok += bien
        if not bien:
            fallas.append((f"Motor: {nombre}", f"esperado={esperado}", f"obtenido={obtenido}"))

    for nombre, entrada, obs, esperado, espera_aviso in CASOS:
        res = diagnosticar(entrada, obs)
        if not res["ok"]:
            fallas.append((nombre, "Error de validacion inesperado", res["errores"]))
            continue

        top_id = res["diagnosticos"][0]["id"] if res["diagnosticos"] else None
        tiene_aviso = len(res["advertencias"]) > 0

        bien = (top_id == esperado) and (tiene_aviso == espera_aviso)
        ok += bien
        if not bien:
            fallas.append((nombre, f"esperado=({esperado}, aviso={espera_aviso})",
                           f"obtenido=({top_id}, aviso={tiene_aviso})"))

    if contrato:
        fallas.extend(("Contrato fase 0", error, "") for error in contrato)

    print(f"Casos aprobados: {ok}/{len(CASOS)} ({100 * ok // len(CASOS)}%)")
    print(f"Pruebas de motor: {motor_ok}/{len(pruebas_motor)}")
    print(f"Contratos de fase 0: {len(contrato)}")
    print(f"Ejemplos humanos correctos: {len(EJEMPLOS_CORRECTOS)}")
    print(f"Limitaciones humanas documentadas: {len(CASOS_CONOCIDOS_INCOMPLETOS)}")
    if verbose:
        for f in fallas:
            print("  FALLA:", f)
    return 0 if ok == len(CASOS) and motor_ok == len(pruebas_motor) and not contrato else 1


if __name__ == "__main__":
    sys.exit(main("-v" in sys.argv))
