"""Preprocesamiento de texto libre para el campo de observaciones.

Convierte a mayusculas, elimina tildes y signos de puntuacion para detectar
sintomas adicionales mencionados por el tecnico.
"""
import re
import unicodedata

# Palabras clave que se traducen a hechos booleanos si no vienen en el formulario
PATRONES_OBSERVACIONES = {
    # Estas frases producen hechos positivos; negaciones e incertidumbre aún no se interpretan.
    "chispazo": ["CHISPA", "CHISPAZO", "CHISPAZOS", "CORTO"],
    "reinicios": ["REINICIA", "REINICIOS", "REINICIANDO", "SE REINICIA"],
    "apagado_solo": ["APAGA SOLO", "SE APAGA", "APAGADO REPENTINO"],
    "pantalla_azul": ["PANTALLA AZUL", "BSOD", "PANTALLAZO AZUL"],
    "ram_instalada": ["TIENE RAM", "TIENE TODAS LAS RAMS", "RAM INSTALADA", "MEMORIA INSTALADA"],
    "pila_bios_ok": ["PILA DE LA BIOS", "PILA NUEVA", "BATERIA CMOS OK"],
}


def normalizar_entrada(texto):
    nfkd = unicodedata.normalize("NFD", texto)
    sin_acentos = "".join(c for c in nfkd if unicodedata.category(c) != "Mn")
    solo_alfanum = re.sub(r"[^A-Za-z0-9\s]", " ", sin_acentos)
    return " ".join(solo_alfanum.upper().split())


def extraer_hechos(texto):
    """Busca sintomas clave en las observaciones y devuelve un diccionario de hechos."""
    if not texto or not texto.strip():
        return {}
    limpio = f" {normalizar_entrada(texto)} "
    encontrados = {}
    for hecho, variantes in PATRONES_OBSERVACIONES.items():
        if any(f" {v} " in limpio for v in variantes):
            encontrados[hecho] = "si"
    return encontrados
