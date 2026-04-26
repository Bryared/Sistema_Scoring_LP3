# Investigación Formativa: Sistema Experto Fintech de Onboarding Dual mediante IA Neuro-Simbólica

**Asignatura:** Lenguaje de Programación III  
**Institución:** Universidad Nacional Agraria La Molina (UNALM)



## 5. Conclusiones para Medio Curso
Esta integración demuestra de manera didáctica el poder de los algoritmos de Inteligencia Artificial (Redes y Genéticos) actuando como proveedores de "datos probabilísticos", y Prolog actuando como el juez que toma la decisión final basada en reglas y emite una justificación transparente. Es un ejemplo perfecto de sistemas híbridos para la banca moderna.
## 1. Título del sistema experto
**Sistema Experto de Onboarding Dual para Fintech mediante IA Neuro-Simbólica.**

La finalidad de este sistema experto es detectar fraude, resolver casos de incertidumbre y evaluar riesgo crediticio con criterios ya definidos y explicables. Se enfoca en la automatización de la evaluación de clientes para procesos de onboarding financiero.

## 2. Objetivo del sistema
El objetivo del sistema experto es el poder analizar el perfil de un cliente y determinar si es aprobado, rechazado o derivado a evaluación manual, todo en el contexto de onboarding financiero. Este sistema está dirigido a las áreas de riesgo, analistas de cumplimiento y personal técnico sujeto a tomar decisiones automáticas, transparentes y consistentes.

Este sistema también explica por qué un cliente es aceptado o rechazado, con ayuda de toda la información que se ha brindado del cliente y sus señales de comportamiento, variables de seguridad y predicciones de Machine Learning que están convertidas en hechos lógicos en Prolog.

## 3. Base de conocimiento
La base de conocimientos usada está definida por reglas de inferencia definidas ya en el archivo `motor_inferencia.pl`, siendo compuesta por hechos atómicos almacenados en el archivo `hechos_base.pl`.

### 3.1 Hechos principales
Los hechos describen la situación de cada cliente:
- `ubicacion_ip/2`: país desde donde se conecta el cliente.
- `intentos_login/2`: número de intentos de acceso.
- `ingresos/2`: nivel de ingresos del cliente.
- `pago_servicios/2`: comportamiento de pago.
- `antiguedad_laboral/2`: tiempo de permanencia laboral.
- `billetera_digital/2`: nivel de uso de billetera digital.
- `patrimonio/2`: valor patrimonial del cliente.
- `deuda_total/2`: total de deuda acumulada.
- `tasa_acordada/2` y `tasa_cobrada/2`: comparación de tasas para detectar cobros indebidos.
- `transferencia/6`: historial de transferencias con origen, destino, monto, timestamp, fecha y concepto.
- `tiempo_llenado/2`: tiempo que tardó el cliente en completar el formulario.
- `residencia/2`: país de residencia.
- `justificacion_vpn/2`: si existe o no justificación para el uso de VPN.
- `dispositivo_imei/2`: IMEI del dispositivo.
- `imei_en_lista_negra/1`: IMEIs sospechosos o bloqueados.
- `suma_cuotas_mensuales/2`: carga financiera mensual.
- `antiguedad_domicilio/2`: estabilidad domiciliaria.
- `sector_laboral/2`: sector económico del cliente.
- `creditos_activos/2`: número de créditos vigentes.
- `consultas_bancarias_15dias/2`: cantidad de consultas recientes.
- `tipo_patrimonio/2`: tipo de activo principal.
- `dni_vencido/2`: documento vencido o vigente.
- `en_lista_ofac/2`: coincidencia con listas de sanción.
- `es_pep/2`: si el cliente es persona políticamente expuesta.
- `ml_probabilidad_default/2`: probabilidad de incumplimiento generada por ML.
- `ml_fraude_anomalia/2`: detección de anomalías por Isolation Forest.
- `ml_perfil_cluster/2`: perfil del cliente según K-Means.
- `ml_texto_sospechoso/3`: detección de lenguaje sospechoso en transferencias.

Con todos estos hechos se logra trabajar no solo con datos financieros clásicos, sino también con el comportamiento digital que tiene el cliente, como algunas señales de fraude y predicciones neuronales.

### 3.2 Reglas principales
El motor contiene reglas de inferencia organizadas por módulos. Las principales son las siguientes:

**a) Reglas de fraude y seguridad**
Al detectar señales críticas de fraude por parte de un cliente el sistema rechaza de manera inmediata, como por ejemplo:
- DNI vencido.
- Coincidencia en lista OFAC.
- IP desde país de alto riesgo.
- Múltiples intentos de login.
- Formulario completado demasiado rápido.
- VPN sin justificación.
- IMEI en lista negra.

Estas reglas tienen prioridad alta porque la seguridad debe evaluarse antes que el scoring crediticio.

**b) Reglas de scoring crediticio**
Este sistema, con la relación entre cuotas mensuales e ingresos, logra calcular la carga financiera. Luego de ello evalúa el riesgo con reglas clásicas:
- Si el cliente tiene muchos créditos activos, se considera posible "ruleteo".
- Si tiene demasiadas consultas bancarias recientes, se interpreta como señal de desesperación crediticia.
- Si presenta morosidad histórica, aumenta el riesgo.
- Si su probabilidad de default generada por ML es muy alta, también se rechaza.
- El clúster asignado por K-Means ajusta el umbral de aceptación:
  - *joven_riesgoso*: límite más estricto.
  - *emprendedor_promedio*: límite intermedio.
  - *familia_estable*: límite un poco más flexible.

**c) Reglas de aprobación**
El sistema tiene como regla de aprobación las condiciones de estabilidad, buen comportamiento de pago y el respaldo digital. Existen dos niveles:
- **Aprobado Premium:** para clientes con ingresos altos, buen historial, estabilidad laboral y domicilio sólido.
- **Aprobado Estándar:** para clientes con ingresos suficientes, pagos puntuales y alto uso de billetera digital.

**d) Reglas de lavado de activos y AML**
El sistema detecta patrones tipo smurfing o triangulación a través del análisis de transferencias. Se evalúa si existe una cadena de movimientos entre tres cuentas en un intervalo corto de tiempo. Para reducir la tolerancia y hacer el análisis más estricto, el modelo NLP detecta palabras sospechosas como "xyz" o "inversion rapida".

**e) Reglas de compliance**
También se incluyen reglas para:
- **SBS:** detectar riesgo de insolvencia según el tipo de patrimonio y el nivel de deuda.
- **Indecopi:** detectar cobro indebido cuando la tasa cobrada supera la tasa acordada.

### 3.3 Lógica de las reglas
La lógica del sistema sigue una prioridad clara:
1. Primero se evalúa fraude y seguridad.
2. Luego se evalúa el riesgo crediticio.
3. Después se considera la posibilidad de aprobación.
4. Si el caso es ambiguo, se deriva a evaluación manual.
5. Finalmente, se aplican reglas de compliance y AML cuando corresponda.

Esta estructura permite una toma de decisiones ordenada, explicable y alineada con un entorno Fintech real.

## 4. Motor de inferencia
El motor de inferencia está implementado en Prolog y utiliza encadenamiento hacia atrás. 
Para activar el sistema, la consulta a utilizar es:

```prolog
?- evaluar_cliente(c_001).
```

A partir de esa consulta, Prolog ejecuta la regla `dictamen_final/2`, que revisa primero fraude, luego anomalías ML, luego PEP, después riesgo crediticio y finalmente reglas de aprobación.

Para mejorar la eficiencia y evitar respuestas contradictorias, se hace uso del operador cut (`!`) que impide que Prolog siga evaluando reglas innecesarias después de encontrar una decisión válida.

## 5. Sesión de prueba
A continuación, se muestran cinco consultas de prueba con su respuesta esperada por parte del sistema.

**Caso 1: Denegado por fraude**
- **Consulta:** `?- evaluar_cliente(c_001).`
- **Respuesta esperada:**
  ```text
  [XAI] ALERTA SEGURIDAD: ... 
  [XAI] DICTAMEN FINAL: Onboarding Cancelado por seguridad estricta.
  >> CONCLUSIÓN DEL SISTEMA: DENEGADO POR SEGURIDAD (FRAUDE LÓGICO DETECTADO)
  ```
- **Interpretación:** el cliente presenta señales críticas de fraude, como DNI vencido, país riesgoso, IMEI sospechoso o múltiples intentos de acceso.

**Caso 2: Rechazo por anomalía ML**
- **Consulta:** `?- evaluar_cliente(c_002).`
- **Respuesta esperada:**
  ```text
  [XAI] DICTAMEN FINAL: El modelo Isolation Forest detecto comportamiento invisible no catalogable.
  >> CONCLUSIÓN DEL SISTEMA: REQUIERE VALIDACION BIOMETRICA FACIAL (ANOMALIA ML DETECTADA)
  ```
- **Interpretación:** el comportamiento del cliente es anómalo según el modelo de Machine Learning.

**Caso 3: Denegado por riesgo crediticio**
- **Consulta:** `?- evaluar_cliente(c_003).`
- **Respuesta esperada:**
  ```text
  [XAI] RECHAZO NEURO-SIMBOLICO: ...
  [XAI] DICTAMEN FINAL: Onboarding Rechazado ...
  >> CONCLUSIÓN DEL SISTEMA: DENEGADO POR RIESGO CREDITICIO
  ```
- **Interpretación:** el cliente supera los límites de endeudamiento o tiene probabilidad alta de default.

**Caso 4: Aprobado premium**
- **Consulta:** `?- evaluar_cliente(c_005).`
- **Respuesta esperada:**
  ```text
  [XAI] DICTAMEN FINAL: Onboarding Exitoso (Premium).
  >> CONCLUSIÓN DEL SISTEMA: APROBADO PREMIUM
  ```
- **Interpretación:** el cliente muestra estabilidad laboral, buen historial de pagos y respaldo financiero.

**Caso 5: Aprobado estándar o evaluación manual**
- **Consulta:** `?- evaluar_cliente(c_004).`
- **Respuesta esperada:**
  ```text
  [XAI] DICTAMEN FINAL: Onboarding Exitoso (Estandar).
  >> CONCLUSIÓN DEL SISTEMA: APROBADO ESTÁNDAR
  ```
  o, en casos ambiguos:
  ```text
  >> CONCLUSIÓN DEL SISTEMA: REQUIERE EVALUACION MANUAL
  ```
- **Interpretación:** el sistema no encuentra una señal suficientemente fuerte para aprobar o rechazar de forma automática.

## 6. Reflexión personal
El principal reto fue modelar de forma correcta el conocimiento del problema en Prolog, es decir, traducir situaciones reales (fraude, riesgo crediticio, aprobación) en hechos y reglas lógicas coherentes. En un principio el sistema no presentaba con exactitud los criterios de decisión, por lo que se realizó un ajuste en las reglas para que representen correctamente cada caso.

También fue clave entender cómo el motor de inferencia procesa las consultas para tomar decisiones, permitiendo que el sistema no solo dé un resultado, sino que lo justifique. El resultado final fue un sistema experto que evalúa perfiles de clientes de manera lógica, estructurada y transparente.

## 7. Conclusión
El sistema experto que se desarrolló demuestra la capacidad de Prolog para la construcción de un motor de inferencia sólido, basado en reglas y decisiones que se justifican con los hechos.

El sistema emplea lógica simbólica para evaluar clientes de forma sistemática, priorizando seguridad, análisis de riesgo y aprobación. No solo se genera una respuesta, sino que el motor de inferencia justifica el razonamiento de cada decisión, un factor fundamental en el ámbito financiero. En consecuencia, queda evidenciado la utilidad de los sistemas expertos como una herramienta que puede ser transparente, consistente y útil para la toma de decisiones automatizada.
## 8. Conclusiones para Medio Curso
Esta integración demuestra de manera didáctica el poder de los algoritmos de Inteligencia Artificial (Redes y Genéticos) actuando como proveedores de "datos probabilísticos", y Prolog actuando como el juez que toma la decisión final basada en reglas y emite una justificación transparente. Es un ejemplo perfecto de sistemas híbridos para la banca moderna.