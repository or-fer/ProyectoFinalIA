"""Bateria de pruebas automaticas para el sistema experto.

    python probar.py
    python probar.py -v
"""
import sys
from motor_inferencia import diagnosticar
from pruebas.casos_falla import CASOS


def main(verbose=False):
    ok = 0
    fallas = []

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

    print(f"Casos aprobados: {ok}/{len(CASOS)} ({100 * ok // len(CASOS)}%)")
    if verbose:
        for f in fallas:
            print("  FALLA:", f)
    return 0 if ok == len(CASOS) else 1


if __name__ == "__main__":
    sys.exit(main("-v" in sys.argv))
