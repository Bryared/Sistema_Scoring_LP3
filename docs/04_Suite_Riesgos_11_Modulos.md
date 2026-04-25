# Capítulo 5: La Suite de los 11 Módulos de Riesgo

El núcleo de Prolog está segmentado en tres grandes escudos o líneas de defensa. 

## Capa 1: Ciberseguridad Antifraude (Rechazo Temprano)
1. **Velocidad Anti-Bots:** Mide los milisegundos. Si un formulario se llena en 2 segundos, es un script. Rechazo crítico.
2. **Identidad Vencida (KYC):** Cruza la base de Reniec. DNI caducado es fraude documental.
3. **Fuerza Bruta:** Más de 3 intentos fallidos de login denotan un posible ataque hacker.
4. **Geolocalización IP:** Si el cliente reside en Perú pero su IP es de Rusia, se rechaza salvo que declare VPN laboral.
5. **Lista Negra IMEI:** Cruza con OSIPTEL para bloquear celulares robados.
6. **Cumplimiento OFAC y PEP:** Cruce con bases internacionales. Terroristas (OFAC) son bloqueados; Políticos (PEP) son derivados a humanos.

## Capa 2: Evaluación del Riesgo Crediticio (Scoring)
7. **Carga Financiera DSR:** Si el cliente destina más del 35% de su sueldo a pagar deudas, está al borde de la quiebra. Rechazado.
8. **Ruleteo Financiero:** Si tiene más de 3 tarjetas de crédito activas y las usa de manera rotativa, representa alto riesgo.
9. **Huella de Desesperación:** Si el sistema nota que el cliente tuvo más de 5 consultas en burós de crédito en 15 días, significa que fue rechazado por otros bancos recientemente.

## Capa 3: Monitoreo Legal, Auditoría y AML
10. **AML Difuso Temporal:** Detecta el *Smurfing*. Para ser lavado, el dinero debe triangular `A->B->C->A`. Pero Prolog es inteligente: exige que ocurra en menos de 72 horas y usa lógica difusa para tolerar que el dinero no regrese al 100% (porque los lavadores pagan comisiones a las mulas).
11. **Insolvencia Patrimonial Diferenciada:** Cumplimiento SBS. La deuda no puede superar 3 veces el patrimonio si este es inmobiliario (difícil de embargar), pero puede ser hasta 5 veces si es patrimonio líquido (efectivo en bancos).
12. **Auditoría de Contratos:** Un Smart Contract lógico verifica que las operaciones de cobro central (Tasa Cobrada) respeten el PDF que firmó el usuario (Tasa Acordada).