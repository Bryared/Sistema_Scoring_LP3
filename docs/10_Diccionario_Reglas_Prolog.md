# Capítulo 10: Diccionario Lógico de las 50 Reglas (Prolog)

Este documento fue creado con fines puramente académicos y pedagógicos. Su propósito es explicar una a una las 50 reglas que componen el "Cerebro Lógico" de nuestro sistema experto (`motor_inferencia.pl`), para que cualquier estudiante o investigador pueda entender cómo se traduce la lógica financiera real a código Prolog.

---

## Módulo 1: Fraude y Seguridad Cibernética (7 Reglas)
Estas son reglas de exclusión absolutas (Hard Rules). Usan el predicado `es_fraude/1`.

1. **DNI Vencido:** `es_fraude(Id) :- dni_vencido(Id, true).` -> Bloquea a clientes indocumentados.
2. **Listas Negras OFAC:** `es_fraude(Id) :- en_lista_ofac(Id, true).` -> Bloquea a sancionados internacionales (lavado/terrorismo).
3. **Países de Alto Riesgo:** `es_fraude(Id) :- ubicacion_ip(Id, Pais), pais_riesgo(Pais).` -> Bloquea si la IP es de un país sancionado (ej. Rusia, China).
4. **Ataque de Fuerza Bruta:** `es_fraude(Id) :- intentos_login(Id, Intentos), Intentos > 3.` -> Bloquea si hay múltiples intentos de contraseña fallidos.
5. **Ataque de Bots:** `es_fraude(Id) :- tiempo_llenado(Id, S), S < 10.` -> Si llenó el formulario bancario en menos de 10 segundos, es un bot de auto-fill, no un humano.
6. **Uso de VPNs Sospechosas:** `es_fraude(Id) :- ubicacion_ip(Id, IP), residencia(Id, Res), IP \= Res, justificacion_vpn(Id, false).` -> Bloquea si la IP no coincide con su país y no hay justificación (ej. viaje de negocios).
7. **Equipos Robados:** `es_fraude(Id) :- dispositivo_imei(Id, Imei), imei_en_lista_negra(Imei).` -> Bloquea si el dispositivo móvil fue reportado como robado.

---

## Módulo 2: Riesgo Crediticio y Reglas Neuro-Simbólicas (8 Reglas)
Evalúan si el cliente tiene capacidad de pago. Usa `riesgo_alto_credito/1`.

8. **Cálculo de Carga Financiera:** `carga_financiera(Id, Porcentaje) :- ...` -> (1 regla) Suma las cuotas mensuales de deuda que tiene el cliente y las divide entre su salario.
9. **Límite Joven Riesgoso:** Si Machine Learning lo clasificó como "Joven Riesgoso", Prolog rechaza si su carga supera el 25%.
10. **Límite Emprendedor Promedio:** Si ML lo clasificó como "Emprendedor", Prolog permite deuda hasta el 35% de su sueldo.
11. **Límite Familia Estable:** Si ML detecta "Familia Estable", Prolog es más flexible y le permite endeudarse hasta el 40%.
12. **Probabilidad de Quiebra (ML):** Si la predicción probabilística de la Red Neuronal supera el 85% de riesgo, Prolog lo rechaza inmediatamente.
13. **Ruleteo Crediticio:** Rechaza al cliente si actualmente está pagando más de 3 créditos al mismo tiempo en distintos bancos.
14. **Desesperación Crediticia:** Rechaza si el cliente ha consultado su historial bancario más de 5 veces en los últimos 15 días (buscando dinero urgente).
15. **Morosidad:** Rechaza si su comportamiento de pago general está marcado como "moroso".

---

## Módulo 3: Aprobación y Onboarding (11 Reglas)
Dictaminan el resultado final usando el predicado `dictamen_final/2` apoyado por sub-reglas auxiliares.

**Sub-reglas Auxiliares (4 reglas):**

16. **Capacidad Sólida:** Requiere ganar más de S/.2000 y llevar más de 12 meses en su empleo actual.
17. **Historial Impecable:** Requiere que sus pagos anteriores sean siempre puntuales.
18. **Estabilidad Alta:** Requiere vivir más de 24 meses en la misma casa y trabajar en tecnología, salud o educación.
19. **Respaldo Digital:** Requiere un uso intensivo (alto) de billeteras digitales.

**Reglas de Decisión Final - El Juez (7 reglas):**

20. **Fraude (Cut):** Si `es_fraude` es verdadero, el dictamen es "DENEGADO POR SEGURIDAD". Detiene la ejecución gracias al operador `!`.
21. **Anomalía ML:** Si el algoritmo Isolation Forest detecta comportamiento invisible, el dictamen exige "VALIDACION BIOMETRICA FACIAL".
22. **Alerta PEP:** Si es una Persona Políticamente Expuesta, se deriva a "EVALUACION MANUAL".
23. **Riesgo Alto:** Si `riesgo_alto_credito` se activa, se dictamina "DENEGADO POR RIESGO".
24. **Aprobado Premium:** Si cumple Capacidad Sólida, Historial Impecable y Estabilidad Alta.
25. **Aprobado Estándar:** Si gana más de S/.800, tiene Historial Impecable y Respaldo Digital.
26. **Zona Gris:** Si no cumple ninguna de las reglas anteriores, el sistema por defecto dictamina "REQUIERE EVALUACION MANUAL".

---

## Módulo 4: Prevención de Lavado de Activos / AML (3 Reglas)
Evalúan grafos transaccionales para detectar *Smurfing* (pitufeo).

27. **Detección de Smurfing (Regla Lógica Compleja):** `alerta_aml/3` busca si hay un envío grande de dinero (ej. 10k) que triangule pasando por 3 cuentas distintas y regrese a la cuenta original en menos de 72 horas (259200 segundos). Si el sistema NLP detecta palabras raras ("inversion xyz"), disminuye la tolerancia a la mitad para cazar el lavado.
28. **Pase Limpio:** Si no cumple el patrón anterior, dictamina 'SIN RIESGO DE LAVADO'.
29. **Trazabilidad de Nodos:** `traza_aml_nodos/7` reconstruye matemáticamente el grafo de las cuentas puente para que Python dibuje el esquema en pantalla con Plotly.

---

## Módulo 5 y 6: Compliance SBS e Indecopi (5 Reglas)
Auditan el marco regulatorio del banco.

30. **Riesgo Insolvencia (Líquido):** Si el patrimonio principal es líquido (efectivo), la SBS permite que la deuda no supere 5 veces ese patrimonio.
31. **Riesgo Insolvencia (Inmobiliario):** Si el patrimonio son casas/terrenos, al ser menos líquidos, la deuda máxima no puede superar 3 veces su valor. Si lo pasa, lanza alerta.
32. **Aprobación SBS:** Regla por defecto que declara 'SOLVENTE' si no se rompen los límites de deuda.
33. **Cobro Indebido (Indecopi):** `auditoria_cobros` audita Contratos Inteligentes. Si la tasa cobrada en el sistema es mayor a la tasa firmada en el contrato, emite "COBRO INDEBIDO DETECTADO".
34. **Auditoría Limpia:** Si las tasas cuadran, emite 'CONTRATO LIMPIO'.

---

## Módulo 7: Scoring Cuantitativo Numérico (16 Reglas)
Este módulo asigna un puntaje tradicional de 0 a 1000 al cliente sumando y restando bonos por su comportamiento.

**Ingresos (3 reglas):**
35. `+100 pts` si gana más de 2000.
36. `+50 pts` si gana más de 800.
37. `0 pts` por defecto.

**Historial (3 reglas):**
38. `+150 pts` por pagos puntuales.
39. `-200 pts` como fuerte castigo por pagos morosos.
40. `0 pts` por defecto.

**Billetera Digital (2 reglas):**
41. `+50 pts` por modernidad (uso alto de billetera).
42. `0 pts` por defecto.

**Estabilidad (2 reglas):**
43. `+100 pts` si vive más de 24 meses en la misma casa (no es fugitivo/golondrino).
44. `0 pts` por defecto.

**Riesgo y Penalizaciones Clásicas (3 reglas):**
45. `-100 pts` si tiene más de 3 créditos activos.
46. `-50 pts` si ha hecho demasiadas consultas recientes.
47. `0 pts` por defecto.

**Penalización Inteligente ML (2 reglas):**
48. *Regla Matemática:* Resta la probabilidad de impago proyectada por la Red Neuronal multiplicada por 200. (Ej: 50% de probabilidad de no pagar resta -100 pts directos).
49. `0 pts` por defecto.

**Motor de Cálculo y Normalización (1 regla):**
50. `calcular_score/2`: Suma todos los puntos (Inicia en un base de 500) y le pone un candado para que matemáticamente el puntaje final jamás exceda los `1000` puntos ni sea inferior a `0` puntos.
