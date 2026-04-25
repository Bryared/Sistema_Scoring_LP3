import random
import math
import time
from datetime import datetime, timedelta

def generate_data():
    with open('hechos_base.pl', 'w') as f:
        f.write("% Archivo generado estadísticamente: hechos_base.pl\n")
        f.write("% Contiene predicados estructurados para el Sistema Experto Dual XAI (Blindaje Nivel 1)\n\n")
        
        # Declaraciones discontiguous para evitar warnings en Prolog
        predicados = [
            "ubicacion_ip/2", "intentos_login/2", "ingresos/2", "pago_servicios/2",
            "antiguedad_laboral/2", "billetera_digital/2", "patrimonio/2", "deuda_total/2",
            "tasa_acordada/2", "tasa_cobrada/2", "transferencia/5",
            "tiempo_llenado/2", "residencia/2", "justificacion_vpn/2",
            "dispositivo_imei/2", "imei_en_lista_negra/1", "suma_cuotas_mensuales/2",
            "antiguedad_domicilio/2", "sector_laboral/2", "creditos_activos/2",
            "consultas_bancarias_15dias/2", "tipo_patrimonio/2",
            "dni_vencido/2", "en_lista_ofac/2", "es_pep/2"
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
        
        # Timestamp base actual
        current_ts = int(time.time())
        
        for i in range(1, 501):
            client_id = f"c_{i:03d}"
            
            # --- DATOS BÁSICOS ---
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
                
            patrimonio = int(max(100, random.gauss(ingresos * 5, 2000)))
            deuda_total = int(max(0, random.gauss(patrimonio * 0.5, patrimonio)))
            tasa_acordada = round(random.uniform(0.05, 0.25), 2)
            tasa_cobrada = tasa_acordada if random.random() < 0.95 else round(tasa_acordada + random.uniform(0.01, 0.05), 2)
            
            carga_porcentaje = random.gauss(0.25, 0.15)
            suma_cuotas = int(max(0, ingresos * carga_porcentaje))
            
            tiempo_llenado = random.randint(1, 9) if random.random() < 0.02 else random.randint(15, 120)
            residencia = 'peru' if random.random() < 0.95 else random.choice(['colombia', 'chile', 'eeuu'])
            justificacion_vpn = 'true' if random.random() < 0.1 else 'false'
            
            is_blacklisted = random.random() < 0.02
            imei_asignado = random.choice(lista_negra_imeis) if is_blacklisted else f"35{random.randint(1000000000000, 9999999999999)}"
            
            antiguedad_domicilio = random.randint(0, 120)
            sector = random.choice(['tecnologia', 'salud', 'educacion', 'comercio', 'turismo', 'construccion'])
            
            creditos_activos = random.randint(0, 5)
            consultas_15dias = random.randint(0, 7)
            tipo_patrimonio = random.choice(['liquido', 'inmobiliario'])
            
            # NUEVOS DATOS (KYC y Compliance)
            dni_vencido = 'true' if random.random() < 0.03 else 'false'
            en_ofac = 'true' if random.random() < 0.01 else 'false'
            es_pep = 'true' if random.random() < 0.02 else 'false'
            
            # CASOS DE PRUEBA FORZADOS
            if i == 1: # c_001 -> Fraude Bots
                tiempo_llenado = 2
            if i == 2: # c_002 -> Fraude IMEI (en lista negra)
                imei_asignado = lista_negra_imeis[0]
            if i == 3: # c_003 -> Sobreendeudado (DSR > 35%)
                ingresos = 3000; suma_cuotas = 1500 # 50%
            if i == 4: # c_004 -> Ruletero / Desesperación
                creditos_activos = 6; consultas_15dias = 8
            if i == 5: # c_005 -> Aprobado Premium (Estabilidad > 24m, Sector Tech)
                ingresos = 6000; estado_pago = 'puntual'; suma_cuotas = 1000; tiempo_llenado = 45; antiguedad_domicilio = 36; sector = 'tecnologia'; en_ofac = 'false'; dni_vencido = 'false'; es_pep = 'false'
            if i == 6: # c_006 -> Insolvencia SBS Inmobiliaria vs Liquido
                patrimonio = 10000; deuda_total = 35000; tipo_patrimonio = 'inmobiliario' # 3.5x
            if i == 8: # c_008 -> Cobro Indebido
                tasa_acordada = 0.10; tasa_cobrada = 0.15
            if i == 9: # c_009 -> VPN Justificada (Aprobado)
                country = 'eeuu'; residencia = 'peru'; justificacion_vpn = 'true'
            if i == 11: # c_011 -> Lista OFAC
                en_ofac = 'true'
            if i == 12: # c_012 -> PEP (Evaluación Manual)
                es_pep = 'true'; en_ofac = 'false'; dni_vencido = 'false'
                
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
            
            f.write(f"dni_vencido({client_id}, {dni_vencido}).\n")
            f.write(f"en_lista_ofac({client_id}, {en_ofac}).\n")
            f.write(f"es_pep({client_id}, {es_pep}).\n")
            
            # Noise transfers
            num_transferencias = random.randint(0, 2)
            for _ in range(num_transferencias):
                dest = random.choice(clientes)
                if dest != client_id:
                    monto = int(random.uniform(100, 2000))
                    dias_atras = random.randint(1, 30)
                    ts = current_ts - (dias_atras * 86400)
                    dt = datetime.fromtimestamp(ts)
                    fecha_str = f"'{dt.strftime('%Y-%m-%d')}'"
                    f.write(f"transferencia({client_id}, {dest}, {monto}, {ts}, {fecha_str}).\n")
            f.write("\n")
            
        # Caso c_007: Triangulación AML con MERMA (Comisión) - RÁPIDA (Smurfing Real)
        f.write("% --- CASO DE PRUEBA AML (c_007) : SMURFING RAPIDO (48 HORAS) ---\n")
        ts_007_1 = current_ts - 86400 * 3 # Hace 3 dias
        ts_007_2 = ts_007_1 + 86400 * 1   # 1 dia despues
        ts_007_3 = ts_007_1 + 86400 * 2   # 2 dias despues (dentro de las 72h)
        f.write(f"transferencia(c_007, c_400, 15000, {ts_007_1}, '2026-04-20').\n")
        f.write(f"transferencia(c_400, c_401, 14000, {ts_007_2}, '2026-04-21').\n")
        f.write(f"transferencia(c_401, c_007, 13500, {ts_007_3}, '2026-04-22').\n")
        f.write("\n")
        
        # Caso c_010: Falso Positivo Temporal - DEMORA 6 MESES (No es lavado rápido)
        f.write("% --- CASO DE PRUEBA AML (c_010) : FALSO POSITIVO (6 MESES DE ESPERA) ---\n")
        ts_010_1 = current_ts - 86400 * 180 # Hace 6 meses
        ts_010_2 = ts_010_1 + 86400 * 90    # 3 meses despues
        ts_010_3 = ts_010_1 + 86400 * 180   # 6 meses despues (> 72 horas)
        f.write(f"transferencia(c_010, c_400, 20000, {ts_010_1}, '2025-10-20').\n")
        f.write(f"transferencia(c_400, c_401, 19000, {ts_010_2}, '2026-01-20').\n")
        f.write(f"transferencia(c_401, c_010, 18000, {ts_010_3}, '2026-04-20').\n")

if __name__ == '__main__':
    generate_data()
    print("Base de conocimientos completa (Blindaje OFAC, PEP, Timestamps) generada exitosamente en hechos_base.pl")
