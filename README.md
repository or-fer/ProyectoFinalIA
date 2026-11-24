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
├── gestor_sesion.py           # Estado, historial y etapas de una sesión
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

`GestorSesion` conserva los datos estructurados, los hechos extraídos de las
observaciones, el historial y la etapa actual (1 a 4). La interfaz lo utiliza
para enviar cada turno al normalizador y después al motor sin mezclar hechos
extraídos con campos estructurados.

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

## 4. Estado documentado de las fases 0 y 1

### Fase 0 — Separación de información

- Los datos medidos y categóricos se describen en `pruebas/matriz_informacion.py`.
- Los hechos derivados son resultados del encadenamiento y no datos capturados.
- `pruebas/casos_falla.py` conserva la línea base de 20 casos históricos.
- `pruebas/ejemplos_lenguaje.py` registra frases humanas reconocidas y limitaciones conocidas.
- `probar.py` valida el contrato de información y conserva los casos existentes.

Esta fase no amplía la base de conocimiento ni agrega comprensión real de conversaciones.

### Fase 1 — Formalización del motor SI-ENTONCES

- `motor_inferencia.py` valida la estructura de `base_conocimiento.json`.
- Las reglas pueden derivar hechos o producir diagnósticos.
- El proceso continúa hasta que ninguna regla nueva pueda dispararse.
- Las reglas que apoyan un diagnóstico combinan sus factores de certeza.
- `pruebas/casos_motor.py` verifica operadores, encadenamiento, CF y errores de configuración.

Esta fase no cambia las reglas de `base_conocimiento.json`, no interpreta negaciones
ni extrae mediciones de texto libre. Los límites se conservarán como pruebas de deuda
hasta la siguiente fase.

## 5. Plan completo de desarrollo por fases

Las fases siguientes deben implementarse en orden. Cada fase debe conservar aprobada
la batería anterior antes de comenzar la siguiente. No se debe robustecer la base de
conocimiento ni modificar reglas existentes antes de completar las fases 2 a 4.

### Fase 2 — Normalización humana

**Objetivo:** convertir lenguaje cotidiano en texto estándar que pueda analizarse de forma determinista.

**Responsabilidades del código:**

- Ampliar `normalizar.py`.
- Convertir mayúsculas, minúsculas y acentos de forma controlada.
- Normalizar puntos y comas decimales.
- Expandir abreviaturas habituales de medición.
- Admitir expresiones equivalentes para sí, no, encendido, apagado y detección.
- Mantener el texto original junto con su representación normalizada.

**Ejemplos esperados:**

```text
127 V
127 volts
127 voltios
```

Estas variantes deben producir el mismo dato estructurado: `v_ac = 127`.

**Entregables:**

- Funciones nuevas separadas de la extracción de hechos.
- Pruebas unitarias de normalización.
- Tabla de sinónimos y variantes documentada.
- Confirmación de que signos de puntuación no cambian el significado.

**Criterio de aceptación:** al menos 100 variantes lingüísticas deben resolver al mismo hecho esperado cuando su significado sea equivalente.

**No incluye:** extracción de entidades, manejo de negaciones, preguntas al usuario ni modificación de `base_conocimiento.json`.

### Fase 3 — Negación e incertidumbre

**Objetivo:** evitar que una negación se interprete como un síntoma positivo.

**Responsabilidades del código:**

- Ampliar el análisis de expresiones antes de crear hechos.
- Detectar negaciones explícitas e implícitas.
- Representar confirmación, negación, duda y ausencia de observación por separado.
- Asociar cada hecho con la evidencia textual que lo produjo.
- Reducir o impedir el uso de hechos dudosos como si fueran ciertos.
- Detectar coincidencias en frases negativas como `"no hubo chispazo"` o `"sin continuidad"`.

**Estados mínimos propuestos:**

```text
confirmado
negado
desconocido
dudoso
contradictorio
```

**Ejemplos esperados:**

- `"no hubo chispazo"` produce `chispazo = no`, no `chispazo = si`.
- `"no me sale pantalla azul"` produce `pantalla_azul = no`.
- `"creo que gira"` produce un estado dudoso.
- `"tal vez no haya video"` no debe utilizarse como un hecho positivo definitivo.

**Entregables:**

- Representación estructurada de cada hecho observado.
- Reglas de negación y alcance documentadas.
- Pruebas positivas, negativas y dudosas.
- Explicación visible de por qué se acepta o rechaza una observación.

**Criterio de aceptación:** las frases negativas incluidas en las pruebas no deben activar reglas positivas asociadas con el síntoma negado.

**No incluye:** extracción de todos los campos todavía ni integración conversacional.

### Fase 4 — Extracción de entidades humanas

**Objetivo:** convertir una descripción completa en hechos compatibles con `validar_entrada` y el motor SI-ENTONCES.

**Responsabilidades del código:**

- Crear una capa independiente de análisis de texto, por ejemplo `extractor_humano.py`.
- Extraer mediciones numéricas con unidad.
- Extraer estados sí/no.
- Extraer patrones de pitidos.
- Extraer síntomas conocidos.
- Resolver fechas o rangos solamente si aparecen como información útil; no inventar valores.
- Combinar datos del formulario y datos extraídos sin sobrescritura silenciosa.
- Pedir confirmación cuando una medición o síntoma contradiga el formulario.

**Ejemplo:**

```text
"Mide 95 volts y los ventiladores sí giran"
```

Debe producir:

```json
{
  "v_ac": 95,
  "ventiladores": "si"
}
```

**Entregables:**

- Extracción de entidades separada del normalizador.
- Tabla de patrones, sinónimos y formatos numéricos.
- Función que compare datos del formulario con datos extraídos.
- Resultado con campo, valor, polaridad, evidencia y confianza.
- Pruebas de texto combinado, unidades y contradicciones.

**Criterio de aceptación:** una descripción humana debe poder convertir mediciones y síntomas conocidos en hechos válidos sin enviar texto directamente al motor como un dato desconocido.

**No incluye:** diálogo persistente ni modificación de las reglas de diagnóstico.

### Fase 5 — Diálogo dirigido por datos faltantes

**Objetivo:** permitir que el sistema solicite la información con mayor utilidad cuando los datos sean incompletos.

**Responsabilidades del código:**

- Mantener el estado de una conversación en memoria.
- Consolidar respuestas nuevas sin perder datos anteriores.
- Identificar datos faltantes que puedan cambiar diagnósticos.
- Formular una pregunta a la vez.
- Permitir respuestas afirmativas, negativas, numéricas y `"no sé"`.
- Asociar cada respuesta con el campo que completa.
- Añadir una confirmación antes de usar datos dudosos.

**Prioridad sugerida de preguntas:**

1. ¿El equipo enciende?
2. ¿Giran los ventiladores?
3. ¿Hay video?
4. ¿Qué patrón de pitidos se escucha?
5. ¿Cuál es el voltaje de la toma AC?
6. ¿Cómo están los rieles medidos?

**Entregables:**

- Modelo simple de estado conversacional.
- Lista priorizada de datos faltantes.
- Formato de pregunta, respuesta y hecho confirmado.
- Interfaz que pueda mostrar datos detectados antes del diagnóstico.
- Pruebas de preguntas, respuestas parciales y reinicio.

**Criterio de aceptación:** ante datos insuficientes, el sistema debe solicitar primero un dato útil y conservar los datos anteriores al recibir una respuesta.

**No incluye:** reconocimiento mediante una red neuronal ni envío de datos sensibles a servicios externos.

### Fase 6 — Calibración de factores de certeza

**Objetivo:** hacer que los factores de certeza sean coherentes, trazables y respaldados por casos conocidos.

**Responsabilidades del código:**

- Revisar las contribuciones de cada regla sin alterar arbitrariamente diagnósticos.
- Mantener la fórmula `CF = CF1 + CF2(1 - CF1)` para evidencia independiente.
- Registrar todas las reglas que participan en un diagnóstico.
- Distinguir evidencia fuerte, evidencia débil y contradicción.
- Evitar reducir toda confianza globalmente por cualquier advertencia menor.
- Documentar qué porcentaje proviene de una regla y cuál proviene de combinación.
- No presentar porcentajes como probabilidad estadística si no existe base empírica.

**Entregables:**

- Tabla de reglas con CF, evidencias y motivo de calibración.
- Casos extremos de combinación.
- Pruebas para valores límite.
- Explicación visible de la composición del CF.
- Declaración sobre el significado académico de los porcentajes.

**Criterio de aceptación:** dos combinaciones independientes deben producir exactamente el mismo CF esperado y la traza debe mostrar las dos reglas originales.

**No incluye:** inventar datos estadísticos ni sustituir CF por una red neuronal.

### Fase 7 — Robustecimiento de la base de conocimiento

**Objetivo:** ampliar y depurar las reglas de diagnóstico sin perder explicabilidad.

**Responsabilidades del contenido técnico:**

- Revisar `base_conocimiento.json` contra los casos aprobados.
- Separar hechos observables de hechos derivados.
- Eliminar reglas duplicadas o contradictorias.
- Revisar reglas que dependen de un solo síntoma débil.
- Relacionar cada regla nueva con al menos un caso de prueba.
- Documentar cada diagnóstico, acción y advertencia de seguridad.
- Mantener IDs únicos y condiciones compatibles con `validar_kb`.

**Entregables:**

- JSON validado automáticamente antes de cargar.
- Tabla de reglas antes y después de revisiones.
- Casos de límite asociados a cada cambio.
- Diagnósticos alternativos bien justificados.
- Documento de reglas ambiguas y decisiones pendientes.

**Criterio de aceptación:** ninguna regla puede agregarse sin una prueba que falle si la regla desaparece y sin documentación de su condición y CF.

**No incluye:** aprendizaje automático que genere reglas no auditables.

### Fase 8 — Pruebas rigurosas y evaluación final

**Objetivo:** demostrar que el motor conserva el comportamiento histórico y mejora sin introducir falsos positivos graves.

**Capas de prueba:**

1. Normalización y sinónimos.
2. Negación e incertidumbre.
3. Extracción de entidades.
4. Operadores y encadenamiento.
5. Punto fijo y ejecución única.
6. Combinación de CF.
7. Contradicciones físicas.
8. Datos incompletos.
9. Conversaciones breves y reinicio.
10. Interfaz gráfica y errores visibles.

**Métricas sugeridas:**

- Casos históricos aprobados.
- Exactitud del diagnóstico principal.
- Exhaustividad de síntomas reconocidos.
- Tasa de negaciones interpretadas correctamente.
- Tasa de falsas alarmas.
- Casos indeterminados.
- Contradicciones detectadas.
- Tiempo de respuesta.
- Cobertura de casos por regla.

**Entregables:**

- Batería organizada por capas.
- Reporte de aprobados y fallidos.
- Capturas de la interfaz con escenarios representativos.
- Registro de defectos conocidos.
- Comparación entre versión inicial y versión final.
- Confirmación de que no quedan archivos temporales ni rutas locales absolutas innecesarias.

**Criterio de aceptación:** la batería completa debe pasar en al menos dos equipos y reproducir el resultado sin dependencias externas no documentadas.

## Distribución sugerida del trabajo

- **Integrantes 1 y 2:** fases 2 y 4, normalización y extracción determinista.
- **Integrante 3:** fase 3 y definición formal de negación e incertidumbre.
- **Integrante 4:** fases 6 y 7, revisión crítica de CF y base de conocimiento.
- **Integrante 5:** fase 5 y pruebas de interacción en `app.py`.
- **Todo el equipo:** fase 8 y revisión cruzada de casos, resultados y capturas.

Cada integrante debe documentar las decisiones tomadas y añadir casos de prueba que demuestren el comportamiento que implementó.
