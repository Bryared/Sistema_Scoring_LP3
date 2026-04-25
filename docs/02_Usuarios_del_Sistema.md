# Capítulo 3: Usuarios y Audiencia del Sistema

El sistema cuenta con una interfaz gráfica (Streamlit) que no está diseñada para el consumidor final, sino para los empleados clave del **Back-Office** de la institución financiera.

## 3.1. Analista de Riesgos (Risk Analyst)
- **Rol:** Aprobar o denegar créditos que caen en "Zonas Grises".
- **Uso en el sistema:** Revisa la pestaña de Onboarding. Aunque Prolog automatiza el 90% de las decisiones (rechazando estafadores y aprobando perfiles premium), el Analista interviene cuando el sistema detecta a una Persona Políticamente Expuesta (PEP), ya que la ley exige una evaluación humana para prevenir casos de corrupción.

## 3.2. Oficial de Cumplimiento (Compliance Officer)
- **Rol:** Proteger al banco de ser utilizado para lavar dinero del narcotráfico o terrorismo. Reportar a la Unidad de Inteligencia Financiera (UIF).
- **Uso en el sistema:** Utiliza la pestaña de **AML (Anti-Money Laundering)**. Juega con el *Slider de Tolerancia Difusa* para rastrear comisiones ocultas. Analiza el grafo visual interactivo (los nodos rojos) para descubrir exactamente quién le envió dinero a quién, y exporta el Log Inmutable como evidencia para la fiscalía.

## 3.3. Auditor Legal (SBS / Indecopi)
- **Rol:** Asegurar que el banco no cometa abusos contra el consumidor ni corra riesgos de insolvencia.
- **Uso en el sistema:** Revisa la pestaña de **Compliance SBS**. Usa el sistema de Auditoría de Contratos Inteligentes para probar que la Tasa de Interés Acordada en el contrato es matemáticamente idéntica a la Tasa Cobrada por el sistema central del banco. También audita la solidez de la cartera de clientes asegurando que el apalancamiento no supere 3x en patrimonios inmobiliarios y 5x en liquidez.