# Capítulo 1: Contexto Académico y Evolución del Proyecto

## 1.1. Origen del Proyecto
Este proyecto nace como una investigación formativa para la asignatura **Lenguaje de Programación III** de la **Universidad Nacional Agraria La Molina (UNALM)**. El requerimiento inicial era desarrollar un Sistema Experto basado en programación lógica (Prolog) capaz de procesar una base de conocimientos (hechos y reglas) para tomar decisiones.

## 1.2. De Asignación Académica a Core Bancario
Lo que comenzó como un modelo teórico escaló hacia la construcción de una arquitectura Fintech de nivel de producción. Nos dimos cuenta de que Prolog es la herramienta perfecta para resolver uno de los mayores problemas actuales en la banca: el problema de la **"Caja Negra"**.

En la banca moderna, si una Red Neuronal rechaza un crédito, el banco no sabe por qué lo hizo. Esto viola las normativas de la **SBS (Superintendencia de Banca y Seguros)**, que exigen explicabilidad para evitar discriminación. Al usar Prolog, construimos un motor de Inteligencia Artificial Simbólica (y luego Neuro-Simbólica) que imprime un Árbol de Trazabilidad paso a paso (XAI - Explainable AI) cada vez que toma una decisión.

## 1.3. Alcance Actual
El proyecto actual es un simulador completo de Onboarding y Compliance. Contiene generación de datos estadísticos masivos, evaluación en tiempo real de 11 módulos de riesgo, detección de Lavado de Activos con lógica difusa, cruce con listas de terrorismo internacional (OFAC) y 4 modelos predictivos de Machine Learning.