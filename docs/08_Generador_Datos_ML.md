# Capítulo 8: El Componente Neuro (Machine Learning) - `generar_datos.py` (Parte 2)

Este capítulo explica la teoría y la lógica de la **Fase 2** del script `generar_datos.py`. Una vez generada la lista de 500 clientes en la memoria RAM, aplicamos Inteligencia Artificial Estadística usando la librería `scikit-learn` de Python.

## 8.1. Teoría Neuro-Simbólica
Los sistemas puramente "Simbólicos" (como un Prolog normal) sufren del problema del "Límite Rígido". Si programas que el DSR máximo sea 35%, un cliente con 35.1% será rechazado, lo cual no es comercialmente inteligente.
Al inyectar el componente "Neuro" (Modelos Estadísticos Predictivos), Python analiza variables ocultas que Prolog no puede ver, calcula probabilidades y agrupa clientes de manera flexible. Python le pasa estos resultados a Prolog, quien ahora tiene la "autorización predictiva" para alterar sus propios límites.

---

## 8.2. Desglose del Código: Preprocesamiento y Entrenamiento

### Preprocesamiento de Matrices (Features y Target)
Los algoritmos de ML no leen diccionarios crudos; leen arreglos de números (`numpy arrays`). El código extrae las características (`Features`) relevantes para cada tipo de modelo:
- **`X_scoring`:** Junta [Ingresos, Cuotas, Consultas, Antigüedad].
- **`X_anomaly`:** Junta [Tiempo llenado, Intentos Login, Consultas].
- **`X_clustering`:** Junta [Ingresos, Deuda Total, Antigüedad Domicilio].

Para entrenar un modelo que prediga si alguien va a caer en quiebra (Default), necesitamos una respuesta objetivo (`Target` o variable `Y`). Como no tenemos base de datos histórica real, simulamos una:
`is_default = 1 if c['estado_pago'] == 'moroso' or DSR > 40% else 0`

### Modelo 1: Regresión Logística (Scoring Predictivo)
Se utiliza para calcular la probabilidad porcentual de que alguien "rompa la cadena de pagos".
```python
clf = LogisticRegression(max_iter=1000)
clf.fit(X_scoring, y_default_simulado)
probs_default = clf.predict_proba(X_scoring)[:, 1]
```
Se alimenta al algoritmo con la matriz `X_scoring` (los 500 clientes) frente a la matriz `Y` (quién quebró y quién no). El algoritmo aprende los patrones y luego devuelve un arreglo `probs_default` que contiene un porcentaje del 0.0 al 1.0 para cada cliente.

### Modelo 2: Isolation Forest (Anomalías)
Se utiliza para la ciberseguridad avanzada. Es un modelo *No Supervisado*, lo que significa que no necesita saber quién cometió fraude en el pasado (`Y`); solo necesita los datos crudos (`X`).
```python
iso = IsolationForest(contamination=0.05, random_state=42)
iso.fit(X_anomaly)
anomalias = iso.predict(X_anomaly)
```
El bosque aísla aleatoriamente características. Si un perfil se aísla con muy pocos cortes (por ejemplo, porque llena el formulario demasiado rápido y consulta mucho el buró), el algoritmo deduce que es una anomalía y arroja un `-1`. Si es normal, arroja `1`.

### Modelo 3: K-Means (Clustering Demográfico)
Otro modelo *No Supervisado*. En lugar de tratar a todos por igual, se agrupan matemáticamente en clústeres.
```python
kmeans = KMeans(n_clusters=3, random_state=42)
clusters = kmeans.fit_predict(X_clustering)
```
La IA mapea a los 500 clientes en un espacio de 3 dimensiones (Ingresos vs Deuda vs Edad) y encuentra sus "centros de gravedad". Así crea 3 tribus: `joven_riesgoso`, `familia_estable`, y `emprendedor_promedio`.

### Modelo 4: Simulación NLP para AML
Se utiliza un enfoque rudimentario de Procesamiento de Lenguaje Natural iterando sobre el campo `concepto` de las transferencias bancarias generadas previamente. Busca correspondencias de palabras en una lista `palabras_peligro` (ej. "xyz", "favores"). Si el booleano es positivo, lo marca como `texto_sospechoso` para advertir al motor lógico de Lavado de Activos.

---

## 8.3. Fase 3: Traducción y Escritura en Prolog
Una vez que las redes neuronales han terminado sus cálculos, tenemos variables en memoria RAM de Python.
El paso final es inyectar esto en el motor simbólico. El script itera nuevamente a los 500 clientes, abre el archivo `hechos_base.pl` y mediante sentencias `f.write()` traduce el lenguaje Python al lenguaje lógico Prolog.

Por ejemplo, un score de Python `0.85` se imprime físicamente en el archivo de texto de esta manera:
`ml_probabilidad_default(c_001, 0.85).`
`ml_fraude_anomalia(c_001, false).`
`ml_perfil_cluster(c_001, joven_riesgoso).`

Con el archivo `hechos_base.pl` completamente escrito con datos crudos y predicciones de Inteligencia Artificial, el componente Neuro finaliza su trabajo y le cede el paso al Cerebro Lógico (Prolog).
