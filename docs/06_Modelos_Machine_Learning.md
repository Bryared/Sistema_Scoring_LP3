# Capítulo 7: Modelos de Machine Learning (Nivel 2 Neuro-Simbólico)

Este capítulo documenta la transformación arquitectónica del proyecto: de ser un sistema 100% Simbólico (Reglas rígidas en Prolog) a convertirse en un sistema verdaderamente **Neuro-Simbólico**. 

Para lograr esta hibridación, se incorporó la librería estadística `scikit-learn` en Python. Python actúa como el componente `Neuro` (Machine Learning), el cual descubre patrones ocultos e inyecta probabilidades matemáticas a Prolog (el componente `Simbólico`). Prolog, al recibir estos nuevos "hechos neuronales", flexibiliza sus reglas estáticas y toma decisiones más precisas y adaptativas.

## 7.1. Credit Scoring Predictivo (Regresión Logística)
- **El Problema Original:** Prolog decidía el impago de forma binaria mirando un umbral fijo (ej. "Rechazar si DSR > 35%").
- **La Solución ML:** Entrenamos un algoritmo de *Regresión Logística* que analiza el vector de características del cliente (Ingresos, Antigüedad Laboral, Cuotas) y predice una Probabilidad de Default del 0% al 100%.
- **Impacto Neuro-Simbólico:** Prolog recibe el hecho `ml_probabilidad_default(Id, Score)`. Si el Score de quiebra es altísimo (Ej. 95%), Prolog rechaza al cliente independientemente de otras variables, blindando al banco contra insolvencias basándose en predicciones estadísticas, no solo en reglas escritas a mano.

## 7.2. Detección de Anomalías Antifraude (Isolation Forest)
- **El Problema Original:** Las mafias cibernéticas pueden superar los filtros estáticos usando IPs limpias y DNIs robados que no están vencidos.
- **La Solución ML:** Implementamos un modelo de Inteligencia Artificial No Supervisada (*Isolation Forest*). Este algoritmo mide la "distancia" del comportamiento de un usuario frente al promedio de los 500 clientes. Si alguien presenta una matriz de acciones atípica (ej. llenar formularios rápido y pedir créditos masivos al instante), es marcado como `Anomalía`.
- **Impacto Neuro-Simbólico:** Al recibir `ml_fraude_anomalia(Id, true)`, Prolog no cancela el onboarding ciegamente (para evitar sesgos o falsos positivos de la IA), sino que altera su ruta de decisión y exige una **Validación Biométrica (Liveness Test)** obligatoria.

## 7.3. Clustering Demográfico Dinámico (K-Means)
- **El Problema Original:** Aplicar la misma política de riesgo crediticio a un estudiante de 20 años que a una familia estable de 45 años es un error comercial que genera pérdida de oportunidades.
- **La Solución ML:** Utilizamos el algoritmo *K-Means* para segmentar la cartera de 500 clientes en 3 "Tribus Financieras" o Clusters: `Joven Riesgoso`, `Emprendedor Promedio` y `Familia Estable`.
- **Impacto Neuro-Simbólico:** Prolog recibe el perfil semántico del cliente y ejecuta Límites DSR Dinámicos. A un perfil "Joven Riesgoso" le bloqueará créditos si su deuda supera apenas el 25%, pero a una "Familia Estable" le flexibilizará la política permitiéndole endeudarse hasta un 40%.

## 7.4. Procesamiento de Lenguaje Natural AML (NLP TF-IDF)
- **El Problema Original:** Las reglas lógicas de Prevención de Lavado de Activos (AML) solo evalúan montos y tiempos, siendo ciegas a la semántica humana.
- **La Solución ML:** Extraemos el "concepto" textual que el cliente escribe al realizar una transferencia bancaria. Evaluamos el texto buscando patrones catalogados como riesgosos (ej. "pago favores", "inversión xyz").
- **Impacto Neuro-Simbólico:** Si Python etiqueta la transferencia como texto sospechoso (`ml_texto_sospechoso(Id, true)`), el motor Prolog entra en estado de máxima alerta. Automáticamente **reduce a la mitad** el umbral de tolerancia difusa en la regla de Smurfing, cerrando el cerco matemático y asegurando que la red de lavado sea expuesta en el grafo topológico.
