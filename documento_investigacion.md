# Investigación Formativa: Sistema Experto de Onboarding Dual mediante IA Neuro-Simbólica

**Asignatura:** Lenguaje de Programación III  
**Institución:** Universidad Nacional Agraria La Molina (UNALM)

---

## 1. Planteamiento del Problema
En el sector Fintech de Perú (y América Latina en general), un gran porcentaje de ciudadanos son **"Invisibles Financieros"** (personas sin historial crediticio tradicional). Los modelos neuronales modernos de Machine Learning a menudo categorizan el riesgo como una "Caja Negra", arrojando puntuaciones sin explicación. Sin embargo, entidades regulatorias como la SBS requieren justificación (explicabilidad) para denegar un producto financiero u onboarding.

Para resolver esto, se propone el uso de **IA Neuro-Simbólica**. Se simula un componente Neuronal (que captura datos difusos de comportamiento y los traduce a hechos lógicos) y un Motor de Inferencia Simbólico (XAI) programado en **Prolog**, capaz de generar decisiones transparentes con alta explicabilidad algorítmica sobre Scoring y Prevención de Fraudes.

---

## 2. Base de Conocimiento (Generación Estadística)
La base de hechos (`hechos_base.pl`) se construyó empleando un **algoritmo generador en Python** (`generar_datos.py`). 
En lugar de valores completamente aleatorios, usamos distribuciones probabilísticas (e.g., Distribución Normal para ingresos) y lógicas correlacionadas:
- Un mayor nivel de ingresos incrementa la probabilidad de ser `puntual` en `pago_servicios`.
- Países de riesgo (`rusia`, `china`) tienen configuradas tasas artificialmente más altas de "intentos de login" (simulando ataques de fuerza bruta).
Se generaron un total de **3000 hechos** atómicos válidos en Prolog correspondientes a **500 clientes únicos**.

---

## 3. Motor de Inferencia y Módulo XAI
El archivo `motor_inferencia.pl` contiene 13 reglas diseñadas con lógica de árbol top-down y "Backward Chaining", incorporando el predicado Cut (`!`) para eficiencia de búsqueda.

Las operaciones se segmentan en:
1. **Prevención de Fraudes:** Precedencia alta. Corta operaciones ante IP extranjera no segura y picos de logins.
2. **Scoring Crediticio:** Reglas sobre niveles de ingresos y solvencia laboral.
3. **Manejo de Incertidumbre:** Uso de una métrica alternativa (uso de `billetera_digital`) para justificar empíricamente perfiles estándar ante ingresos bajos.
4. **XAI (Explainability):** Empleo constante de predicados I/O tipo `format/2` para imprimir el dictamen y el razonamiento exacto.

---

## 4. Sesión de Pruebas (Test Cases)

A continuación, se presentan las simulaciones del motor de inferencia mostrando la funcionalidad XAI para los 5 escenarios solicitados:

### Caso 1: DENEGADO POR FRAUDE (Seguridad)
Se evaluó a `c_001` (Rusia, 5 intentos de login).
```text
?- evaluar_cliente(c_001).

======================================================
>> INICIANDO MOTOR DE INFERENCIA PARA CLIENTE: c_001

[XAI] ALERTA SEGURIDAD: Cliente c_001 rechazado. Conexion IP desde pais de altisimo riesgo (rusia).

[XAI] DICTAMEN FINAL: Onboarding Cancelado para c_001 por Riesgo de Fraude.
>> CONCLUSIÓN DEL EXPERTO: DENEGADO POR SEGURIDAD
======================================================
```

### Caso 2: DENEGADO POR SCORING (Morosidad)
Se evaluó a `c_002` (Ingresos bajos, pago de servicios Moroso, intentos de login: 1).
```text
?- evaluar_cliente(c_002).

======================================================
>> INICIANDO MOTOR DE INFERENCIA PARA CLIENTE: c_002

[XAI] DICTAMEN FINAL: Onboarding Rechazado para c_002 por Riesgo Crediticio.
[XAI] RAZONAMIENTO: El motor logico detecto comportamiento activo MOROSO en pagos de servicios.
>> CONCLUSIÓN DEL EXPERTO: DENEGADO POR SCORING
======================================================
```

### Caso 3: APROBACIÓN PREMIUM (Scoring Excelente)
Se evaluó a `c_003` (Puntual, Ingresos: 5500, Antigüedad: 48 meses).
```text
?- evaluar_cliente(c_003).

======================================================
>> INICIANDO MOTOR DE INFERENCIA PARA CLIENTE: c_003

[XAI] DICTAMEN FINAL: Onboarding Exitoso para c_003 (Nivel Premium).
[XAI] RAZONAMIENTO: Alta solvencia y arraigo laboral combinada con comportamiento puntual.
>> CONCLUSIÓN DEL EXPERTO: APROBADO PREMIUM
======================================================
```

### Caso 4: APROBACIÓN ESTÁNDAR (Fallback - Neuro-Simbólico)
Se evaluó a `c_004` (Ingresos Medios: 900, Puntual, Billetera Digital: Alto uso).
```text
?- evaluar_cliente(c_004).

======================================================
>> INICIANDO MOTOR DE INFERENCIA PARA CLIENTE: c_004

[XAI] DICTAMEN FINAL: Onboarding Exitoso para c_004 (Nivel Estandar).
[XAI] RAZONAMIENTO: Uso de Fallback. Ingreso modesto de S/.900 mitigado por pago de servicios puntual y alto nivel de Billetera Digital.
>> CONCLUSIÓN DEL EXPERTO: APROBADO ESTANDAR (FALLBACK)
======================================================
```

### Caso 5: INCERTIDUMBRE Y EVALUACIÓN MANUAL
Se evaluó a `c_005` (Ingresos: 1100, Pago: Atrasado, Billetera Digital: Medio).
```text
?- evaluar_cliente(c_005).

======================================================
>> INICIANDO MOTOR DE INFERENCIA PARA CLIENTE: c_005

[XAI] DICTAMEN FINAL: Cliente c_005 derivado para Evaluacion Manual por Incertidumbre.
[XAI] RAZONAMIENTO: Variables difusas. Ingresos: S/.1100 | Pagos: atrasado | Nivel Billetera: medio. No encaja en limites deterministas.
>> CONCLUSIÓN DEL EXPERTO: REQUIERE EVALUACION MANUAL
======================================================
```

---

## 5. Reflexión Académica
El uso del paradigma híbrido (Neuro-Simbólico) permite resolver de manera elegante problemas complejos en el negocio Fintech. Aunque las redes neuronales pueden clasificar e identificar patrones implícitos con alta precisión (simulado aquí con la asignación probabilística en Python), son inherentemente incapaces de fundamentar explícitamente y bajo reglas duras sus predicciones. La integración con Prolog como capa final de decisión demuestra el potencial de combinar modelos estadísticos con sistemas simbólicos: garantizan eficiencia tecnológica al tiempo que cumplen con estrictas exigencias éticas y regulatorias bancarias (Explicabilidad / XAI).
