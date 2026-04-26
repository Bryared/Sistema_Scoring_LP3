# Investigación Formativa: Sistema Experto Fintech mediante IA Neuro-Simbólica y Evolutiva

**Asignatura:** Lenguaje de Programación III  
**Institución:** Universidad Nacional Agraria La Molina (UNALM)

---

## 1. Planteamiento del Problema
En el sector Fintech de Perú, un gran porcentaje de ciudadanos son **"Invisibles Financieros"** (personas sin historial crediticio tradicional). Los modelos neuronales modernos de Machine Learning a menudo categorizan el riesgo como una "Caja Negra", arrojando puntuaciones sin explicación. Sin embargo, entidades regulatorias como la SBS requieren justificación (explicabilidad) para denegar un producto financiero. Además, las instituciones financieras enfrentan el problema de **optimización de cartera**: poseen un presupuesto limitado para préstamos y necesitan seleccionar a los clientes que maximicen la rentabilidad mientras minimizan el riesgo de impago.

Para resolver esto, se ha implementado un sistema que cubre la **Unidad 1 y Unidad 2 del sílabo**, combinando:
1. **Inteligencia Artificial Neuronal (Scoring Predicativo):** Un Perceptrón Multicapa (MLP).
2. **Computación Evolutiva (Optimización de Cartera):** Un Algoritmo Genético.
3. **IA Simbólica (XAI y Compliance):** Un Motor de Inferencia en Prolog.

---

## 2. Redes Neuronales: Predicción de Default (Unidad 2)
Se implementó un modelo **Perceptrón Multicapa (MLPClassifier)** utilizando `scikit-learn` (`modelo_neuronal.py`). 
Este modelo se entrena con variables continuas y categóricas (Ingresos, intentos de login, antigüedad laboral, DSR/Carga Financiera y nivel de adopción de Billetera Digital).
- **Algoritmo de Aprendizaje:** Backpropagation con optimizador `adam` (función de activación `relu`).
- **Función:** Retorna la probabilidad matemática de impago (Default Risk) entre 0 y 1. 
- **Integración:** La salida estocástica de esta Red Neuronal alimenta como "Hecho Lógico" a la base de conocimiento de Prolog, superando la limitación de la lógica determinista pura ante la incertidumbre humana.

---

## 3. Algoritmos Genéticos: Optimización de Cartera (Unidad 2)
Para resolver la restricción de capital del banco, se desarrolló un Algoritmo Genético utilizando la librería `DEAP` (`algoritmo_genetico.py`). 
El problema se modeló matemáticamente como una variante del **Knapsack Problem (Problema de la Mochila)**:
- **Individuo:** Un cromosoma booleano de longitud $N$ (donde $N$ es el número de clientes pre-aprobados). El gen 1 significa "otorgar préstamo", el gen 0 significa "rechazar".
- **Función de Aptitud (Fitness):** Maximizar el retorno esperado neto.
  $$ Fitness = \sum (P_i \times T_i) - (P_i \times Risk_i) $$
  *(Donde $P$ es el préstamo, $T$ la tasa de interés, y $Risk$ la probabilidad de default generada por la Red Neuronal).*
- **Restricción:** La suma de los préstamos otorgados no debe superar el presupuesto máximo (ej. S/. 1,000,000). Si lo supera, el individuo recibe una penalidad severa.
- **Operadores:** Cruzamiento de dos puntos (`cxTwoPoint`), mutación de bit-flip (`mutFlipBit`) y selección por torneos.

---

## 4. Motor de Inferencia Simbólico y Módulo XAI (Unidad 1)
El archivo `motor_inferencia.pl` contiene reglas diseñadas con lógica de árbol top-down y "Backward Chaining", incorporando el predicado Cut (`!`) para eficiencia de búsqueda. Toma la probabilidad de la red neuronal y los hechos del usuario, y realiza:
1. **Prevención de Fraudes y AML (Anti-Money Laundering):** Corta operaciones ante IP de riesgo, triangulación rápida de dinero (Smurfing < 72h) y validación en listas OFAC/PEP.
2. **Compliance SBS:** Validación de límites de deuda/patrimonio.
3. **XAI (Explainability):** Imprime el dictamen final con la fundamentación algorítmica y humana del porqué se aprueba o rechaza a un cliente, asegurando transparencia legal.

### Sesión de Pruebas y Uso Interactivo
Gracias a la implementación interactiva, el sistema permite introducir **Nuevos Clientes** en tiempo real. Al hacerlo, la Red Neuronal evalúa su probabilidad inmediatamente, y luego el Motor de Inferencia los analiza generando un rastro de auditoría inmutable basado en Hash Criptográfico.

---

## 5. Conclusiones (Reflexión Final)
El desarrollo del proyecto cumple cabalmente los lineamientos del curso Lenguaje de Programación III. Se logró integrar exitosamente un paradigma de **IA Neuro-Simbólica con Computación Evolutiva**:
1. Las **Redes Neuronales** clasifican el riesgo implícito con alta precisión y capturan la no-linealidad de los datos.
2. Los **Algoritmos Genéticos** resuelven eficientemente el problema NP-Hard de asignación de capital, priorizando los perfiles de riesgo más rentables bajo restricciones financieras estrictas.
3. El **Motor Simbólico (Prolog)** actúa como árbitro final, garantizando el cumplimiento regulatorio estricto y proporcionando la Explicabilidad (XAI) exigida por las normativas bancarias modernas, algo que ninguna IA de tipo "Caja Negra" puede ofrecer por sí sola de manera legal y auditable.
