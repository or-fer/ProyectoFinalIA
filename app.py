"""Interfaz grafica en Tkinter para el sistema experto de diagnostico de hardware."""
import tkinter as tk
from tkinter import ttk

from motor_inferencia import CATEGORICOS, diagnosticar, formatear_resultado


class AplicacionDiagnostico(tk.Tk):
    """Interfaz de datos estructurados; el texto libre solo usa el normalizador actual."""

    def __init__(self):
        super().__init__()
        self.title("Diagnóstico de fallas en hardware - Sistema experto")
        self.geometry("1020x680")
        self.minsize(920, 620)

        self.entradas = {}
        self._construir_interfaz()

    def _construir_interfaz(self):
        contenedor = ttk.Frame(self, padding=10)
        contenedor.pack(fill="both", expand=True)
        contenedor.columnconfigure(0, weight=1)
        contenedor.columnconfigure(1, weight=1)
        contenedor.rowconfigure(0, weight=1)

        panel_izq = ttk.Frame(contenedor)
        panel_izq.grid(row=0, column=0, sticky="nsew", padx=(0, 8))

        panel_der = ttk.Frame(contenedor)
        panel_der.grid(row=0, column=1, sticky="nsew")
        panel_der.rowconfigure(1, weight=1)
        panel_der.columnconfigure(0, weight=1)

        # Seccion 1: Alimentacion y potencia
        sec1 = ttk.LabelFrame(panel_izq, text="1. Alimentación y potencia", padding=8)
        sec1.pack(fill="x", pady=(0, 6))
        self._agregar_campo(sec1, 0, "Voltaje de la toma AC (V)", "v_ac", "texto")
        self._agregar_campo(sec1, 1, "¿Hay continuidad en el fusible?", "fusible_continuidad", "combo")
        self._agregar_campo(sec1, 2, "Riel de 12 V (V)", "v_12", "texto")
        self._agregar_campo(sec1, 3, "Riel de 5 V (V)", "v_5", "texto")
        self._agregar_campo(sec1, 4, "Riel de 3.3 V (V)", "v_3_3", "texto")
        self._agregar_campo(sec1, 5, "¿Huele a quemado?", "olor_quemado", "combo")

        # Seccion 2: Arranque y logica digital
        sec2 = ttk.LabelFrame(panel_izq, text="2. Arranque y lógica digital", padding=8)
        sec2.pack(fill="x", pady=(0, 6))
        self._agregar_campo(sec2, 0, "¿Enciende el LED de encendido?", "led_encendido", "combo")
        self._agregar_campo(sec2, 1, "¿Giran los ventiladores?", "ventiladores", "combo")
        self._agregar_campo(sec2, 2, "¿Hay señal de video?", "video", "combo")
        self._agregar_campo(sec2, 3, "Patrón de pitidos", "beeps", "combo")
        self._agregar_campo(sec2, 4, "Temperatura del CPU (°C)", "temp_cpu", "texto")

        # Seccion 3: Conectividad y perifericos
        sec3 = ttk.LabelFrame(panel_izq, text="3. Conectividad y periféricos", padding=8)
        sec3.pack(fill="x", pady=(0, 6))
        self._agregar_campo(sec3, 0, "¿Se detecta la red?", "red_detectada", "combo")
        self._agregar_campo(sec3, 1, "¿Enciende el LED del puerto de red?", "led_puerto_red", "combo")
        self._agregar_campo(sec3, 2, "¿Hay continuidad en el cable de red?", "continuidad_cable_red", "combo")
        self._agregar_campo(sec3, 3, "¿Responden los periféricos USB?", "usb_responde", "combo")

        # Observaciones
        ttk.Label(panel_izq, text="Observaciones (opcional):").pack(anchor="w")
        self.txt_obs = tk.Text(panel_izq, height=3, width=45, wrap="word")
        self.txt_obs.pack(fill="x", pady=(2, 8))

        # Botones
        barra_btn = ttk.Frame(panel_izq)
        barra_btn.pack(anchor="w")
        ttk.Button(barra_btn, text="Diagnosticar", command=self.ejecutar_diagnostico).pack(side="left", padx=(0, 6))
        ttk.Button(barra_btn, text="Limpiar", command=self.limpiar).pack(side="left")

        # Panel derecho: Resultado
        ttk.Label(panel_der, text="Resultado").grid(row=0, column=0, sticky="w")
        self.txt_res = tk.Text(panel_der, wrap="word", state="disabled")
        self.txt_res.grid(row=1, column=0, sticky="nsew", pady=(2, 0))

        scroll = ttk.Scrollbar(panel_der, orient="vertical", command=self.txt_res.yview)
        scroll.grid(row=1, column=1, sticky="ns")
        self.txt_res.configure(yscrollcommand=scroll.set)

    def _agregar_campo(self, padre, fila, etiqueta, clave, tipo):
        padre.columnconfigure(0, weight=1)
        padre.columnconfigure(1, weight=1)
        ttk.Label(padre, text=etiqueta).grid(row=fila, column=0, sticky="w", pady=2)
        if tipo == "texto":
            var = tk.StringVar()
            ttk.Entry(padre, textvariable=var, width=24).grid(row=fila, column=1, sticky="ew", pady=2)
        else:
            var = tk.StringVar()
            opciones = [""] + CATEGORICOS[clave]
            combo = ttk.Combobox(padre, textvariable=var, values=opciones, state="readonly", width=22)
            combo.grid(row=fila, column=1, sticky="ew", pady=2)
        self.entradas[clave] = var

    def ejecutar_diagnostico(self):
        datos = {k: v.get() for k, v in self.entradas.items()}
        observaciones = self.txt_obs.get("1.0", "end").strip()
        resultado = diagnosticar(datos, observaciones)
        salida = formatear_resultado(resultado)

        self.txt_res.configure(state="normal")
        self.txt_res.delete("1.0", "end")
        self.txt_res.insert("1.0", salida)
        self.txt_res.configure(state="disabled")

    def limpiar(self):
        for var in self.entradas.values():
            var.set("")
        self.txt_obs.delete("1.0", "end")
        self.txt_res.configure(state="normal")
        self.txt_res.delete("1.0", "end")
        self.txt_res.configure(state="disabled")


if __name__ == "__main__":
    app = AplicacionDiagnostico()
    app.mainloop()
