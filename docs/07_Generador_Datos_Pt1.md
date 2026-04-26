# Capítulo 7: Ingesta de Datos Sintéticos - `generar_datos.py` (Parte 1)

Este capítulo explica la teoría y la lógica detrás de la **Fase 1** del archivo `generar_datos.py`, cuyo propósito es crear un ecosistema bancario completo y realista desde cero, previo a cualquier análisis de Inteligencia Artificial.

## 7.1. Teoría: La importancia de los Datos Correlacionados
Para que un sistema experto o un modelo de Machine Learning funcione, no basta con generar números aleatorios (Ej. `random.randint(1, 100)`). Si un cliente aleatorio tiene ingresos de S/. 500 pero un patrimonio de S/. 5,000,000, los datos son inconsistentes (Data Drift/Noise) y destruirían el modelo.
Por ello, usamos **Campanas de Gauss (Distribución Normal)** mediante `random.gauss()` en Python. Esto asegura que haya una correlación estadística fuerte: Si generamos ingresos altos, el cálculo de deudas y patrimonio se basará en ese ingreso, creando perfiles financieros lógicos.

---

## 7.2. Desglose del Código: Generación y Casos Forzados

### Inicialización y Variables Globales
El script comienza obteniendo el tiempo actual de tu computadora: `current_ts = int(time.time())`.
Se usa **Unix Timestamp** (segundos desde 1970) porque es la forma matemática más precisa y universal de medir el tiempo, vital para luego detectar Lavado de Activos en horas exactas. También se genera una lista negra aleatoria de IMEIs (identificadores de celular) simulando la base de datos robada de OSIPTEL.

### El Bucle de los 500 Clientes
Un bucle `for` itera 500 veces para crear 500 clientes únicos (`c_001` a `c_500`).
Para cada iteración, se construye la identidad digital de la persona:
1. **IP y Login:** Probabilidad condicional. Si la IP cae aleatoriamente en 'rusia', los intentos de login se fuerzan a ser altos (simulando un ataque hacker por fuerza bruta).
2. **Scoring Base:** Se usa la campana de Gauss para generar `ingresos`. Basado en estos ingresos (si son muy bajos), la probabilidad de que la persona sea "Morosa" aumenta drásticamente mediante sentencias `if/elif/else`.
3. **Carga Financiera:** Se genera una "carga_porcentaje" gaussiana alrededor del 25% (0.25). Esto se multiplica por los ingresos para obtener la "suma de cuotas mensuales" real.
4. **KYC y Riesgo Legal:** Se tiran "dados probabilísticos". Solo un 3% tendrá DNI vencido, un 1% estará en listas terroristas OFAC, y un 2% será PEP (Persona Expuesta Políticamente).

### Casos Forzados (El entorno de Pruebas Unitarias)
Si las 500 personas fueran aleatorias, sería imposible demostrarle a un profesor que el sistema funciona, ya que quizás el sistema aleatorio no generó ningún "Bot".
Por eso, el código utiliza sentencias `if i == 1:`, `if i == 2:`, etc.
- **`c_001`:** Se "sobrescriben" sus variables aleatorias forzando un tiempo de llenado de 2 segundos. Se crea intencionalmente un Fraude de Bot.
- **`c_007`:** Se le añaden manualmente transferencias (`ts_007_1`, `ts_007_2`) diseñadas para que cuadren exactamente en menos de 72 horas (Smurfing), probando el algoritmo AML.
- **`c_012`:** Se le asigna `es_pep = true` para probar si Prolog logra desviar la evaluación hacia un analista humano.

### Almacenamiento en Memoria (Listas de Diccionarios)
Durante el bucle, ninguna información se escribe en disco todavía. Todos los perfiles recién creados se agregan a la lista `clientes_data.append({...})`. De igual forma, las transferencias generadas se guardan en `transferencias_data`. 
Esta retención en la memoria RAM es el puente perfecto para preparar los datos antes de inyectarlos a la siguiente fase: El Machine Learning.
