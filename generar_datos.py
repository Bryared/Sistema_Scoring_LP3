import random
import math
from datetime import datetime, timedelta

def generate_data():
    with open('hechos_base.pl', 'w') as f:
        f.write("% Archivo generado estadísticamente: hechos_base.pl\n")
        f.write("% Contiene predicados estructurados para el Sistema Experto Dual XAI (11 Modulos)\n\n")
        
        # Declaraciones discontiguous para evitar warnings en Prolog
        predicados = [
            "ubicacion_ip/2", "intentos_login/2", "ingresos/2", "pago_servicios/2",
            "antiguedad_laboral/2", "billetera_digital/2", "patrimonio/2", "deuda_total/2",
            "tasa_acordada/2", "tasa_cobrada/2", "transferencia/4",
            "tiempo_llenado/2", "residencia/2", "justificacion_vpn/2",
            "dispositivo_imei/2", "imei_en_lista_negra/1", "suma_cuotas_mensuales/2",
            "antiguedad_domicilio/2", "sector_laboral/2", "creditos_activos/2",
            "consultas_bancarias_15dias/2", "tipo_patrimonio/2"
        ]
        for p in predicados:
            f.write(f":- discontiguous {p}.\n")
        f.write("\n")
        
        # Generar lista negra de IMEIs
        lista_negra_imeis = [f"35{random.randint(1000000000000, 9999999999999)}" for _ in range(10)]
        f.write("% --- LISTA NEGRA DE IMEIs DE OSIPTEL ---\n")
        for imei in lista_negra_imeis:
            f.write(f"imei_en_lista_negra('{imei}').\n")
        f.write("\n")
        
        clientes = [f"c_{i:03d}" for i in range(1, 501)]
        
        for i in range(1, 501):
            client_id = f"c_{i:03d}"
            
            # --- DATOS BÁSICOS (Onboarding Inicial) ---
            country = 'peru' if random.random() < 0.90 else random.choice(['rusia', 'china', 'colombia', 'bolivia', 'espana'])
            login_attempts = random.randint(3, 5) if country in ['rusia', 'china'] else random.choice([1, 1, 1, 1, 2, 2, 3, 4, 5])
            ingresos = int(max(0, random.gauss(1800, 1000)))
            
            if ingresos > 2500: estado_pago = random.choice(['puntual', 'puntual', 'puntual', 'atrasado'])
            elif ingresos > 1200: estado_pago = random.choice(['puntual', 'atrasado', 'atrasado', 'moroso'])
            else: estado_pago = random.choice(['atrasado', 'moroso', 'moroso'])
            
            antiguedad = int(max(0, random.gauss(ingresos/100 + 6, 12)))
            nivel_billetera = random.choice(['alto', 'medio', 'bajo'])
            if estado_pago == 'moroso' and ingresos < 1000: nivel_billetera = random.choice(['medio', 'bajo', 'bajo'])
            elif country == 'peru' and ingresos > 0: nivel_billetera = random.choice(['alto', 'alto', 'medio', 'bajo'])
                
            # --- DATOS COMPLIANCE & AUDITORÍA ---
            patrimonio = int(max(100, random.gauss(ingresos * 5, 2000)))
            deuda_total = int(max(0, random.gauss(patrimonio * 0.5, patrimonio)))
            tasa_acordada = round(random.uniform(0.05, 0.25), 2)
            tasa_cobrada = tasa_acordada if random.random() < 0.95 else round(tasa_acordada + random.uniform(0.01, 0.05), 2)
            
            # --- NUEVOS DATOS: 11 MÓDULOS DE RIESGO ---
            # 1. DSR (Carga Financiera)
            # En promedio la gente tiene 25% de carga, pero algunos están muy sobreendeudados
            carga_porcentaje = random.gauss(0.25, 0.15)
            suma_cuotas = int(max(0, ingresos * carga_porcentaje))
            
            # 2. Anti-Bots
            # Bots lo hacen muy rápido (< 10s)
            tiempo_llenado = random.randint(1, 9) if random.random() < 0.02 else random.randint(15, 120)
            
            # 3. IP vs Residencia
            residencia = 'peru' if random.random() < 0.95 else random.choice(['colombia', 'chile', 'eeuu'])
            justificacion_vpn = 'true' if random.random() < 0.1 else 'false'
            
            # 4. Lista Negra IMEI
            is_blacklisted = random.random() < 0.02
            imei_asignado = random.choice(lista_negra_imeis) if is_blacklisted else f"35{random.randint(1000000000000, 9999999999999)}"
            
            # 5. Estabilidad Domiciliaria
            antiguedad_domicilio = random.randint(0, 120) # Meses
            
            # 6. Sector Laboral
            sector = random.choice(['tecnologia', 'salud', 'educacion', 'comercio', 'turismo', 'construccion'])
            
            # 7 & 8. Ruleteo y Desesperación
            creditos_activos = random.randint(0, 5)
            consultas_15dias = random.randint(0, 7)
            
            # 9. Tipo de Patrimonio (Insolvencia Diferenciada)
            tipo_patrimonio = random.choice(['liquido', 'inmobiliario'])
            
            # CASOS DE PRUEBA FORZADOS
            if i == 1: # c_001 -> Fraude IP y Bots (IP Rusia, Residence Peru, no justificado, 2s llenado)
                country = 'rusia'; residencia = 'peru'; justificacion_vpn = 'false'; tiempo_llenado = 2
            if i == 2: # c_002 -> Fraude IMEI (en lista negra)
                imei_asignado = lista_negra_imeis[0]
            if i == 3: # c_003 -> Sobreendeudado (DSR > 35%)
                ingresos = 3000; suma_cuotas = 1500 # 50%
            if i == 4: # c_004 -> Ruletero / Desesperación
                creditos_activos = 6; consultas_15dias = 8
            if i == 5: # c_005 -> Aprobado Premium (Estabilidad > 24m, Sector Tech)
                ingresos = 6000; estado_pago = 'puntual'; suma_cuotas = 1000; tiempo_llenado = 45; antiguedad_domicilio = 36; sector = 'tecnologia'
            if i == 6: # c_006 -> Insolvencia SBS Inmobiliaria vs Liquido
                patrimonio = 10000; deuda_total = 35000; tipo_patrimonio = 'inmobiliario' # 3.5x, Rechazado si Inmobiliario. Aprobado si Liquido.
            if i == 8: # c_008 -> Cobro Indebido
                tasa_acordada = 0.10; tasa_cobrada = 0.15
            if i == 9: # c_009 -> VPN Justificada (Aprobado)
                country = 'eeuu'; residencia = 'peru'; justificacion_vpn = 'true'
                
            # Escritura de variables
            f.write(f"ubicacion_ip({client_id}, {country}).\n")
            f.write(f"intentos_login({client_id}, {login_attempts}).\n")
            f.write(f"ingresos({client_id}, {ingresos}).\n")
            f.write(f"pago_servicios({client_id}, {estado_pago}).\n")
            f.write(f"antiguedad_laboral({client_id}, {antiguedad}).\n")
            f.write(f"billetera_digital({client_id}, {nivel_billetera}).\n")
            f.write(f"patrimonio({client_id}, {patrimonio}).\n")
            f.write(f"deuda_total({client_id}, {deuda_total}).\n")
            f.write(f"tasa_acordada({client_id}, {tasa_acordada}).\n")
            f.write(f"tasa_cobrada({client_id}, {tasa_cobrada}).\n")
            
            f.write(f"tiempo_llenado({client_id}, {tiempo_llenado}).\n")
            f.write(f"residencia({client_id}, {residencia}).\n")
            f.write(f"justificacion_vpn({client_id}, {justificacion_vpn}).\n")
            f.write(f"dispositivo_imei({client_id}, '{imei_asignado}').\n")
            f.write(f"suma_cuotas_mensuales({client_id}, {suma_cuotas}).\n")
            f.write(f"antiguedad_domicilio({client_id}, {antiguedad_domicilio}).\n")
            f.write(f"sector_laboral({client_id}, {sector}).\n")
            f.write(f"creditos_activos({client_id}, {creditos_activos}).\n")
            f.write(f"consultas_bancarias_15dias({client_id}, {consultas_15dias}).\n")
            f.write(f"tipo_patrimonio({client_id}, {tipo_patrimonio}).\n")
            
            # Noise transfers
            num_transferencias = random.randint(0, 2)
            for _ in range(num_transferencias):
                dest = random.choice(clientes)
                if dest != client_id:
                    monto = int(random.uniform(100, 2000))
                    fecha_str = f"'{datetime.now().strftime('%Y-%m-%d')}'"
                    f.write(f"transferencia({client_id}, {dest}, {monto}, {fecha_str}).\n")
            f.write("\n")
            
        # Caso c_007: Triangulación AML con MERMA (Comisión)
        f.write("% --- CASO DE PRUEBA AML (c_007) ---\n")
        f.write("% c_007 envia 15000 a c_400. c_400 envia 14000 a c_401 (comisión de mula).\n")
        f.write("% c_401 regresa 13500 a c_007 (comisión). Total regresa 90% (13500/15000).\n")
        f.write("transferencia(c_007, c_400, 15000, '2026-04-20').\n")
        f.write("transferencia(c_400, c_401, 14000, '2026-04-21').\n")
        f.write("transferencia(c_401, c_007, 13500, '2026-04-22').\n")

if __name__ == '__main__':
    generate_data()
    print("Base de conocimientos completa (11 modulos) generada exitosamente en hechos_base.pl")
