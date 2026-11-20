# Sistema Experto de Diagnóstico de Fallas en Hardware

**Institución:** Universidad Nacional Autónoma de México (UNAM) — Facultad de Ingeniería  
**Asignatura:** Inteligencia Artificial — Proyecto Final  
**Profesor:** Dr. José Fidel Urquiza Yllescas  

## 1. Descripción del proyecto

Prototipo de sistema experto basado en reglas (`SI - ENTONCES`) con encadenamiento hacia adelante (*forward chaining*) y factores de certeza (CF) para asistir en el diagnóstico inicial de fallas de hardware y etapa de alimentación en equipos de cómputo.

A partir de un formulario con mediciones eléctricas básicas (toma AC, continuidad de fusible, rieles de +12 V, +5 V y +3.3 V, temperatura del CPU) y síntomas observables (LEDs, ventiladores, video, pitidos POST, red y USB), el motor infiere los diagnósticos más probables, detecta incongruencias físicas en los datos capturados y sugiere acciones de revisión y seguridad.

## 2. Estructura del proyecto

```text
DiagnosticoHardwareIA/
├── app.py                     # Interfaz gráfica en Tkinter
├── motor_inferencia.py        # Motor de encadenamiento hacia adelante, CF y congruencia
├── base_conocimiento.json     # Hechos derivados, reglas SI-ENTONCES y diagnósticos
├── normalizar.py              # Limpieza de texto libre en observaciones
├── demo.py                    # Ejemplos rápidos ejecutables en terminal
├── probar.py                  # Batería de pruebas automáticas
├── pruebas/
│   └── casos_falla.py         # 20 casos de prueba (normales, límite e incongruentes)
├── requirements.txt
└── README.md
```

## 3. Requisitos y ejecución

No requiere instalar paquetes externos; funciona con **Python 3.8+** y su biblioteca estándar (`tkinter`, `json`, `unicodedata`).

```bash
cd DiagnosticoHardwareIA

# Ejecutar la interfaz gráfica
python3 app.py

# Ejecutar demostración en terminal
python3 demo.py

# Correr batería de pruebas automáticas
python3 probar.py -v
```
