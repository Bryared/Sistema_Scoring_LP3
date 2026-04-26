# Capítulo 6: El Cerebro Lógico - `motor_inferencia.pl`

Este capítulo desglosa la teoría y el código detrás del archivo `motor_inferencia.pl`, el cual actúa como el "Cerebro Simbólico" de nuestra arquitectura.

## 6.1. Teoría: ¿Por qué Prolog y cómo funciona?
Prolog (Programming in Logic) es un lenguaje de Inteligencia Artificial Simbólica basado en la lógica de predicados de primer orden. 
A diferencia de lenguajes como Python o Java (imperativos), Prolog es **declarativo**. No se le dice "cómo" hacer algo, sino "qué" es verdad. 

El motor funciona mediante:
1. **Backward Chaining (Encadenamiento hacia atrás):** Si le preguntamos `?- dictamen_final(c_001, Resultado).`, Prolog buscará el objetivo (Resultado) e irá hacia atrás verificando si las premisas o reglas que lo componen son ciertas basándose en los hechos (los datos del cliente).
2. **Corte Lógico (`!`):** Es un operador fundamental en nuestro código. Le dice a Prolog: *"Si entraste a esta regla y es verdad, detente y no busques más alternativas"*. Esto ahorra muchísima memoria RAM y hace que el motor responda en milisegundos.

---

## 6.2. Desglose del Código: De principio a Fin

### Inclusión de Hechos
El archivo comienza con `:- include('hechos_base.pl').`. Esto "fusiona" nuestra base de datos generada por Python con las leyes del banco escritas en Prolog.

### Módulo 1: Prevención de Fraude Lógico
Aquí se definen las Reglas de rechazo inmediato.
```prolog
es_fraude(Id) :- dni_vencido(Id, true), format('...').
es_fraude(Id) :- tiempo_llenado(Id, S), S < 10, format('...').
```
Prolog evalúa línea por línea. Si el DNI está vencido, la regla `es_fraude` se vuelve verdadera (`true`) y lanza un `format` (un mensaje en consola que servirá para la explicabilidad XAI). Si no es fraude, Prolog simplemente salta a la siguiente sección.

### Módulo 2: Evaluación de Scoring Crediticio (Neuro-Simbólica)
Esta sección calcula si es viable prestarle dinero al usuario.
```prolog
carga_financiera(Id, Porcentaje) :- ...
```
Esta es una regla matemática pura. Suma las deudas y las divide entre los ingresos para calcular el **Debt Service Ratio (DSR)**.

A continuación, Prolog consume las predicciones inyectadas por Python:
```prolog
riesgo_alto_credito(Id) :-
    carga_financiera(Id, Carga), ml_perfil_cluster(Id, joven_riesgoso), Carga > 25.
```
Aquí la teoría Neuro-Simbólica brilla: Prolog exige que la Carga sea solo > 25% si y solo si el cliente pertenece al clúster Machine Learning `joven_riesgoso`. Hace lo mismo con la Regresión Logística (`ml_probabilidad_default > 0.85`). Si se cumplen, `riesgo_alto_credito` se vuelve `true`.

### Módulo 3: El Árbol de Decisión (Dictamen Final)
Es la función central del sistema que el dashboard manda llamar. El **orden** de las reglas aquí es crítico:
1. Primero revisa el fraude: `dictamen_final(..., 'DENEGADO...') :- es_fraude(Id), !.` (Si hay fraude, el `!` bloquea el resto del código).
2. Luego revisa Anomalías ML (Isolation Forest).
3. Luego las Alertas de Personas Expuestas Políticamente (PEP).
4. Luego el riesgo crediticio de impago.
5. Finalmente, aprueba a los que logran esquivar todos los filtros anteriores.

### Módulo 4: Prevención de Lavado de Activos (AML y Smurfing)
La regla más compleja topológicamente: `alerta_aml`.
```prolog
transferencia(Id, B, Monto1, Ts1, ...), 
transferencia(B, C, Monto2, ...),
transferencia(C, Id, Monto3, Ts3, ...).
```
Busca en la red si existe un ciclo `A -> B -> C -> A`. 
**Teoría AML Estricta:** Un ciclo no significa lavado si se demoró 5 años. Por eso, calculamos `Ts3 - Ts1` (Timestamp final menos inicial) y exigimos matemáticamente que sea `<= 259200` (72 horas).
**Teoría Neuro-Simbólica (NLP):** Si la IA de Python inyectó el hecho `ml_texto_sospechoso`, Prolog activa una reducción de tolerancia (`ToleranciaFinal is ToleranciaBase / 2`). Esto vuelve al algoritmo más agresivo si hay descripciones de transferencias extrañas.

### Módulo 5 y 6: Compliance SBS e Indecopi
Son evaluaciones estáticas. 
- `intervencion_sbs` revisa que tu nivel de endeudamiento no supere el 500% si tu patrimonio es líquido, o el 300% si es inmobiliario (difícil de vender ante embargos).
- `auditoria_cobros` es un Smart Contract puro: Si `tasa_cobrada` > `tasa_acordada`, salta la alarma de "Cobro Indebido", cumpliendo normativas Indecopi.
