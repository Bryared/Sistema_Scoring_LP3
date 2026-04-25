# Capítulo 6: Manual de Uso y Pruebas Unitarias

Para poner a prueba el sistema durante una demostración o auditoría, sigue estos pasos.

## 6.1. Ejecución del Sistema
1. Asegúrate de tener instalado SWI-Prolog y Python en tu equipo.
2. Corre el generador de IA: `python generar_datos.py`.
3. Inicia la interfaz web: `streamlit run app.py`.

## 6.2. Casos de Estudio (Tests Pre-programados)
Busca estos IDs en el panel lateral para forzar respuestas específicas del motor:

### El Bot Hacker (`c_001`)
- **Resultado Esperado:** Denegado por Seguridad.
- **Motivo:** El campo "Tiempo de Llenado" es anormalmente bajo (2s). Además, el modelo Isolation Forest (ML) lo marcará como "Comportamiento Anómalo DETECTADO" por lo que exigirá validación biométrica.

### El Riesgo Estadístico (`c_003`)
- **Resultado Esperado:** Denegado por Riesgo Crediticio.
- **Motivo:** La regresión logística le asignará un Score altísimo de default (95%). Prolog al leer esto y agruparlo en el Cluster "Joven Riesgoso", le bajará el umbral de deuda permitido al 25%, rechazándolo automáticamente.

### El Lavador de Activos (`c_007`)
- **Acción:** Selecciona el caso, ve a la pestaña AML.
- **Resultado Esperado con Tolerancia 0%:** Sin Riesgo.
- **Resultado Esperado con Tolerancia 10%:** ALERTA CRÍTICA y Grafo dibujado. 
- **Demostración NLP:** Prolog avisará que el NLP redujo la tolerancia porque detectó la palabra clave sospechosa en la descripción de la transferencia.

### El Falso Positivo (`c_010`)
- **Resultado Esperado:** Sin riesgo de lavado.
- **Motivo:** Aunque el dinero triangula, Prolog calculará el Timestamp y verá que demoró 6 meses. Ignorará la alerta sabiamente porque el *Smurfing* rápido ocurre en 72 horas.

### El Político (`c_012`)
- **Resultado Esperado:** Derivado a Evaluación Manual (PEP).
- **Motivo:** Demuestra el acatamiento estricto de las leyes anticorrupción SBS.

## 6.3. Verificación de Inmutabilidad XAI
Tras evaluar un caso, dirígete a la parte final de la barra lateral izquierda y presiona **"Mostrar Logs Inmutables XAI"**. Demostrarás cómo cada clic generó un sello SHA-256 imposible de modificar, sirviendo como evidencia ante juicios por discriminación.