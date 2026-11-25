"""Controlador de una sesion de diagnostico.

Conserva el estado entre turnos sin modificar la logica del motor de
inferencia. Los datos estructurados y las observaciones se mantienen
separados porque el motor valida cada tipo de entrada de forma distinta.
"""
from copy import deepcopy
from collections.abc import Mapping

from motor_inferencia import diagnosticar
from normalizar import extraer_hechos


class GestorSesion:
    """Coordina entradas sucesivas de una sesion de diagnostico."""

    ETAPA_MINIMA = 1
    ETAPA_MAXIMA = 4

    def __init__(self, etapa_inicial=1, kb=None):
        self._validar_etapa(etapa_inicial)
        self.etapa_actual = etapa_inicial
        self.kb = kb
        self.historial = []
        self.entrada_acumulada = {}
        self.hechos_acumulados = {}
        self.observaciones = []
        self.ultimo_resultado = None

    def procesar(self, entrada=None, texto_libre=""):
        """Acumula un turno y ejecuta el diagnostico con todo el contexto."""
        if entrada is None:
            entrada = {}
        if not isinstance(entrada, Mapping):
            raise TypeError("La entrada de la sesion debe ser un objeto tipo diccionario.")
        if texto_libre is None:
            texto_libre = ""
        if not isinstance(texto_libre, str):
            raise TypeError("El texto libre de la sesion debe ser una cadena.")

        entrada_turno = dict(entrada)
        hechos_texto = extraer_hechos(texto_libre)

        # La entrada estructurada tiene prioridad sobre hechos detectados en
        # el mismo turno, igual que en motor_inferencia.diagnosticar.
        self.entrada_acumulada.update(entrada_turno)
        hechos_turno = dict(hechos_texto)
        hechos_turno.update(entrada_turno)
        self.hechos_acumulados.update(hechos_turno)
        if texto_libre.strip():
            self.observaciones.append(texto_libre.strip())

        resultado = diagnosticar(
            self.entrada_acumulada,
            " ".join(self.observaciones),
            kb=self.kb,
        )
        self.ultimo_resultado = resultado
        self.historial.append({
            "etapa": self.etapa_actual,
            "entrada": deepcopy(entrada_turno),
            "texto": texto_libre,
            "hechos": deepcopy(hechos_turno),
            "resultado": deepcopy(resultado),
        })
        return resultado

    def avanzar_etapa(self):
        """Avanza una etapa sin superar la etapa 4 y devuelve la etapa actual."""
        self.etapa_actual = min(self.etapa_actual + 1, self.ETAPA_MAXIMA)
        return self.etapa_actual

    def establecer_etapa(self, etapa):
        """Establece explicitamente la etapa actual entre 1 y 4."""
        self._validar_etapa(etapa)
        self.etapa_actual = etapa

    def reiniciar(self, etapa_inicial=1):
        """Borra el contexto de la sesion y comienza una etapa nueva."""
        self._validar_etapa(etapa_inicial)
        self.etapa_actual = etapa_inicial
        self.historial.clear()
        self.entrada_acumulada.clear()
        self.hechos_acumulados.clear()
        self.observaciones.clear()
        self.ultimo_resultado = None

    def obtener_estado(self):
        """Devuelve una copia del estado para mostrarlo sin exponer mutabilidad."""
        return {
            "etapa_actual": self.etapa_actual,
            "historial": deepcopy(self.historial),
            "entrada_acumulada": deepcopy(self.entrada_acumulada),
            "hechos_acumulados": deepcopy(self.hechos_acumulados),
            "observaciones": list(self.observaciones),
            "ultimo_resultado": deepcopy(self.ultimo_resultado),
        }

    @classmethod
    def _validar_etapa(cls, etapa):
        if isinstance(etapa, bool) or not isinstance(etapa, int):
            raise ValueError("La etapa debe ser un entero entre 1 y 4.")
        if not cls.ETAPA_MINIMA <= etapa <= cls.ETAPA_MAXIMA:
            raise ValueError("La etapa debe estar entre 1 y 4.")
