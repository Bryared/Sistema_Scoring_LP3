# 4. Arquitectura Técnica

1. **Base de Datos (Python - generar_datos.py):** Crea 500 clientes, métricas de interacción, listas OFAC/PEP y transferencias con Timestamps.
2. **Cerebro Lógico (Prolog - motor_inferencia.pl):** Embudo de reglas estrictas y lógicas matemáticas para evaluar clientes en milisegundos.
3. **Dashboard (Streamlit - app.py):** Interfaz gráfica que dibuja redes con NetworkX, genera logs con Hashlib y conecta al usuario con Prolog mediante PySwip.