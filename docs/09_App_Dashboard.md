# Capítulo 9: Interfaz Web y Explicabilidad (XAI) - `app.py`

Este capítulo analiza el archivo `app.py`, el cual funciona como la capa de presentación (Frontend) de nuestra arquitectura. Está desarrollado utilizando la librería `Streamlit` en Python.

## 9.1. Teoría: La importancia de XAI y RegTech
En sistemas bancarios, no es suficiente que un algoritmo sea exacto; debe ser **Auditable**.
1. **XAI (Explainable AI):** Si la IA rechaza un crédito, el cliente tiene derecho a saber el porqué. Nuestra interfaz extrae el razonamiento del motor lógico y lo presenta de forma humana.
2. **RegTech (Regulatory Technology):** Simula el componente inmutable (Blockchain) que se le presentaría a un auditor de la SBS. Para lograrlo, aplicamos criptografía de modo que las decisiones no puedan ser alteradas retroactivamente por los empleados del banco.

---

## 9.2. Desglose del Código

### La Conexión con el Cerebro: `PySwip`
El bloque de código inicial intenta importar `Prolog` desde la librería puente `pyswip`.
```python
prolog = Prolog()
prolog.consult("motor_inferencia.pl")
```
Esto levanta todo el código lógico que explicamos en el Capítulo 6 y lo mantiene vivo en la memoria RAM de Python.
A continuación se crea la función auxiliar `q_string(query_str, var_name)`. Al usar PySwip, cuando haces una pregunta a Prolog, este retorna una estructura de datos algo compleja (Generadores con diccionarios de bytes). La función `q_string` envuelve esa petición, la ejecuta, extrae el resultado exacto y lo limpia de formatos basura para que Streamlit lo pueda imprimir elegantemente.

### El Cifrado Inmutable (`write_audit_log`)
El corazón de nuestra política de Compliance RegTech.
```python
sha_signature = hashlib.sha256(raw_data.encode()).hexdigest()
```
Cada vez que el usuario presiona "Evaluar" o "Escanear AML", Python empaqueta el Nombre del Cliente, la Fecha exacta y el Dictamen de Prolog en una sola cadena de texto. Se usa la librería `hashlib` para generar un **Hash SHA-256**. 
Un Hash es una huella digital matemática: si alguien entra al archivo `audit_trail_xai.log` y borra una coma del dictamen, el Hash original ya no cuadrará con el texto modificado, evidenciando el sabotaje ante los auditores legales.

### Estructura Visual (Los 3 Módulos)
El dashboard usa `st.tabs` para separar el ecosistema en 3 pestañas.

**TAB 1: Onboarding y Componente Neuro**
Muestra variables descriptivas usando `st.metric`. Invoca la función `q_string` para leer los modelos de Machine Learning (Score, Clúster) inyectados en la fase previa. Cuando presionas el botón de "Evaluar", invoca la query principal de Prolog: `?- dictamen_final(...)`. Atrapa el resultado y muestra una bandera roja (error) o verde (success) según el string retornado. Simultáneamente, graba el Hash inmutable.

**TAB 2: Grafo Interactivo AML**
Contiene un *Slider* visual que modifica en tiempo real la variable numérica "Tolerancia de Comisión".
Cuando se activa el escaneo, ejecuta la query `alerta_aml`. Si Prolog advierte de un "LAVADO DE ACTIVOS", la aplicación Python ejecuta otra query (`traza_aml_nodos`) para averiguar quiénes fueron los testaferros `B` y `C`.
Con esa información, instancia la librería `NetworkX` (Teoría de Grafos). Añade los Nodos (Clientes) y los Vértices (Monto Transferido) para construir la topología. Finalmente usa `Plotly` para dibujar el grafo interactivo con puntos rojos directamente en la interfaz.

**TAB 3: Compliance Legal SBS**
Evalúa el riesgo de insolvencia y llama al módulo lógico de Smart Contracts (`auditoria_cobros`). Si la tasa cobrada es distinta a la acordada, genera la alerta visual de Cobro Indebido. Genera también su respectivo registro Hash de auditoría.

Al finalizar, la barra lateral lateral izquierda incluye un botón que carga y lee en crudo el archivo `.log` generado, demostrando la inmutabilidad de la trazabilidad generada durante toda la sesión.
