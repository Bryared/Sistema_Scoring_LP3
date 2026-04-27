# 🏦 Sistema Experto Fintech: Onboarding Dual Neuro-Simbólico

![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Prolog](https://img.shields.io/badge/Prolog-000000?style=for-the-badge&logo=prolog&logoColor=white)

🚀 **Demo en Vivo:** [https://marcianitos.streamlit.app/](https://marcianitos.streamlit.app/)

Bienvenido al **Sistema Experto de Onboarding Dual para Fintech**, un proyecto de investigación académica (UNALM - Lenguaje de Programación III) que implementa una arquitectura **Neuro-Simbólica**. 

Este sistema une lo mejor de dos mundos: la **Inteligencia Artificial (Python)** para cálculos probabilísticos y predicciones, y la **Lógica Simbólica (Prolog)** como un juez inquebrantable que toma decisiones basadas en reglas estrictas (Hard Rules), garantizando transparencia y explicabilidad (XAI).

---

## 📖 Tutorial de Uso (Cómo probar la App)

La aplicación cuenta con 5 módulos interactivos. Sigue estos pasos para probar el poder del sistema:

### 1. ➕ Nuevo Cliente
- **¿Qué hace?** Permite simular el registro de un nuevo cliente.
- **Prueba recomendada:** Intenta crear al "Cliente Perfecto". Ponle ingresos de `8000`, antigüedad laboral de `60` meses, nivel de billetera `alto` y pago `puntual`. Verás que la Red Neuronal le asignará un riesgo bajísimo. 

### 2. 📊 Onboarding (Scoring)
- **¿Qué hace?** Evalúa al cliente usando más de 50 reglas lógicas de Prolog cruzadas con Machine Learning.
- **Prueba recomendada:** Selecciona un cliente aleatorio (ej. `c_001` o el que creaste). El sistema te dirá si está **Aprobado**, **Rechazado** o si requiere **Evaluación Manual**. Además, te dará el **Score Final (0-1000)** y una justificación transparente de la decisión.

### 3. 🛡️ AML & Fraude
- **¿Qué hace?** Detecta patrones de Lavado de Activos (Smurfing) mediante el análisis de redes transaccionales.
- **Prueba recomendada:** Ejecuta el análisis AML. El sistema buscará triangulaciones de dinero rápidas y, si el NLP detecta palabras sospechosas, ajustará la tolerancia para cazar el fraude. Verás el grafo de transferencias interactivo.

### 4. ⚖️ Auditoría Legal y Compliance SBS
- **¿Qué hace?** Verifica que el banco cumpla con las normativas financieras.
- **Prueba recomendada:** Corre el *Compliance*. Validará si el cliente tiene riesgo de insolvencia (según SBS) y auditará mediante Contratos Inteligentes lógicos que la tasa de interés cobrada no sea mayor a la acordada (Indecopi).

### 5. 🧠 IA (Redes & Genéticos)
- **¿Qué hace?** Optimiza el presupuesto del banco usando la Teoría de la Evolución.
- **Prueba recomendada:** Usa el selector y escoge **"Optimizar Solo Pre-Aprobados"**. El Algoritmo Genético leerá a los clientes que Prolog aprobó, descartará a los poco rentables y seleccionará solo a la élite para maximizar la ganancia del banco sin exceder el presupuesto. Si seleccionas **"Optimizar Todo"**, verás cómo la IA pura invierte en masa ignorando el riesgo legal.

---

## 🏗️ Arquitectura Técnica

El sistema está dividido en dos grandes cerebros:

### 1. El Cerebro Lógico (Prolog) - *El Juez*
Implementado en `motor_inferencia.pl` y `hechos_base.pl`. Prolog evalúa reglas inquebrantables de negocio:
- **Fraude Hard Rules:** DNI vencido, IP sospechosa, listas OFAC = Rechazo automático.
- **Reglas de Negocio:** Historial impecable, ingresos mínimos, estabilidad domiciliaria = Aprobación.
- **Transparencia (XAI):** Cada decisión genera una traza de texto justificando *por qué* se tomó la decisión.

### 2. El Cerebro Estadístico (Python) - *El Asesor*
- **Machine Learning (`modelo_neuronal.py`):** Estima el riesgo probabilístico futuro (Probabilidad de Default). Estos cálculos se envían a Prolog como hechos lógicos.
- **Algoritmos Genéticos (`algoritmo_genetico.py`):** Optimiza la cartera de préstamos usando `DEAP`. Busca maximizar la rentabilidad descartando inversiones de riesgo o que superen el límite presupuestal del banco.

---

## ⚙️ Instalación Local (Desarrolladores)

Si deseas correr el proyecto en tu propia máquina:

1. Clona el repositorio.
2. Instala **SWI-Prolog** en tu sistema operativo y asegúrate de agregarlo a las variables de entorno (PATH).
3. Instala las dependencias de Python:
   ```bash
   pip install -r requirements.txt
   ```
4. Levanta la aplicación con Streamlit:
   ```bash
   streamlit run app.py
   ```

---
*Proyecto desarrollado para la asignatura de Lenguaje de Programación III - UNALM.*
