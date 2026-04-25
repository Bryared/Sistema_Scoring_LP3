import random
import time
from datetime import datetime
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import IsolationForest
from sklearn.cluster import KMeans

def generate_data():
    lista_negra_imeis = [f"35{random.randint(1000000000000, 9999999999999)}" for _ in range(10)]
    current_ts = int(time.time())
    
    clientes_data = []
    transferencias_data = []
    
    print("Iniciando Fase 1: Generación de Datos Sintéticos...")
    for i in range(1, 501):
        client_id = f"c_{i:03d}"
        country = 'peru' if random.random() < 0.90 else random.choice(['rusia', 'china', 'colombia', 'bolivia', 'espana'])
        login_attempts = random.randint(3, 5) if country in ['rusia', 'china'] else random.choice([1, 1, 1, 1, 2, 2, 3, 4, 5])
        ingresos = int(max(0, random.gauss(1800, 1000)))
        
        if ingresos > 2500: estado_pago = random.choice(['puntual', 'puntual', 'puntual', 'atrasado'])
        elif ingresos > 1200: estado_pago = random.choice(['puntual', 'atrasado', 'atrasado', 'moroso'])
        else: estado_pago = random.choice(['atrasado', 'moroso', 'moroso'])
        
        antiguedad = int(max(0, random.gauss(ingresos/100 + 6, 12)))
        nivel_billetera = random.choice(['alto', 'medio', 'bajo'])
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
        
        dni_vencido = 'true' if random.random() < 0.03 else 'false'
        en_ofac = 'true' if random.random() < 0.01 else 'false'
        es_pep = 'true' if random.random() < 0.02 else 'false'
        
        # CASOS FORZADOS PARA DEMOSTRACIÓN
        if i == 1: # c_001 -> Fraude Bots / Anomalia
            tiempo_llenado = 2; ingresos = 15000; consultas_15dias = 15
        if i == 2: # c_002 -> Fraude IMEI
            imei_asignado = lista_negra_imeis[0]
        if i == 3: # c_003 -> Alto riesgo default (Joven impulsivo)
            ingresos = 3000; suma_cuotas = 1500; antiguedad = 2; antiguedad_domicilio = 6
        if i == 4: # c_004 -> Ruletero
            creditos_activos = 6; consultas_15dias = 8
        if i == 5: # c_005 -> Premium (Familia estable)
            ingresos = 6000; estado_pago = 'puntual'; suma_cuotas = 1000; antiguedad_domicilio = 48; sector = 'tecnologia'
        if i == 6: # c_006 -> Insolvencia
            patrimonio = 10000; deuda_total = 35000; tipo_patrimonio = 'inmobiliario'
        if i == 7: # c_007 -> AML
            pass # Transferencias añadidas luego
        if i == 8: # c_008 -> Cobro Indebido
            tasa_acordada = 0.10; tasa_cobrada = 0.15
        if i == 9: # c_009 -> VPN
            country = 'eeuu'; residencia = 'peru'; justificacion_vpn = 'true'
        if i == 11: # c_011 -> OFAC
            en_ofac = 'true'
        if i == 12: # c_012 -> PEP
            es_pep = 'true'
            
        clientes_data.append({
            'id': client_id,
            'country': country, 'login_attempts': login_attempts, 'ingresos': ingresos,
            'estado_pago': estado_pago, 'antiguedad': antiguedad, 'nivel_billetera': nivel_billetera,
            'patrimonio': patrimonio, 'deuda_total': deuda_total, 'tasa_acordada': tasa_acordada,
            'tasa_cobrada': tasa_cobrada, 'tiempo_llenado': tiempo_llenado, 'residencia': residencia,
            'justificacion_vpn': justificacion_vpn, 'imei_asignado': imei_asignado, 'suma_cuotas': suma_cuotas,
            'antiguedad_domicilio': antiguedad_domicilio, 'sector': sector, 'creditos_activos': creditos_activos,
            'consultas_15dias': consultas_15dias, 'tipo_patrimonio': tipo_patrimonio,
            'dni_vencido': dni_vencido, 'en_ofac': en_ofac, 'es_pep': es_pep
        })
        
        # Transferencias (con conceptos NLP)
        conceptos_normales = ["pago luz", "alquiler", "cena", "transferencia familiar", "ahorros"]
        conceptos_sospechosos = ["pago favores", "donativo x", "inversion rapida", "xyz", "sin concepto"]
        
        num_transferencias = random.randint(0, 2)
        for _ in range(num_transferencias):
            dest = f"c_{random.randint(1, 500):03d}"
            if dest != client_id:
                monto = int(random.uniform(100, 2000))
                dias_atras = random.randint(1, 30)
                ts = current_ts - (dias_atras * 86400)
                is_suspicious = random.random() < 0.05
                concepto = random.choice(conceptos_sospechosos) if is_suspicious else random.choice(conceptos_normales)
                
                transferencias_data.append({
                    'origen': client_id, 'destino': dest, 'monto': monto,
                    'ts': ts, 'fecha': datetime.fromtimestamp(ts).strftime('%Y-%m-%d'),
                    'concepto': concepto
                })
                
    # Agregar transferencias forzadas
    # c_007 -> Smurfing rápido (Con NLP Sospechoso)
    ts_007_1 = current_ts - 86400 * 3
    transferencias_data.append({'origen':'c_007', 'destino':'c_400', 'monto':15000, 'ts':ts_007_1, 'fecha':'2026-04-20', 'concepto':'inversion xyz'})
    transferencias_data.append({'origen':'c_400', 'destino':'c_401', 'monto':14000, 'ts':ts_007_1 + 86400*1, 'fecha':'2026-04-21', 'concepto':'pago favores'})
    transferencias_data.append({'origen':'c_401', 'destino':'c_007', 'monto':13500, 'ts':ts_007_1 + 86400*2, 'fecha':'2026-04-22', 'concepto':'retorno'})

    # c_010 -> Smurfing lento (Falso Positivo)
    ts_010_1 = current_ts - 86400 * 180
    transferencias_data.append({'origen':'c_010', 'destino':'c_400', 'monto':20000, 'ts':ts_010_1, 'fecha':'2025-10-20', 'concepto':'alquiler'})
    transferencias_data.append({'origen':'c_400', 'destino':'c_401', 'monto':19000, 'ts':ts_010_1 + 86400*90, 'fecha':'2026-01-20', 'concepto':'ahorros'})
    transferencias_data.append({'origen':'c_401', 'destino':'c_010', 'monto':18000, 'ts':ts_010_1 + 86400*180, 'fecha':'2026-04-20', 'concepto':'pago'})

    print("Iniciando Fase 2: Entrenamiento Machine Learning (Nivel 2 Neuro-Simbólico)...")
    
    # Preprocesamiento para ML
    X_scoring = []
    X_anomaly = []
    X_clustering = []
    y_default_simulado = []
    
    for c in clientes_data:
        # Features: [Ingresos, Cuotas, Consultas, Antiguedad_Lab, Antiguedad_Dom]
        features = [c['ingresos'], c['suma_cuotas'], c['consultas_15dias'], c['antiguedad'], c['antiguedad_domicilio']]
        X_scoring.append(features)
        
        # Anomaly Features: [Tiempo llenado, Intentos Login, Consultas]
        X_anomaly.append([c['tiempo_llenado'], c['login_attempts'], c['consultas_15dias']])
        
        # Clustering: [Ingresos, Deuda Total, Antiguedad Domicilio]
        X_clustering.append([c['ingresos'], c['deuda_total'], c['antiguedad_domicilio']])
        
        # Target simulado para entrenamiento (Default = moroso o DSR muy alto)
        is_default = 1 if c['estado_pago'] == 'moroso' or (c['suma_cuotas']/max(1,c['ingresos']) > 0.4) else 0
        y_default_simulado.append(is_default)
        
    X_scoring = np.array(X_scoring)
    X_anomaly = np.array(X_anomaly)
    X_clustering = np.array(X_clustering)
    y_default_simulado = np.array(y_default_simulado)
    
    # --- MODELO 1: REGRESIÓN LOGÍSTICA (CREDIT SCORING) ---
    print(" Entrenando Modelo Predictivo de Default...")
    clf = LogisticRegression(max_iter=1000)
    clf.fit(X_scoring, y_default_simulado)
    probs_default = clf.predict_proba(X_scoring)[:, 1]
    
    # --- MODELO 2: ISOLATION FOREST (ANOMALÍAS FRAUDE) ---
    print(" Entrenando Isolation Forest para Anomalías...")
    iso = IsolationForest(contamination=0.05, random_state=42)
    iso.fit(X_anomaly)
    anomalias = iso.predict(X_anomaly) # -1 es anomalia, 1 es normal
    
    # --- MODELO 3: K-MEANS (CLUSTERING DEMOGRÁFICO) ---
    print(" Entrenando K-Means Clustering...")
    kmeans = KMeans(n_clusters=3, random_state=42)
    clusters = kmeans.fit_predict(X_clustering)
    cluster_names = {0: "joven_riesgoso", 1: "familia_estable", 2: "emprendedor_promedio"}
    
    # --- MODELO 4: SIMULACIÓN NLP (PALABRAS SOSPECHOSAS EN TRANSFERENCIAS) ---
    print(" Ejecutando NLP en Descripciones de Transferencias...")
    palabras_peligro = ["favores", "xyz", "inversion rapida", "testaferro"]
    
    print("Iniciando Fase 3: Escritura de Base de Conocimientos Prolog...")
    with open('hechos_base.pl', 'w') as f:
        f.write("% Archivo generado con IA NEURO-SIMBÓLICA: hechos_base.pl\n\n")
        predicados = [
            "ubicacion_ip/2", "intentos_login/2", "ingresos/2", "pago_servicios/2",
            "antiguedad_laboral/2", "billetera_digital/2", "patrimonio/2", "deuda_total/2",
            "tasa_acordada/2", "tasa_cobrada/2", "transferencia/6",
            "tiempo_llenado/2", "residencia/2", "justificacion_vpn/2",
            "dispositivo_imei/2", "imei_en_lista_negra/1", "suma_cuotas_mensuales/2",
            "antiguedad_domicilio/2", "sector_laboral/2", "creditos_activos/2",
            "consultas_bancarias_15dias/2", "tipo_patrimonio/2",
            "dni_vencido/2", "en_lista_ofac/2", "es_pep/2",
            "ml_probabilidad_default/2", "ml_fraude_anomalia/2", "ml_perfil_cluster/2",
            "ml_texto_sospechoso/3"
        ]
        for p in predicados:
            f.write(f":- discontiguous {p}.\n")
        f.write("\n")
        
        for imei in lista_negra_imeis:
            f.write(f"imei_en_lista_negra('{imei}').\n")
        f.write("\n")
        
        # Inyectar variables tradicionales y Predicciones ML
        for idx, c in enumerate(clientes_data):
            client_id = c['id']
            f.write(f"ubicacion_ip({client_id}, {c['country']}).\n")
            f.write(f"intentos_login({client_id}, {c['login_attempts']}).\n")
            f.write(f"ingresos({client_id}, {c['ingresos']}).\n")
            f.write(f"pago_servicios({client_id}, {c['estado_pago']}).\n")
            f.write(f"antiguedad_laboral({client_id}, {c['antiguedad']}).\n")
            f.write(f"billetera_digital({client_id}, {c['nivel_billetera']}).\n")
            f.write(f"patrimonio({client_id}, {c['patrimonio']}).\n")
            f.write(f"deuda_total({client_id}, {c['deuda_total']}).\n")
            f.write(f"tasa_acordada({client_id}, {c['tasa_acordada']}).\n")
            f.write(f"tasa_cobrada({client_id}, {c['tasa_cobrada']}).\n")
            f.write(f"tiempo_llenado({client_id}, {c['tiempo_llenado']}).\n")
            f.write(f"residencia({client_id}, {c['residencia']}).\n")
            f.write(f"justificacion_vpn({client_id}, {c['justificacion_vpn']}).\n")
            f.write(f"dispositivo_imei({client_id}, '{c['imei_asignado']}').\n")
            f.write(f"suma_cuotas_mensuales({client_id}, {c['suma_cuotas']}).\n")
            f.write(f"antiguedad_domicilio({client_id}, {c['antiguedad_domicilio']}).\n")
            f.write(f"sector_laboral({client_id}, {c['sector']}).\n")
            f.write(f"creditos_activos({client_id}, {c['creditos_activos']}).\n")
            f.write(f"consultas_bancarias_15dias({client_id}, {c['consultas_15dias']}).\n")
            f.write(f"tipo_patrimonio({client_id}, {c['tipo_patrimonio']}).\n")
            f.write(f"dni_vencido({client_id}, {c['dni_vencido']}).\n")
            f.write(f"en_lista_ofac({client_id}, {c['en_ofac']}).\n")
            f.write(f"es_pep({client_id}, {c['es_pep']}).\n")
            
            # --- INYECCIÓN DE MACHINE LEARNING EN PROLOG ---
            prob = round(probs_default[idx], 4)
            is_anomaly = 'true' if anomalias[idx] == -1 else 'false'
            cluster_asignado = cluster_names[clusters[idx]]
            
            # Fuerza c_001 como anomalía (Isolation Forest)
            if client_id == 'c_001': is_anomaly = 'true'
            if client_id == 'c_003': prob = 0.95; cluster_asignado = 'joven_riesgoso'
            if client_id == 'c_005': prob = 0.05; cluster_asignado = 'familia_estable'
            
            f.write(f"ml_probabilidad_default({client_id}, {prob}).\n")
            f.write(f"ml_fraude_anomalia({client_id}, {is_anomaly}).\n")
            f.write(f"ml_perfil_cluster({client_id}, {cluster_asignado}).\n\n")

        # Inyectar transferencias y resultados NLP
        for t in transferencias_data:
            f.write(f"transferencia({t['origen']}, {t['destino']}, {t['monto']}, {t['ts']}, '{t['fecha']}', '{t['concepto']}').\n")
            
            es_sospechoso = 'false'
            if any(palabra in t['concepto'].lower() for palabra in palabras_peligro):
                es_sospechoso = 'true'
            
            f.write(f"ml_texto_sospechoso({t['origen']}, {t['destino']}, {es_sospechoso}).\n")
            
    print("¡Generación completada! El motor Simbólico (Prolog) ahora cuenta con predicciones Neuronales (ML).")

if __name__ == '__main__':
    generate_data()
