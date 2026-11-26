"""Interfaz grafica conversacional en Tkinter con diseno organico y bordes redondeados.

Integra GestorSesion para mantener memoria de sesion a lo largo de 4 etapas:
  1. Deteccion inicial (sintomas en lenguaje libre o botones rapidos)
  2. Analisis tecnico (mediciones electricas, sintomas y observaciones con bloqueo inteligente)
  3. Solucion y verificacion (explicacion de reglas, CF, pasos y seguridad)
  4. Compra y convenios (catalogo de refacciones/herramientas con descuento)
"""
import json
import os
import tkinter as tk
from tkinter import scrolledtext, ttk

from gestor_sesion import GestorSesion
from motor_inferencia import CATEGORICOS, NUMERICOS

RUTA_CONVENIOS = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "convenios_refacciones.json"
)

# Paleta organica suave (tonos lavanda, salvia y crepusculo)
PALETA = {
    "fondo_app": "#F5F3FA",         # Lavanda muy tenue, suave a la vista
    "tarjeta_bg": "#FFFFFF",        # Blanco puro para tarjetas principales
    "tarjeta_borde": "#E2DCF0",     # Borde lila pastel sutil
    "tarjeta_suave": "#FAF8FE",     # Fondo secundario dentro de tarjetas
    "campo_bloqueado": "#EFECEF",   # Fondo sutil para controles deshabilitados
    "primario": "#7C5DFA",          # Violeta organico principal
    "primario_hover": "#6746EB",    # Hover del boton principal
    "primario_suave": "#EDE9FE",    # Relleno pastel para etapas completadas
    "primario_texto": "#4C35B5",    # Texto oscuro sobre fondo pastel
    "secundario_bg": "#EFEBF8",     # Botones secundarios suaves
    "secundario_hover": "#E2DAF3",
    "secundario_fg": "#3B3355",
    "texto_principal": "#231F33",
    "texto_secundario": "#686180",
    "texto_bloqueado": "#A39EB5",
    "chat_bot_bg": "#F4F1FC",       # Burbuja suave del asistente
    "chat_usr_bg": "#E9F7F2",       # Burbuja verde salvia suave del usuario
    "alerta_bg": "#FDECEF",         # Rosa coral suave para peligro critico
    "alerta_fg": "#9F1D35",
    "aviso_bg": "#FEF6E6",          # Ambar calido para advertencias
    "aviso_fg": "#8A5300",
    "convenio_bg": "#E8F8F2",       # Menta organico para cupones y convenios
    "convenio_fg": "#116149",
    # Panel derecho (Memoria Viva en tono crepusculo profundo)
    "mem_bg": "#1F1D2E",
    "mem_borde": "#393552",
    "mem_titulo": "#C4A7E7",
    "mem_texto": "#E0DEF4",
    "mem_ok": "#9CCFD8",
    "mem_dato": "#F6C177",
    "mem_alerta": "#EB6F92",
}

CONVENIOS_RESPALDO = {
    "D_AC": {
        "articulo": "Multimetro digital TRMS + Regulador/Supresor de picos (1200 VA)",
        "tienda": "Casa de la Tecnologia Centro / Steren Aliado",
        "descuento": "15% con codigo UNAM-HW15",
        "costo_estimado": "$480 - $750 MXN",
        "nota": "Ideal para verificar estabilidad de linea AC y proteger la fuente.",
    },
    "D_FUS": {
        "articulo": "Fuente de poder certificada 80+ Bronze (550W - 650W)",
        "tienda": "CyberTech & Refacciones CU",
        "descuento": "12% en reemplazo directo + diagnostico gratis",
        "costo_estimado": "$950 - $1,350 MXN",
        "nota": "No se recomienda reparar etapa primaria; sustituye la unidad completa.",
    },
    "D_PSU": {
        "articulo": "Probador digital de fuentes ATX + Fuente 80+ Bronze 600W",
        "tienda": "CyberTech & Refacciones CU",
        "descuento": "12% con codigo FIX-PSU12",
        "costo_estimado": "$1,050 - $1,450 MXN",
        "nota": "Permite validar rieles bajo carga y reemplazar la fuente degradada.",
    },
    "D_PSU_ALTO": {
        "articulo": "Fuente de poder certificada 80+ Bronze/Gold con proteccion OVP",
        "tienda": "PC Componentes & Soporte Aliado",
        "descuento": "15% por reemplazo urgente de seguridad",
        "costo_estimado": "$1,150 - $1,600 MXN",
        "nota": "Reemplazo prioritario: la proteccion OVP evita dano a tarjeta madre y discos.",
    },
    "D_QUEMADO": {
        "articulo": "Kit de aislamiento (pulsera antiestatica, alcohol isopropilico y fuente)",
        "tienda": "Electronica & Hardware del Sur",
        "descuento": "10% en kit de mantenimiento + revision de placa",
        "costo_estimado": "$320 - $1,200 MXN",
        "nota": "Desconecta el equipo antes de retirar componentes danados.",
    },
    "D_BTN": {
        "articulo": "Switch pulsador ATX de reemplazo / Kit destornilladores aislados",
        "tienda": "Casa de la Tecnologia Centro",
        "descuento": "10% con codigo PANEL-10",
        "costo_estimado": "$120 - $280 MXN",
        "nota": "Util para descartar falso contacto en PWR_SW o boton del gabinete.",
    },
    "D_RAM": {
        "articulo": "Modulo de memoria RAM compatible (DDR4/DDR5) + Alcohol isopropilico",
        "tienda": "PC Componentes & Soporte Aliado",
        "descuento": "10% en memorias RAM + limpieza de ranuras sin costo",
        "costo_estimado": "$450 - $950 MXN",
        "nota": "Verifica frecuencia y generacion soportada por tu tarjeta madre.",
    },
    "D_GPU": {
        "articulo": "Tarjeta grafica de reemplazo / Adaptador de video + Aire comprimido",
        "tienda": "PC Componentes & Soporte Aliado",
        "descuento": "8% en tarjetas de video seleccionadas",
        "costo_estimado": "$1,800 - $4,500 MXN",
        "nota": "Confirma capacidad de watts de tu fuente antes de instalar.",
    },
    "D_MON": {
        "articulo": "Cable HDMI 2.1 / DisplayPort certificado blindado",
        "tienda": "Steren Aliado / CyberTech CU",
        "descuento": "15% en cables de video",
        "costo_estimado": "$140 - $290 MXN",
        "nota": "Descarta falsos contactos de senal antes de intervenir el gabinete.",
    },
    "D_CPU_MB": {
        "articulo": "Bateria CMOS CR2032 + Pasta termica + Servicio de diagnostico POST",
        "tienda": "Taller Especializado Hardware Pro",
        "descuento": "20% en diagnostico de placa madre y socket",
        "costo_estimado": "$180 - $600 MXN",
        "nota": "Incluye reinicio de CMOS y verificacion de pines de CPU.",
    },
    "D_TERM": {
        "articulo": "Pasta termica de alta conductividad + Kit limpieza + Ventilador CPU",
        "tienda": "CyberTech & Refacciones CU",
        "descuento": "15% en kit termico (Codigo COOL-15)",
        "costo_estimado": "$190 - $550 MXN",
        "nota": "Reduce entre 10 °C y 25 °C en equipos con pasta seca o polvo acumulado.",
    },
    "D_SOFT": {
        "articulo": "Unidad SSD de respaldo (500 GB / 1 TB) + Memoria USB de diagnostico",
        "tienda": "PC Componentes & Soporte Aliado",
        "descuento": "10% en unidades SSD para respaldo preventivo",
        "costo_estimado": "$650 - $1,150 MXN",
        "nota": "Respalda tu informacion antes de ejecutar pruebas intensivas de disco.",
    },
    "D_RED_CABLE": {
        "articulo": "Cable Patch Cord UTP Cat 6 certificado + Probador de red RJ-45",
        "tienda": "Steren Aliado / Casa de la Tecnologia",
        "descuento": "15% en cableado estructurado",
        "costo_estimado": "$90 - $260 MXN",
        "nota": "Soluciona perdida de enlace fisico por pares abiertos o ponchado defectuoso.",
    },
    "D_RED_NIC": {
        "articulo": "Adaptador USB 3.0 a Gigabit Ethernet / Tarjeta PCIe de red",
        "tienda": "CyberTech & Refacciones CU",
        "descuento": "12% con codigo NET-12",
        "costo_estimado": "$240 - $420 MXN",
        "nota": "Alternativa inmediata si el puerto integrado de la placa dano su controlador.",
    },
    "D_USB": {
        "articulo": "Hub USB 3.0 con alimentacion externa / Tarjeta expansion PCIe USB",
        "tienda": "Casa de la Tecnologia Centro",
        "descuento": "10% en expansion de puertos",
        "costo_estimado": "$280 - $490 MXN",
        "nota": "Evita sobrecargar los puertos frontales de la tarjeta madre.",
    },
}

NOMBRES_ETAPAS = {
    1: "1. Detección",
    2: "2. Análisis",
    3: "3. Solución",
    4: "4. Convenios",
}

ETIQUETAS_CAMPOS = {
    "v_ac": "Toma AC (V)",
    "fusible_continuidad": "Continuidad fusible",
    "v_12": "Riel +12 V",
    "v_5": "Riel +5 V",
    "v_3_3": "Riel +3.3 V",
    "olor_quemado": "Olor a quemado",
    "led_encendido": "LED encendido",
    "ventiladores": "Ventiladores giran",
    "video": "Señal de video",
    "beeps": "Pitidos POST",
    "temp_cpu": "Temp. CPU (°C)",
    "red_detectada": "Red detectada",
    "led_puerto_red": "LED puerto red",
    "continuidad_cable_red": "Continuidad cable red",
    "usb_responde": "Periféricos USB",
}


def _puntos_rectangulo_redondeado(x1, y1, x2, y2, radio):
    """Genera los vertices suavizados para dibujar un rectangulo con esquinas redondas."""
    r = max(2, min(radio, (x2 - x1) / 2, (y2 - y1) / 2))
    return [
        x1 + r, y1,
        x2 - r, y1,
        x2, y1,
        x2, y1 + r,
        x2, y2 - r,
        x2, y2,
        x2 - r, y2,
        x1 + r, y2,
        x1, y2,
        x1, y2 - r,
        x1, y1 + r,
        x1, y1,
    ]


class TarjetaRedondeada(tk.Canvas):
    """Contenedor con esquinas redondeadas suaves basado en Canvas de Tkinter."""

    def __init__(
        self,
        parent,
        bg_exterior,
        bg_tarjeta=PALETA["tarjeta_bg"],
        borde=PALETA["tarjeta_borde"],
        radio=18,
        padding=12,
        **kwargs,
    ):
        super().__init__(
            parent,
            bg=bg_exterior,
            highlightthickness=0,
            bd=0,
            **kwargs,
        )
        self.bg_tarjeta = bg_tarjeta
        self.borde = borde
        self.radio = radio
        self.padding = padding

        self.interior = tk.Frame(self, bg=bg_tarjeta, bd=0, highlightthickness=0)
        self._win_id = self.create_window(padding, padding, window=self.interior, anchor="nw")
        self.bind("<Configure>", self._redibujar)

    def ajustar_altura_contenido(self):
        """Adapta la altura de la tarjeta al alto real requerido por sus widgets."""
        self.interior.update_idletasks()
        alto_req = self.interior.winfo_reqheight() + (2 * self.padding) + 4
        if alto_req > 20:
            self.configure(height=alto_req)
            self._redibujar()

    def _redibujar(self, event=None):
        w = self.winfo_width()
        h = self.winfo_height()
        if w < 10 or h < 10:
            return
        self.delete("fondo_tarjeta")
        pts = _puntos_rectangulo_redondeado(1, 1, w - 2, h - 2, self.radio)
        self.create_polygon(
            pts,
            smooth=True,
            fill=self.bg_tarjeta,
            outline=self.borde,
            width=1.5,
            tags="fondo_tarjeta",
        )
        self.tag_lower("fondo_tarjeta")
        inner_w = max(1, w - 2 * self.padding)
        inner_h = max(1, h - 2 * self.padding)
        self.coords(self._win_id, self.padding, self.padding)
        self.itemconfigure(self._win_id, width=inner_w, height=inner_h)


class BotonRedondeado(tk.Canvas):
    """Boton organico tipo pildora con esquinas redondas, estados y efecto hover."""

    def __init__(
        self,
        parent,
        texto,
        comando=None,
        bg_exterior=PALETA["tarjeta_bg"],
        bg_normal=PALETA["secundario_bg"],
        bg_hover=PALETA["secundario_hover"],
        fg_texto=PALETA["secundario_fg"],
        borde="",
        radio=14,
        altura=34,
        ancho=130,
        fuente=("Segoe UI", 9, "bold"),
    ):
        super().__init__(
            parent,
            width=ancho,
            height=altura,
            bg=bg_exterior,
            highlightthickness=0,
            bd=0,
            cursor="hand2",
        )
        self.texto = texto
        self.comando = comando
        self.bg_normal = bg_normal
        self.bg_hover = bg_hover
        self.fg_texto = fg_texto
        self.borde = borde
        self.radio = radio
        self.fuente = fuente
        self._hover = False

        self.bind("<Configure>", lambda _e: self._dibujar())
        self.bind("<Enter>", self._on_enter)
        self.bind("<Leave>", self._on_leave)
        self.bind("<ButtonRelease-1>", self._on_click)

    def configurar_colores(self, bg_normal, bg_hover, fg_texto, borde=""):
        self.bg_normal = bg_normal
        self.bg_hover = bg_hover
        self.fg_texto = fg_texto
        self.borde = borde
        self._dibujar()

    def _on_enter(self, _e):
        self._hover = True
        self._dibujar()

    def _on_leave(self, _e):
        self._hover = False
        self._dibujar()

    def _on_click(self, _e):
        if callable(self.comando):
            self.comando()

    def _dibujar(self):
        w = self.winfo_width()
        h = self.winfo_height()
        if w < 6 or h < 6:
            return
        self.delete("all")
        relleno = self.bg_hover if self._hover else self.bg_normal
        pts = _puntos_rectangulo_redondeado(1, 1, w - 2, h - 2, self.radio)
        self.create_polygon(
            pts,
            smooth=True,
            fill=relleno,
            outline=self.borde if self.borde else relleno,
            width=1.2,
        )
        self.create_text(
            w / 2,
            h / 2,
            text=self.texto,
            fill=self.fg_texto,
            font=self.fuente,
        )


class AplicacionDiagnostico(tk.Tk):
    """Chatbot hibrido en Tkinter con memoria de sesion y formulario inteligente."""

    def __init__(self):
        super().__init__()
        self.title("Asistente Experto de Diagnóstico de Hardware — IA Híbrida")
        self.geometry("1280x860")
        self.minsize(1100, 740)
        self.configure(bg=PALETA["fondo_app"])

        self.gestor_sesion = GestorSesion(etapa_inicial=1)
        self.convenios = self._cargar_convenios()
        self.entradas = {}
        self.widgets_etapa2 = {}
        self.labels_etapa2 = {}
        self._actualizando_reglas_form = False
        self.alerta_critica_activa = None

        self._configurar_tema_ttk()
        self._construir_interfaz()
        self._mostrar_bienvenida()
        self._actualizar_panel_memoria()

    def _configurar_tema_ttk(self):
        estilo = ttk.Style(self)
        if "clam" in estilo.theme_names():
            estilo.theme_use("clam")
        estilo.configure(
            "Organico.TEntry",
            fieldbackground=PALETA["tarjeta_suave"],
            foreground=PALETA["texto_principal"],
            bordercolor=PALETA["tarjeta_borde"],
            lightcolor=PALETA["primario"],
            darkcolor=PALETA["tarjeta_borde"],
            padding=4,
        )
        estilo.map(
            "Organico.TEntry",
            fieldbackground=[("disabled", PALETA["campo_bloqueado"])],
            foreground=[("disabled", PALETA["texto_bloqueado"])],
        )
        estilo.configure(
            "Organico.TCombobox",
            fieldbackground=PALETA["tarjeta_suave"],
            background=PALETA["secundario_bg"],
            foreground=PALETA["texto_principal"],
            bordercolor=PALETA["tarjeta_borde"],
            arrowcolor=PALETA["primario"],
            padding=4,
        )
        estilo.map(
            "Organico.TCombobox",
            fieldbackground=[
                ("disabled", PALETA["campo_bloqueado"]),
                ("readonly", PALETA["tarjeta_suave"]),
            ],
            foreground=[
                ("disabled", PALETA["texto_bloqueado"]),
                ("readonly", PALETA["texto_principal"]),
            ],
        )

    def _cargar_convenios(self):
        """Carga convenios_refacciones.json si existe; si no, usa el respaldo."""
        if os.path.exists(RUTA_CONVENIOS):
            try:
                with open(RUTA_CONVENIOS, encoding="utf-8") as f:
                    data = json.load(f)
                if isinstance(data, dict) and data:
                    return data
            except (OSError, json.JSONDecodeError):
                pass
        return CONVENIOS_RESPALDO

    def _construir_interfaz(self):
        contenedor = tk.Frame(self, bg=PALETA["fondo_app"], padx=14, pady=12)
        contenedor.pack(fill="both", expand=True)
        contenedor.columnconfigure(0, weight=7)
        contenedor.columnconfigure(1, weight=4)
        contenedor.rowconfigure(0, weight=1)

        # ==================== COLUMNA IZQUIERDA: CHAT Y CONTROLES ====================
        panel_izq = tk.Frame(contenedor, bg=PALETA["fondo_app"])
        panel_izq.grid(row=0, column=0, sticky="nsew", padx=(0, 12))
        panel_izq.rowconfigure(1, weight=1)
        panel_izq.columnconfigure(0, weight=1)

        # 1. Tarjeta superior de etapas (stepper redondeado)
        card_etapas = TarjetaRedondeada(
            panel_izq,
            bg_exterior=PALETA["fondo_app"],
            bg_tarjeta=PALETA["tarjeta_bg"],
            borde=PALETA["tarjeta_borde"],
            radio=18,
            padding=8,
            height=54,
        )
        card_etapas.grid(row=0, column=0, sticky="ew", pady=(0, 8))

        self.botones_etapa = {}
        for idx, (num, nombre) in enumerate(NOMBRES_ETAPAS.items()):
            card_etapas.interior.columnconfigure(idx, weight=1)
            btn = BotonRedondeado(
                card_etapas.interior,
                texto=nombre,
                comando=lambda n=num: self._cambiar_etapa_manual(n),
                bg_exterior=PALETA["tarjeta_bg"],
                altura=34,
                ancho=140,
                radio=15,
            )
            btn.grid(row=0, column=idx, sticky="ew", padx=3)
            self.botones_etapa[num] = btn

        # 2. Tarjeta central de conversacion (chat redondeado)
        card_chat = TarjetaRedondeada(
            panel_izq,
            bg_exterior=PALETA["fondo_app"],
            bg_tarjeta=PALETA["tarjeta_bg"],
            borde=PALETA["tarjeta_borde"],
            radio=22,
            padding=12,
        )
        card_chat.grid(row=1, column=0, sticky="nsew", pady=(0, 8))
        card_chat.interior.rowconfigure(0, weight=1)
        card_chat.interior.columnconfigure(0, weight=1)

        self.chat_box = scrolledtext.ScrolledText(
            card_chat.interior,
            wrap="word",
            font=("Segoe UI", 10),
            bg=PALETA["tarjeta_bg"],
            fg=PALETA["texto_principal"],
            padx=8,
            pady=6,
            state="disabled",
            relief="flat",
            bd=0,
            highlightthickness=0,
        )
        self.chat_box.grid(row=0, column=0, sticky="nsew")
        self._configurar_estilos_chat()

        # 3. Tarjeta dinamica de controles por etapa (autoajustable en altura)
        self.card_dinamica = TarjetaRedondeada(
            panel_izq,
            bg_exterior=PALETA["fondo_app"],
            bg_tarjeta=PALETA["tarjeta_bg"],
            borde=PALETA["tarjeta_borde"],
            radio=20,
            padding=12,
            height=110,
        )
        self.card_dinamica.grid(row=2, column=0, sticky="ew", pady=(0, 8))
        self.panel_dinamico = self.card_dinamica.interior
        self.panel_dinamico.columnconfigure(0, weight=1)

        # 4. Barra inferior redondeada de chat libre
        card_input = TarjetaRedondeada(
            panel_izq,
            bg_exterior=PALETA["fondo_app"],
            bg_tarjeta=PALETA["tarjeta_bg"],
            borde=PALETA["tarjeta_borde"],
            radio=20,
            padding=7,
            height=52,
        )
        card_input.grid(row=3, column=0, sticky="ew")
        card_input.interior.columnconfigure(0, weight=1)

        self.var_mensaje = tk.StringVar()
        self.entry_mensaje = tk.Entry(
            card_input.interior,
            textvariable=self.var_mensaje,
            font=("Segoe UI", 10),
            bg=PALETA["tarjeta_suave"],
            fg=PALETA["texto_principal"],
            insertbackground=PALETA["primario"],
            relief="flat",
            bd=6,
        )
        self.entry_mensaje.grid(row=0, column=0, sticky="ew", padx=(4, 8))
        self.entry_mensaje.bind("<Return>", lambda _e: self.enviar_mensaje_libre())

        BotonRedondeado(
            card_input.interior,
            texto="Enviar",
            comando=self.enviar_mensaje_libre,
            bg_exterior=PALETA["tarjeta_bg"],
            bg_normal=PALETA["primario"],
            bg_hover=PALETA["primario_hover"],
            fg_texto="#FFFFFF",
            altura=34,
            ancho=96,
            radio=15,
        ).grid(row=0, column=1, padx=(0, 6))

        BotonRedondeado(
            card_input.interior,
            texto="Reiniciar",
            comando=self.reiniciar_sesion,
            bg_exterior=PALETA["tarjeta_bg"],
            bg_normal=PALETA["secundario_bg"],
            bg_hover=PALETA["secundario_hover"],
            fg_texto=PALETA["secundario_fg"],
            altura=34,
            ancho=96,
            radio=15,
        ).grid(row=0, column=2)

        # ==================== COLUMNA DERECHA: MEMORIA VIVA ====================
        card_memoria = TarjetaRedondeada(
            contenedor,
            bg_exterior=PALETA["fondo_app"],
            bg_tarjeta=PALETA["mem_bg"],
            borde=PALETA["mem_borde"],
            radio=22,
            padding=14,
        )
        card_memoria.grid(row=0, column=1, sticky="nsew")
        card_memoria.interior.rowconfigure(1, weight=1)
        card_memoria.interior.columnconfigure(0, weight=1)

        encabezado_mem = tk.Label(
            card_memoria.interior,
            text="✦ Memoria Viva de la Sesión",
            font=("Segoe UI", 11, "bold"),
            bg=PALETA["mem_bg"],
            fg=PALETA["mem_titulo"],
            anchor="w",
        )
        encabezado_mem.grid(row=0, column=0, sticky="ew", pady=(0, 8))

        self.memoria_box = scrolledtext.ScrolledText(
            card_memoria.interior,
            wrap="word",
            font=("Consolas", 9),
            bg=PALETA["mem_bg"],
            fg=PALETA["mem_texto"],
            padx=4,
            pady=4,
            state="disabled",
            relief="flat",
            bd=0,
            highlightthickness=0,
        )
        self.memoria_box.grid(row=1, column=0, sticky="nsew")
        self.memoria_box.tag_configure(
            "titulo", foreground=PALETA["mem_titulo"], font=("Consolas", 9, "bold")
        )
        self.memoria_box.tag_configure("ok", foreground=PALETA["mem_ok"])
        self.memoria_box.tag_configure(
            "alerta", foreground=PALETA["mem_alerta"], font=("Consolas", 9, "bold")
        )
        self.memoria_box.tag_configure("dato", foreground=PALETA["mem_dato"])

        self._renderizar_controles_etapa()

    def _configurar_estilos_chat(self):
        self.chat_box.tag_configure(
            "bot_nombre",
            foreground=PALETA["primario"],
            font=("Segoe UI", 9, "bold"),
            spacing1=6,
            lmargin1=6,
        )
        self.chat_box.tag_configure(
            "bot_texto",
            background=PALETA["chat_bot_bg"],
            foreground=PALETA["texto_principal"],
            font=("Segoe UI", 10),
            lmargin1=12,
            lmargin2=12,
            rmargin=28,
            spacing1=4,
            spacing3=8,
        )
        self.chat_box.tag_configure(
            "usr_nombre",
            foreground=PALETA["convenio_fg"],
            font=("Segoe UI", 9, "bold"),
            spacing1=6,
            lmargin1=36,
        )
        self.chat_box.tag_configure(
            "usr_texto",
            background=PALETA["chat_usr_bg"],
            foreground=PALETA["texto_principal"],
            font=("Segoe UI", 10),
            lmargin1=36,
            lmargin2=36,
            rmargin=10,
            spacing1=4,
            spacing3=8,
        )
        self.chat_box.tag_configure(
            "alerta_critica",
            background=PALETA["alerta_bg"],
            foreground=PALETA["alerta_fg"],
            font=("Segoe UI", 10, "bold"),
            lmargin1=12,
            lmargin2=12,
            rmargin=18,
            spacing1=6,
            spacing3=10,
        )
        self.chat_box.tag_configure(
            "advertencia",
            background=PALETA["aviso_bg"],
            foreground=PALETA["aviso_fg"],
            font=("Segoe UI", 9, "bold"),
            lmargin1=12,
            lmargin2=12,
            rmargin=18,
            spacing1=5,
            spacing3=8,
        )
        self.chat_box.tag_configure(
            "diagnostico",
            background=PALETA["primario_suave"],
            foreground=PALETA["primario_texto"],
            font=("Segoe UI", 10, "bold"),
            lmargin1=12,
            lmargin2=12,
            rmargin=18,
            spacing1=6,
            spacing3=10,
        )
        self.chat_box.tag_configure(
            "convenio",
            background=PALETA["convenio_bg"],
            foreground=PALETA["convenio_fg"],
            font=("Segoe UI", 10, "bold"),
            lmargin1=12,
            lmargin2=12,
            rmargin=18,
            spacing1=6,
            spacing3=10,
        )
        self.chat_box.tag_configure(
            "razonamiento",
            background="#F1F5F9",
            foreground="#334155",
            font=("Consolas", 9),
            lmargin1=12,
            lmargin2=12,
            rmargin=18,
            spacing1=5,
            spacing3=8,
        )

    def _escribir_chat(self, remitente, mensaje, tag_texto="bot_texto"):
        self.chat_box.configure(state="normal")
        if remitente == "Asistente":
            self.chat_box.insert("end", "● Asistente IA\n", "bot_nombre")
        elif remitente == "Tú":
            self.chat_box.insert("end", "● Tú\n", "usr_nombre")
        self.chat_box.insert("end", f"{mensaje.strip()}\n", tag_texto)
        self.chat_box.insert("end", "\n")
        self.chat_box.see("end")
        self.chat_box.configure(state="disabled")
        self.chat_box.update_idletasks()
        self.chat_box.yview_moveto(1.0)

    def _mostrar_bienvenida(self):
        bienvenida = (
            "¡Hola! Soy tu asistente experto de diagnóstico de hardware.\n"
            "Avanzaremos juntos en 4 etapas con memoria continua: "
            "Detección → Análisis → Solución → Convenios.\n\n"
            "Elige un síntoma rápido abajo o cuéntame qué le pasa a tu equipo en la barra inferior."
        )
        self._escribir_chat("Asistente", bienvenida)

    # ==================== CONTROLES ADAPTATIVOS POR ETAPA ====================

    def _obtener_var_campo(self, clave):
        """Obtiene o crea la StringVar del campo con listener reactivo para bloqueo tipo Forms."""
        if clave not in self.entradas:
            var = tk.StringVar()
            var.trace_add("write", lambda *_args: self._actualizar_estado_formulario_etapa2())
            self.entradas[clave] = var
        return self.entradas[clave]

    def _renderizar_controles_etapa(self):
        for widget in self.panel_dinamico.winfo_children():
            widget.destroy()

        etapa = self.gestor_sesion.etapa_actual
        for num, btn in self.botones_etapa.items():
            if num == etapa:
                btn.configurar_colores(
                    bg_normal=PALETA["primario"],
                    bg_hover=PALETA["primario_hover"],
                    fg_texto="#FFFFFF",
                )
            elif num < etapa:
                btn.configurar_colores(
                    bg_normal=PALETA["primario_suave"],
                    bg_hover="#DDD6FE",
                    fg_texto=PALETA["primario_texto"],
                )
            else:
                btn.configurar_colores(
                    bg_normal=PALETA["secundario_bg"],
                    bg_hover=PALETA["secundario_hover"],
                    fg_texto=PALETA["texto_secundario"],
                )

        if etapa == 1:
            self._construir_controles_etapa_1()
        elif etapa == 2:
            self._construir_controles_etapa_2()
        elif etapa == 3:
            self._construir_controles_etapa_3()
        else:
            self._construir_controles_etapa_4()

        # Ajustar automaticamente la altura exacta de la tarjeta al contenido renderizado
        self.card_dinamica.ajustar_altura_contenido()
        self.after_idle(self.card_dinamica.ajustar_altura_contenido)

    def _construir_controles_etapa_1(self):
        tk.Label(
            self.panel_dinamico,
            text="Etapa 1 — Detección rápida (elige un escenario o escríbelo abajo):",
            font=("Segoe UI", 9, "bold"),
            bg=PALETA["tarjeta_bg"],
            fg=PALETA["texto_principal"],
        ).pack(anchor="w", pady=(0, 8))

        fila = tk.Frame(self.panel_dinamico, bg=PALETA["tarjeta_bg"])
        fila.pack(fill="x")

        presets = [
            (
                "No enciende nada",
                {"led_encendido": "no", "ventiladores": "no"},
                "El equipo no enciende ni prende el LED.",
            ),
            (
                "Gira sin dar video",
                {"led_encendido": "si", "ventiladores": "si", "video": "no"},
                "Prenden los ventiladores pero no da video en pantalla.",
            ),
            (
                "Pantalla azul / reinicios",
                {"led_encendido": "si", "ventiladores": "si", "video": "si"},
                "El equipo se reinicia y me sale pantalla azul.",
            ),
            (
                "Falla red o USB",
                {"red_detectada": "no", "usb_responde": "no"},
                "No detecta internet ni responden los puertos USB.",
            ),
        ]
        for idx, (texto_btn, datos_preset, frase) in enumerate(presets):
            fila.columnconfigure(idx, weight=1)
            BotonRedondeado(
                fila,
                texto=texto_btn,
                comando=lambda d=datos_preset, f=frase: self._aplicar_preset_etapa_1(d, f),
                bg_exterior=PALETA["tarjeta_bg"],
                bg_normal=PALETA["primario_suave"],
                bg_hover="#DDD6FE",
                fg_texto=PALETA["primario_texto"],
                altura=34,
                ancho=145,
                radio=15,
            ).grid(row=0, column=idx, sticky="ew", padx=3)

    def _construir_controles_etapa_2(self):
        self.widgets_etapa2 = {}
        self.labels_etapa2 = {}

        # Fila 0: Encabezado con boton 'Limpiar' y boton 'Analizar ->' siempre visible arriba
        f_top = tk.Frame(self.panel_dinamico, bg=PALETA["tarjeta_bg"])
        f_top.grid(row=0, column=0, sticky="ew", pady=(0, 6))
        f_top.columnconfigure(0, weight=1)

        tk.Label(
            f_top,
            text="Etapa 2 — Análisis técnico (deja vacío lo que no hayas medido):",
            font=("Segoe UI", 9, "bold"),
            bg=PALETA["tarjeta_bg"],
            fg=PALETA["texto_principal"],
            anchor="w",
        ).grid(row=0, column=0, sticky="w")

        BotonRedondeado(
            f_top,
            texto="Limpiar",
            comando=self._limpiar_campos_etapa2,
            bg_exterior=PALETA["tarjeta_bg"],
            bg_normal=PALETA["secundario_bg"],
            bg_hover=PALETA["secundario_hover"],
            fg_texto=PALETA["secundario_fg"],
            altura=28,
            ancho=84,
            radio=13,
            fuente=("Segoe UI", 8, "bold"),
        ).grid(row=0, column=1, padx=(0, 6))

        BotonRedondeado(
            f_top,
            texto="Analizar →",
            comando=self.procesar_analisis_etapa_2,
            bg_exterior=PALETA["tarjeta_bg"],
            bg_normal=PALETA["primario"],
            bg_hover=PALETA["primario_hover"],
            fg_texto="#FFFFFF",
            altura=28,
            ancho=106,
            radio=13,
            fuente=("Segoe UI", 9, "bold"),
        ).grid(row=0, column=2)

        # Fila 1: Mediciones numericas distribuidas de forma uniforme (5 columnas responsivas)
        campos_num = [
            ("AC (V):", "v_ac"),
            ("+12V:", "v_12"),
            ("+5V:", "v_5"),
            ("+3.3V:", "v_3_3"),
            ("CPU °C:", "temp_cpu"),
        ]
        f_num = tk.Frame(self.panel_dinamico, bg=PALETA["tarjeta_bg"])
        f_num.grid(row=1, column=0, sticky="ew", pady=(0, 6))
        for idx, (etq, clave) in enumerate(campos_num):
            f_num.columnconfigure(idx * 2 + 1, weight=1)
            lbl = tk.Label(
                f_num,
                text=etq,
                font=("Segoe UI", 9),
                bg=PALETA["tarjeta_bg"],
                fg=PALETA["texto_secundario"],
            )
            lbl.grid(row=0, column=idx * 2, sticky="w", padx=(4, 3))
            var = self._obtener_var_campo(clave)
            ent = ttk.Entry(f_num, textvariable=var, width=6, style="Organico.TEntry")
            ent.grid(row=0, column=idx * 2 + 1, sticky="ew", padx=(0, 8))
            ent.bind("<Return>", lambda _e: self.procesar_analisis_etapa_2())
            self.widgets_etapa2[clave] = ent
            self.labels_etapa2[clave] = lbl

        # Fila 2: Sintomas categoricos en cuadricula holgada (3 columnas x 4 filas)
        campos_cat = [
            ("LED encendido:", "led_encendido"),
            ("Ventiladores:", "ventiladores"),
            ("Video:", "video"),
            ("Pitidos POST:", "beeps"),
            ("Olor quemado:", "olor_quemado"),
            ("Fusible OK:", "fusible_continuidad"),
            ("Red OK:", "red_detectada"),
            ("LED red:", "led_puerto_red"),
            ("Cable red:", "continuidad_cable_red"),
            ("USB OK:", "usb_responde"),
        ]
        f_cat = tk.Frame(self.panel_dinamico, bg=PALETA["tarjeta_bg"])
        f_cat.grid(row=2, column=0, sticky="ew", pady=(0, 6))
        for c in range(3):
            f_cat.columnconfigure(c * 2 + 1, weight=1)

        for idx, (etq, clave) in enumerate(campos_cat):
            col_base = (idx % 3) * 2
            row_base = idx // 3
            lbl = tk.Label(
                f_cat,
                text=etq,
                font=("Segoe UI", 9),
                bg=PALETA["tarjeta_bg"],
                fg=PALETA["texto_secundario"],
            )
            lbl.grid(row=row_base, column=col_base, sticky="w", padx=(4, 4), pady=2)
            var = self._obtener_var_campo(clave)
            combo = ttk.Combobox(
                f_cat,
                textvariable=var,
                values=[""] + CATEGORICOS[clave],
                state="readonly",
                width=18 if clave == "beeps" else 9,
                style="Organico.TCombobox",
            )
            combo.grid(row=row_base, column=col_base + 1, sticky="ew", padx=(0, 10), pady=2)
            self.widgets_etapa2[clave] = combo
            self.labels_etapa2[clave] = lbl

        # Fila 3: Banner de estado inteligente (muestra bloqueos y avisos fisicos en tiempo real)
        self.var_aviso_form = tk.StringVar(
            value="Formulario inteligente activo: los campos incompatibles se bloquean automáticamente."
        )
        self.lbl_aviso_form = tk.Label(
            self.panel_dinamico,
            textvariable=self.var_aviso_form,
            font=("Segoe UI", 8, "italic"),
            bg=PALETA["tarjeta_suave"],
            fg=PALETA["texto_secundario"],
            anchor="w",
            padx=8,
            pady=3,
        )
        self.lbl_aviso_form.grid(row=3, column=0, sticky="ew", pady=(2, 6))

        # Fila 4: Observaciones y boton Analizar (100% visible con altura autoajustable)
        f_obs = tk.Frame(self.panel_dinamico, bg=PALETA["tarjeta_bg"])
        f_obs.grid(row=4, column=0, sticky="ew")
        f_obs.columnconfigure(1, weight=1)
        tk.Label(
            f_obs,
            text="Observaciones:",
            font=("Segoe UI", 9, "bold"),
            bg=PALETA["tarjeta_bg"],
            fg=PALETA["texto_principal"],
        ).grid(row=0, column=0, padx=(4, 6))
        self.var_obs_etapa2 = tk.StringVar()
        ent_obs = ttk.Entry(f_obs, textvariable=self.var_obs_etapa2, style="Organico.TEntry")
        ent_obs.grid(row=0, column=1, sticky="ew", padx=(0, 8))
        ent_obs.bind("<Return>", lambda _e: self.procesar_analisis_etapa_2())

        BotonRedondeado(
            f_obs,
            texto="Analizar →",
            comando=self.procesar_analisis_etapa_2,
            bg_exterior=PALETA["tarjeta_bg"],
            bg_normal=PALETA["primario"],
            bg_hover=PALETA["primario_hover"],
            fg_texto="#FFFFFF",
            altura=32,
            ancho=118,
            radio=14,
        ).grid(row=0, column=2)

        self._actualizar_estado_formulario_etapa2()

    def _limpiar_campos_etapa2(self):
        self._actualizando_reglas_form = True
        try:
            for var in self.entradas.values():
                var.set("")
            if hasattr(self, "var_obs_etapa2"):
                self.var_obs_etapa2.set("")
        finally:
            self._actualizando_reglas_form = False
        self._actualizar_estado_formulario_etapa2()

    def _parsear_float_seguro(self, clave):
        raw = self._obtener_var_campo(clave).get().strip()
        if not raw:
            return None
        try:
            return float(raw.replace(",", "."))
        except ValueError:
            return None

    def _actualizar_estado_formulario_etapa2(self):
        """Logica condicional tipo Forms: habilita, restringe o bloquea campos incompatibles."""
        if self._actualizando_reglas_form or not self.widgets_etapa2:
            return

        self._actualizando_reglas_form = True
        try:
            bloqueados = {}  # campo -> motivo
            avisos_fisicos = []

            v_ac = self._parsear_float_seguro("v_ac")
            v_12 = self._parsear_float_seguro("v_12")
            v_5 = self._parsear_float_seguro("v_5")
            v_3_3 = self._parsear_float_seguro("v_3_3")

            fusible = self._obtener_var_campo("fusible_continuidad").get().strip()
            olor_quemado = self._obtener_var_campo("olor_quemado").get().strip()
            ventiladores = self._obtener_var_campo("ventiladores").get().strip()
            video = self._obtener_var_campo("video").get().strip()
            cable_red = self._obtener_var_campo("continuidad_cable_red").get().strip()
            red_ok = self._obtener_var_campo("red_detectada").get().strip()

            # Regla 1: Sin voltaje AC valido (< 90 V) o fusible abierto -> no hay salidas DC ni encendido
            sin_ac = v_ac is not None and v_ac < 90.0
            sin_fusible = fusible == "no"
            if sin_ac or sin_fusible:
                motivo = (
                    "Sin entrada AC válida (< 90 V)"
                    if sin_ac
                    else "Fusible abierto (sin continuidad)"
                )
                for c in (
                    "v_12",
                    "v_5",
                    "v_3_3",
                    "led_encendido",
                    "ventiladores",
                    "video",
                    "beeps",
                    "temp_cpu",
                    "red_detectada",
                    "led_puerto_red",
                    "usb_responde",
                ):
                    bloqueados[c] = motivo

            # Regla 2: Olor a quemado o sobretension extrema -> bloquear pruebas activas por seguridad
            sobretension_extrema = (
                (v_ac is not None and v_ac > 300.0)
                or (v_12 is not None and v_12 > 20.0)
                or (v_5 is not None and v_5 > 10.0)
                or (v_3_3 is not None and v_3_3 > 6.0)
            )
            if olor_quemado == "si" or sobretension_extrema:
                motivo = (
                    "Olor a quemado detectado (riesgo de daño)"
                    if olor_quemado == "si"
                    else "Sobretensión crítica fuera de escala física"
                )
                for c in (
                    "video",
                    "beeps",
                    "temp_cpu",
                    "red_detectada",
                    "led_puerto_red",
                    "usb_responde",
                ):
                    bloqueados.setdefault(c, motivo)

            # Regla 3: Equipo sin giro de ventiladores -> no llega a POST ni sistema operativo
            if ventiladores == "no":
                motivo = "Equipo sin giro de ventiladores (no llega a POST)"
                for c in (
                    "video",
                    "beeps",
                    "temp_cpu",
                    "red_detectada",
                    "led_puerto_red",
                    "usb_responde",
                ):
                    bloqueados.setdefault(c, motivo)

            # Regla 4: Si hay señal de video ("si"), no existen pitidos de error POST
            widget_beeps = self.widgets_etapa2.get("beeps")
            if widget_beeps and "beeps" not in bloqueados:
                if video == "si":
                    widget_beeps.configure(values=["", "ninguno"])
                    if self._obtener_var_campo("beeps").get() not in ("", "ninguno"):
                        self._obtener_var_campo("beeps").set("ninguno")
                else:
                    widget_beeps.configure(values=[""] + CATEGORICOS["beeps"])

            # Regla 5: Si el cable de red no tiene continuidad, el LED del puerto RJ-45 no enciende
            if cable_red == "no":
                bloqueados.setdefault("led_puerto_red", "Cable de red sin continuidad física")

            # Regla 6: Si hay red cableada OK con LED encendido, evitar marcar cable roto
            if red_ok == "si" and self._obtener_var_campo("led_puerto_red").get() == "si":
                bloqueados.setdefault("continuidad_cable_red", "Enlace físico activo")

            # Aviso preventivo en vivo si +12V < 10V pero ventiladores == si
            if v_12 is not None and v_12 < 10.0 and ventiladores == "si" and "v_12" not in bloqueados:
                avisos_fisicos.append(
                    f"Nota: +12V en {v_12} V es muy bajo para mantener ventiladores girando; verifica tu medición."
                )

            # Aplicar estados visuales y limpiar valores de campos bloqueados
            for clave, widget in self.widgets_etapa2.items():
                lbl = self.labels_etapa2.get(clave)
                if clave in bloqueados:
                    self._obtener_var_campo(clave).set("")
                    widget.configure(state="disabled")
                    if lbl:
                        lbl.configure(fg=PALETA["texto_bloqueado"])
                else:
                    estado_habilitado = "readonly" if isinstance(widget, ttk.Combobox) else "normal"
                    widget.configure(state=estado_habilitado)
                    if lbl:
                        lbl.configure(fg=PALETA["texto_secundario"])

            # Actualizar banner informativo en tiempo real
            if hasattr(self, "var_aviso_form") and hasattr(self, "lbl_aviso_form"):
                if bloqueados:
                    motivos_unicos = list(dict.fromkeys(bloqueados.values()))
                    self.var_aviso_form.set(
                        f"🔒 Bloqueo activo ({len(bloqueados)} campos): {'; '.join(motivos_unicos)}."
                    )
                    self.lbl_aviso_form.configure(
                        bg=PALETA["aviso_bg"], fg=PALETA["aviso_fg"]
                    )
                elif avisos_fisicos:
                    self.var_aviso_form.set(f"⚠ {avisos_fisicos[0]}")
                    self.lbl_aviso_form.configure(
                        bg=PALETA["aviso_bg"], fg=PALETA["aviso_fg"]
                    )
                elif video == "si":
                    self.var_aviso_form.set(
                        "✓ Video activo: pitidos de error POST restringidos a 'ninguno' (presiona 'Analizar →' para evaluar)."
                    )
                    self.lbl_aviso_form.configure(
                        bg=PALETA["primario_suave"], fg=PALETA["primario_texto"]
                    )
                else:
                    self.var_aviso_form.set(
                        "Formulario inteligente activo: captura tus datos y presiona 'Analizar →' (o Enter)."
                    )
                    self.lbl_aviso_form.configure(
                        bg=PALETA["tarjeta_suave"], fg=PALETA["texto_secundario"]
                    )
        finally:
            self._actualizando_reglas_form = False

    def _construir_controles_etapa_3(self):
        tk.Label(
            self.panel_dinamico,
            text="Etapa 3 — Verificación y Solución (el bot recuerda todo tu caso):",
            font=("Segoe UI", 9, "bold"),
            bg=PALETA["tarjeta_bg"],
            fg=PALETA["texto_principal"],
        ).pack(anchor="w", pady=(0, 8))

        fila = tk.Frame(self.panel_dinamico, bg=PALETA["tarjeta_bg"])
        fila.pack(fill="x")
        fila.columnconfigure(0, weight=1)
        fila.columnconfigure(1, weight=1)
        fila.columnconfigure(2, weight=2)

        BotonRedondeado(
            fila,
            texto="Ver reglas y CF",
            comando=self.mostrar_razonamiento_detallado,
            bg_exterior=PALETA["tarjeta_bg"],
            bg_normal=PALETA["secundario_bg"],
            bg_hover=PALETA["secundario_hover"],
            fg_texto=PALETA["secundario_fg"],
            altura=34,
            ancho=140,
            radio=15,
        ).grid(row=0, column=0, sticky="ew", padx=3)

        BotonRedondeado(
            fila,
            texto="← Ajustar datos",
            comando=lambda: self._cambiar_etapa_manual(2),
            bg_exterior=PALETA["tarjeta_bg"],
            bg_normal=PALETA["secundario_bg"],
            bg_hover=PALETA["secundario_hover"],
            fg_texto=PALETA["secundario_fg"],
            altura=34,
            ancho=130,
            radio=15,
        ).grid(row=0, column=1, sticky="ew", padx=3)

        BotonRedondeado(
            fila,
            texto="Sigue fallando → Ver refacción con convenio",
            comando=self.pasar_a_etapa_4_convenios,
            bg_exterior=PALETA["tarjeta_bg"],
            bg_normal=PALETA["primario"],
            bg_hover=PALETA["primario_hover"],
            fg_texto="#FFFFFF",
            altura=34,
            ancho=240,
            radio=15,
        ).grid(row=0, column=2, sticky="ew", padx=3)

    def _construir_controles_etapa_4(self):
        tk.Label(
            self.panel_dinamico,
            text="Etapa 4 — Sostenibilidad y Convenios con Tiendas Aliadas:",
            font=("Segoe UI", 9, "bold"),
            bg=PALETA["tarjeta_bg"],
            fg=PALETA["texto_principal"],
        ).pack(anchor="w", pady=(0, 8))

        fila = tk.Frame(self.panel_dinamico, bg=PALETA["tarjeta_bg"])
        fila.pack(fill="x")
        fila.columnconfigure(0, weight=2)
        fila.columnconfigure(1, weight=1)
        fila.columnconfigure(2, weight=1)

        BotonRedondeado(
            fila,
            texto="Mostrar cupón y tienda aliada",
            comando=self.mostrar_recomendacion_convenio,
            bg_exterior=PALETA["tarjeta_bg"],
            bg_normal="#138A63",
            bg_hover="#0F7050",
            fg_texto="#FFFFFF",
            altura=34,
            ancho=210,
            radio=15,
        ).grid(row=0, column=0, sticky="ew", padx=3)

        BotonRedondeado(
            fila,
            texto="← Ver solución",
            comando=lambda: self._cambiar_etapa_manual(3),
            bg_exterior=PALETA["tarjeta_bg"],
            bg_normal=PALETA["secundario_bg"],
            bg_hover=PALETA["secundario_hover"],
            fg_texto=PALETA["secundario_fg"],
            altura=34,
            ancho=130,
            radio=15,
        ).grid(row=0, column=1, sticky="ew", padx=3)

        BotonRedondeado(
            fila,
            texto="Nuevo caso",
            comando=self.reiniciar_sesion,
            bg_exterior=PALETA["tarjeta_bg"],
            bg_normal=PALETA["primario_suave"],
            bg_hover="#DDD6FE",
            fg_texto=PALETA["primario_texto"],
            altura=34,
            ancho=120,
            radio=15,
        ).grid(row=0, column=2, sticky="ew", padx=3)

    # ==================== LOGICA DE INTERACCION Y SEGURIDAD ELECTRICA ====================

    def _recopilar_datos_formulario(self):
        """Obtiene todos los valores no vacios capturados actualmente en los campos."""
        return {
            k: v.get().strip()
            for k, v in self.entradas.items()
            if v.get() and v.get().strip()
        }

    def _detectar_sobretension_critica(self, datos_brutos):
        """Guarda electrica previa al motor: detecta voltajes peligrosos fuera de rango."""
        umbrales_peligro = {
            "v_12": (13.2, 20.0, "+12 V"),
            "v_5": (5.5, 10.0, "+5 V"),
            "v_3_3": (3.6, 6.0, "+3.3 V"),
            "v_ac": (145.0, 300.0, "Toma AC"),
        }
        alertas = []
        datos_limpios = {}

        for campo, raw in datos_brutos.items():
            texto = str(raw).strip() if raw is not None else ""
            if not texto:
                continue
            if campo in NUMERICOS:
                try:
                    val = float(texto.replace(",", "."))
                except ValueError:
                    continue

                if campo in umbrales_peligro:
                    lim_alto, max_fisico, etiqueta = umbrales_peligro[campo]
                    if val > max_fisico:
                        alertas.append(
                            f"¡PELIGRO CRÍTICO en {etiqueta}: {val} V! Supera el máximo físico "
                            f"({max_fisico} V). Hay riesgo grave de cortocircuito o daño irreversible en placa base y discos."
                        )
                        continue
                    if val > lim_alto:
                        alertas.append(
                            f"ADVERTENCIA DE SOBRETENSIÓN en {etiqueta}: {val} V (límite seguro: {lim_alto} V)."
                        )
                datos_limpios[campo] = val
            else:
                datos_limpios[campo] = texto

        return datos_limpios, alertas

    def _inferir_datos_desde_texto_libre(self, texto):
        """Complementa normalizar.py detectando intenciones basicas y sintomas frecuentes."""
        t = texto.lower()
        datos = {}
        if "no enciende" in t or "no prende" in t or "muerta" in t:
            datos["led_encendido"] = "no"
            datos["ventiladores"] = "no"
        if "giran" in t and "ventilador" in t and "no" not in t.split("ventilador")[0][-6:]:
            datos["ventiladores"] = "si"
        if "no da video" in t or "sin video" in t or "pantalla negra" in t:
            datos["video"] = "no"
        if "pitido" in t or "bip" in t or "beep" in t:
            if "corto" in t:
                datos["beeps"] = "cortos_repetitivos"
            elif "largo" in t:
                datos["beeps"] = "uno_largo_dos_cortos"
        if "quemado" in t or "humo" in t:
            datos["olor_quemado"] = "si"
        if "no hay internet" in t or "sin red" in t or "no detecta red" in t:
            datos["red_detectada"] = "no"
        if "usb" in t and ("no funciona" in t or "no responde" in t or "no detecta" in t):
            datos["usb_responde"] = "no"
        return datos

    def _aplicar_preset_etapa_1(self, datos_preset, frase):
        self._escribir_chat("Tú", frase, "usr_texto")
        for k, v in datos_preset.items():
            self._obtener_var_campo(k).set(v)

        res = self.gestor_sesion.procesar(datos_preset, frase)
        self.gestor_sesion.establecer_etapa(2)
        self._renderizar_controles_etapa()
        self._actualizar_panel_memoria()

        respuesta = (
            "He registrado esos síntomas iniciales en la memoria de tu caso.\n"
            "Pasemos a la Etapa 2 (Análisis): completa los voltajes (+12V, +5V, +3.3V), "
            "temperatura o pitidos abajo y presiona 'Analizar →'."
        )
        if res.get("diagnosticos"):
            top = res["diagnosticos"][0]
            respuesta += f"\n\nHipótesis preliminar: {top['nombre']} ({top['cf']*100:.0f}% de certeza)."
        self._escribir_chat("Asistente", respuesta)

    def procesar_analisis_etapa_2(self):
        datos_brutos = self._recopilar_datos_formulario()
        obs = self.var_obs_etapa2.get().strip() if hasattr(self, "var_obs_etapa2") else ""
        if hasattr(self, "var_obs_etapa2"):
            self.var_obs_etapa2.set("")

        resumen_usr = [
            f"{ETIQUETAS_CAMPOS.get(k, k)}: {val}" for k, val in datos_brutos.items()
        ]
        if obs:
            resumen_usr.append(f"Observaciones: '{obs}'")
        if not resumen_usr:
            resumen_usr.append("Analizar con los síntomas ya registrados en memoria.")

        self._escribir_chat("Tú", " | ".join(resumen_usr), "usr_texto")

        datos_limpios, alertas_elec = self._detectar_sobretension_critica(datos_brutos)

        if any("PELIGRO CRÍTICO" in a for a in alertas_elec):
            self.alerta_critica_activa = "\n".join(alertas_elec)
            self._escribir_chat(
                "Asistente",
                f"{self.alerta_critica_activa}\n\n"
                "ACCIÓN INMEDIATA: Desconecta el cable de corriente de inmediato. "
                "No vuelvas a encender la computadora con esa fuente. "
                "Pasando a Etapa 4 para recomendarte un reemplazo certificado con convenio.",
                "alerta_critica",
            )
            self.gestor_sesion.procesar(datos_limpios, obs)
            self.gestor_sesion.establecer_etapa(4)
            self._renderizar_controles_etapa()
            self._actualizar_panel_memoria()
            self.mostrar_recomendacion_convenio(forzar_id="D_PSU_ALTO")
            return

        if alertas_elec:
            self._escribir_chat("Asistente", "\n".join(alertas_elec), "advertencia")

        res = self.gestor_sesion.procesar(datos_limpios, obs)
        self.gestor_sesion.establecer_etapa(3)
        self._renderizar_controles_etapa()
        self._actualizar_panel_memoria()
        self._presentar_diagnostico_etapa_3(res)

    def _presentar_diagnostico_etapa_3(self, res):
        if not res.get("ok"):
            errores = "\n".join(f"- {e}" for e in res.get("errores", []))
            self._escribir_chat("Asistente", f"Revisa estos datos:\n{errores}", "advertencia")
            return

        if res.get("advertencias"):
            adv = "ADVERTENCIA DE CONGRUENCIA FÍSICA:\n" + "\n".join(
                f"• {a}" for a in res["advertencias"]
            )
            self._escribir_chat("Asistente", adv, "advertencia")

        if res.get("indeterminado"):
            sugs = "\n".join(f"• {s}" for s in res.get("sugerencias", []))
            self._escribir_chat(
                "Asistente",
                "Con los datos actuales aún no se activa ninguna regla de falla concluyente.\n"
                f"Para llegar a un diagnóstico preciso necesito que me indiques:\n{sugs}",
            )
            return

        top = res["diagnosticos"][0]
        alternativas = ""
        if len(res["diagnosticos"]) > 1:
            otras = [
                f"  - {d['nombre']} ({d['cf']*100:.0f}%)"
                for d in res["diagnosticos"][1:3]
            ]
            alternativas = "\n\nOTRAS FALLAS DETECTADAS EN PARALELO:\n" + "\n".join(otras)

        texto_diag = (
            f"DIAGNÓSTICO PRINCIPAL (Etapa 3 — Solución):\n"
            f"• Falla detectada: {top['nombre']}\n"
            f"• Subsistema: {top['subsistema']} | Certeza combinada: {top['cf']*100:.0f}% ({top['nivel'].upper()})\n\n"
            f"PASOS DE VERIFICACIÓN Y REPARACIÓN:\n"
            f"{top['accion']}\n\n"
            f"PRECAUCIÓN DE SEGURIDAD:\n"
            f"{top['seguridad']}"
            f"{alternativas}\n\n"
            "Si ya realizaste estos pasos y el problema continúa, presiona "
            "'Sigue fallando → Ver refacción con convenio'."
        )
        self._escribir_chat("Asistente", texto_diag, "diagnostico")

    def mostrar_razonamiento_detallado(self):
        res = self.gestor_sesion.ultimo_resultado
        if not res or not res.get("diagnosticos"):
            self._escribir_chat(
                "Asistente",
                "Aún no hay reglas de diagnóstico disparadas. Completa voltajes o síntomas en Etapa 2 y presiona 'Analizar →'.",
            )
            return

        lineas = ["TRAZABILIDAD DEL MOTOR DE INFERENCIA (ENCADENAMIENTO Y CF):"]
        for i, d in enumerate(res["diagnosticos"][:3]):
            etq = "Principal" if i == 0 else f"Alternativa {i}"
            lineas.append(f"\n[{etq}] {d['nombre']} -> CF = {d['cf']*100:.1f}%")
            for r in d["razones"]:
                lineas.append(f"   • Regla {r['regla']}: {r['texto']}")
        if res.get("hechos_derivados"):
            lineas.append(f"\nHechos derivados internamente: {res['hechos_derivados']}")
        self._escribir_chat("Asistente", "\n".join(lineas), "razonamiento")

    def pasar_a_etapa_4_convenios(self):
        self._escribir_chat("Tú", "Ya probé las verificaciones y el equipo sigue fallando.", "usr_texto")
        self.gestor_sesion.establecer_etapa(4)
        self._renderizar_controles_etapa()
        self._actualizar_panel_memoria()
        self.mostrar_recomendacion_convenio()

    def mostrar_recomendacion_convenio(self, forzar_id=None):
        diag_id = forzar_id
        nombre_falla = "Sobretensión crítica en fuente de poder"
        if not diag_id:
            res = self.gestor_sesion.ultimo_resultado
            if res and res.get("diagnosticos"):
                diag_id = res["diagnosticos"][0]["id"]
                nombre_falla = res["diagnosticos"][0]["nombre"]
            else:
                diag_id = "D_PSU"
                nombre_falla = "Diagnóstico general de hardware"

        info = self.convenios.get(diag_id, CONVENIOS_RESPALDO.get(diag_id))
        if not info:
            self._escribir_chat("Asistente", "No hay un convenio específico registrado para esta falla.")
            return

        msg = (
            f"RECOMENDACIÓN DE REFACCIÓN / HERRAMIENTA (Etapa 4 — Convenio):\n"
            f"• Para resolver: {nombre_falla}\n"
            f"• Artículo recomendado: {info['articulo']}\n"
            f"• Tienda / Taller aliado: {info['tienda']}\n"
            f"• Beneficio / Descuento: {info['descuento']}\n"
            f"• Costo estimado: {info['costo_estimado']}\n"
            f"• Nota técnica: {info['nota']}"
        )
        self._escribir_chat("Asistente", msg, "convenio")

    def enviar_mensaje_libre(self):
        texto = self.var_mensaje.get().strip()
        if not texto:
            return
        self.var_mensaje.set("")
        self._escribir_chat("Tú", texto, "usr_texto")

        t_low = texto.lower()

        # 1. Intencion de compra / refacciones / convenios
        if any(
            p in t_low
            for p in (
                "donde compro",
                "dónde compro",
                "refaccion",
                "refacción",
                "convenio",
                "tienda",
                "sigue fallando",
                "ya lo intente",
                "ya lo intenté",
            )
        ):
            self.gestor_sesion.establecer_etapa(4)
            self._renderizar_controles_etapa()
            self._actualizar_panel_memoria()
            self.mostrar_recomendacion_convenio()
            return

        # 2. Intencion de explicacion de reglas / trazabilidad
        if any(p in t_low for p in ("por que", "por qué", "razonamiento", "reglas", "certeza")):
            self.mostrar_razonamiento_detallado()
            return

        # 3. Sincronizar cualquier dato que el usuario haya llenado en el formulario de Etapa 2
        # junto con los sintomas detectados en el texto libre
        datos_form = self._recopilar_datos_formulario()
        datos_texto = self._inferir_datos_desde_texto_libre(texto)
        for k, v in datos_texto.items():
            self._obtener_var_campo(k).set(v)
            datos_form[k] = v

        datos_limpios, alertas_elec = self._detectar_sobretension_critica(datos_form)
        if any("PELIGRO CRÍTICO" in a for a in alertas_elec):
            self.alerta_critica_activa = "\n".join(alertas_elec)
            self._escribir_chat(
                "Asistente",
                f"{self.alerta_critica_activa}\n\n"
                "ACCIÓN INMEDIATA: Desconecta el equipo de la corriente de inmediato.",
                "alerta_critica",
            )
            self.gestor_sesion.procesar(datos_limpios, texto)
            self.gestor_sesion.establecer_etapa(4)
            self._renderizar_controles_etapa()
            self._actualizar_panel_memoria()
            self.mostrar_recomendacion_convenio(forzar_id="D_PSU_ALTO")
            return

        if alertas_elec:
            self._escribir_chat("Asistente", "\n".join(alertas_elec), "advertencia")

        res = self.gestor_sesion.procesar(datos_limpios, texto)
        self._actualizar_panel_memoria()

        pide_conclusion = any(
            p in t_low
            for p in (
                "entonces que pasa",
                "entonces qué pasa",
                "que pasa",
                "qué pasa",
                "que tiene",
                "qué tiene",
                "cual es la falla",
                "cuál es la falla",
                "diagnostico",
                "diagnóstico",
                "analiza",
                "resultado",
                "solucion",
                "solución",
            )
        )

        # Si ya hay diagnostico confirmado y el usuario pregunta que pasa o ya cargo mediciones
        if res.get("diagnosticos") and (pide_conclusion or len(datos_limpios) >= 4):
            self.gestor_sesion.establecer_etapa(3)
            self._renderizar_controles_etapa()
            self._actualizar_panel_memoria()
            self._presentar_diagnostico_etapa_3(res)
            return

        if self.gestor_sesion.etapa_actual == 1:
            self.gestor_sesion.establecer_etapa(2)
            self._renderizar_controles_etapa()
            self._actualizar_panel_memoria()

        if res.get("diagnosticos"):
            top = res["diagnosticos"][0]
            self._escribir_chat(
                "Asistente",
                f"Con los datos actuales, la falla más probable es **{top['nombre']}** "
                f"({top['cf']*100:.0f}% de certeza).\n"
                "Si quieres ver los pasos de reparación, escribe '¿qué tiene?' o presiona 'Analizar →'.",
            )
        else:
            sugs = res.get("sugerencias", [])
            detalle_falta = "\n".join(f"• {s}" for s in sugs[:3]) if sugs else (
                "• Voltajes de fuente (+12V, +5V, +3.3V) o temperatura de CPU.\n"
                "• Si emite pitidos POST o si falla red/USB."
            )
            self._escribir_chat(
                "Asistente",
                "Con los síntomas registrados hasta ahora todavía hay varias causas posibles "
                "(por ejemplo: cable de video, RAM, GPU o tarjeta madre) y ninguna regla alcanza el umbral.\n\n"
                f"Para darte un diagnóstico exacto, dime o captura en el panel de arriba:\n{detalle_falta}",
            )

    def _cambiar_etapa_manual(self, nueva_etapa):
        etapa_previa = self.gestor_sesion.etapa_actual

        # Si el usuario salta de Etapa 2 a Etapa 3 teniendo datos llenos en el formulario,
        # ejecutamos el analisis automaticamente para que vea la respuesta en el chat.
        if etapa_previa == 2 and nueva_etapa == 3 and self._recopilar_datos_formulario():
            self.procesar_analisis_etapa_2()
            return

        self.gestor_sesion.establecer_etapa(nueva_etapa)
        self._renderizar_controles_etapa()
        self._actualizar_panel_memoria()

        if nueva_etapa == 3:
            res = self.gestor_sesion.ultimo_resultado
            if res and (res.get("diagnosticos") or res.get("indeterminado")):
                self._presentar_diagnostico_etapa_3(res)
        elif nueva_etapa == 4:
            self.mostrar_recomendacion_convenio()

    def reiniciar_sesion(self):
        self.gestor_sesion.reiniciar(etapa_inicial=1)
        self.alerta_critica_activa = None
        self._limpiar_campos_etapa2()
        self.chat_box.configure(state="normal")
        self.chat_box.delete("1.0", "end")
        self.chat_box.configure(state="disabled")
        self._renderizar_controles_etapa()
        self._mostrar_bienvenida()
        self._actualizar_panel_memoria()

    # ==================== MONITOR EN VIVO DE MEMORIA ====================

    def _actualizar_panel_memoria(self):
        estado = self.gestor_sesion.obtener_estado()
        etapa = estado["etapa_actual"]
        turnos = len(estado["historial"])
        entrada = estado["entrada_acumulada"]
        hechos = estado["hechos_acumulados"]
        obs = estado["observaciones"]
        res = estado["ultimo_resultado"] or {}

        self.memoria_box.configure(state="normal")
        self.memoria_box.delete("1.0", "end")

        self.memoria_box.insert("end", "ESTADO DE SESIÓN\n", "titulo")
        self.memoria_box.insert("end", f"  Etapa actual  : {NOMBRES_ETAPAS[etapa]}\n", "dato")
        self.memoria_box.insert("end", f"  Turnos en chat: {turnos}\n\n")

        if self.alerta_critica_activa:
            self.memoria_box.insert("end", "ALERTA ELÉCTRICA\n", "alerta")
            self.memoria_box.insert("end", f"{self.alerta_critica_activa}\n\n", "alerta")

        self.memoria_box.insert("end", "DATOS MEMORIZADOS\n", "titulo")
        if entrada:
            for k, v in entrada.items():
                etq = ETIQUETAS_CAMPOS.get(k, k)
                self.memoria_box.insert("end", f"  • {etq}: {v}\n", "ok")
        else:
            self.memoria_box.insert("end", "  (Sin mediciones aún)\n")

        self.memoria_box.insert("end", "\nHECHOS DE OBSERVACIONES\n", "titulo")
        hechos_obs = {k: v for k, v in hechos.items() if k not in entrada}
        if hechos_obs:
            for k, v in hechos_obs.items():
                self.memoria_box.insert("end", f"  • {k} = {v}\n", "dato")
        else:
            self.memoria_box.insert("end", "  (Sin hechos extraídos de texto)\n")

        if obs:
            self.memoria_box.insert("end", "\nNOTAS DEL USUARIO\n", "titulo")
            for idx, nota in enumerate(obs[-3:], 1):
                self.memoria_box.insert("end", f'  {idx}. "{nota}"\n')

        derivados = res.get("hechos_derivados", {})
        if derivados:
            self.memoria_box.insert("end", "\nHECHOS DERIVADOS (IA)\n", "titulo")
            for k, v in derivados.items():
                self.memoria_box.insert("end", f"  • {k} -> {v}\n", "ok")

        diags = res.get("diagnosticos", [])
        self.memoria_box.insert("end", "\nHIPÓTESIS ACTUAL\n", "titulo")
        if diags:
            top = diags[0]
            self.memoria_box.insert(
                "end",
                f"  {top['nombre']}\n  Certeza: {top['cf']*100:.0f}% ({top['nivel']})\n",
                "ok",
            )
        elif self.alerta_critica_activa:
            self.memoria_box.insert("end", "  Sobretensión crítica (D_PSU_ALTO)\n", "alerta")
        else:
            self.memoria_box.insert("end", "  En espera de más evidencia...\n")

        self.memoria_box.configure(state="disabled")


if __name__ == "__main__":
    app = AplicacionDiagnostico()
    app.mainloop()