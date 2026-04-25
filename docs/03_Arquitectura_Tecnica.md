# Capítulo 4: Arquitectura Técnica y Flujo de Datos

La magia del proyecto radica en la orquestación perfecta entre tres tecnologías clave: Python (Datos/ML), Prolog (Lógica) y Streamlit (UI).

## 4.1. Fase 1: Generación y Entrenamiento (Python)
El archivo `generar_datos.py` no lee una base de datos externa; la crea desde cero en milisegundos. 
- Simula estadísticamente la vida financiera de 500 clientes, incluyendo sus IPs, listas OFAC, DNI y transacciones.
- **Nivel Neuro:** Llama a la librería `scikit-learn` para entrenar 4 modelos predictivos (Clustering, Anomalías, Scoring Predictivo y NLP) usando esta misma data.
- **Salida:** Traduce los 500 clientes y las predicciones de Machine Learning a lenguaje de predicados (ej: `ingresos(c_001, 5000).`) y los guarda en `hechos_base.pl`.

## 4.2. Fase 2: Motor de Inferencia Simbólica (Prolog)
El archivo `motor_inferencia.pl` contiene las "Leyes" del banco. 
- Recibe la base de conocimientos generada por Python.
- Evalúa los hechos usando encadenamiento hacia atrás (Backward Chaining) y Cortes Lógicos (`!`) para optimizar el rendimiento (por ejemplo, si un DNI está vencido, aborta la evaluación inmediatamente sin calcular el riesgo crediticio).

## 4.3. Fase 3: Dashboard Web y XAI (Streamlit)
El archivo `app.py` actúa como el puente visual.
- A través de la librería `PySwip`, Streamlit le hace "preguntas" a Prolog en tiempo real (Ej: `?- evaluar_cliente(c_001, Resultado).`).
- Muestra el razonamiento, dibuja grafos topológicos usando `NetworkX`, y finalmente ejecuta `Hashlib` para grabar el dictamen en un archivo inmutable (`audit_trail_xai.log`).