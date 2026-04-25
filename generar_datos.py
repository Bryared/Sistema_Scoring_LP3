import random
import math
from datetime import datetime, timedelta

def generate_data():
    with open('hechos_base.pl', 'w') as f:
        f.write("% Archivo generado estadísticamente: hechos_base.pl\n")
        f.write("% Contiene predicados estructurados para el Sistema Experto Dual XAI\n\n")
        f.write(":- discontiguous ubicacion_ip/2.\n")
        f.write(":- discontiguous intentos_login/2.\n")
        f.write(":- discontiguous ingresos/2.\n")
        f.write(":- discontiguous pago_servicios/2.\n")
        f.write(":- discontiguous antiguedad_laboral/2.\n")
        f.write(":- discontiguous billetera_digital/2.\n")
        f.write(":- discontiguous patrimonio/2.\n")
        f.write(":- discontiguous deuda_total/2.\n")
        f.write(":- discontiguous tasa_acordada/2.\n")
        f.write(":- discontiguous tasa_cobrada/2.\n")
        f.write(":- discontiguous transferencia/4.\n\n")
        
        # Pre-generate clients to handle transfers properly
        clientes = [f"c_{i:03d}" for i in range(1, 501)]
        
        for i in range(1, 501):
            client_id = f"c_{i:03d}"
            
            # --- DATOS ORIGINALES ---
            if random.random() < 0.90:
                country = 'peru'
            else:
                country = random.choice(['rusia', 'china', 'colombia', 'bolivia', 'espana'])
            
            if country in ['rusia', 'china']:
                login_attempts = random.randint(3, 5)
            else:
                login_attempts = random.choice([1, 1, 1, 1, 2, 2, 3, 4, 5])
            
            ingresos = int(max(0, random.gauss(1800, 1000)))
            
            if ingresos > 2500:
                estado_pago = random.choice(['puntual', 'puntual', 'puntual', 'atrasado'])
            elif ingresos > 1200:
                estado_pago = random.choice(['puntual', 'atrasado', 'atrasado', 'moroso'])
            else:
                estado_pago = random.choice(['atrasado', 'moroso', 'moroso'])
            
            antiguedad = int(max(0, random.gauss(ingresos/100 + 6, 12)))
            
            nivel_billetera = random.choice(['alto', 'medio', 'bajo'])
            if estado_pago == 'moroso' and ingresos < 1000:
                nivel_billetera = random.choice(['medio', 'bajo', 'bajo'])
            elif country == 'peru' and ingresos > 0:
                nivel_billetera = random.choice(['alto', 'alto', 'medio', 'bajo'])
                
            # --- NUEVOS DATOS (Compliance y Auditoría) ---
            # Patrimonio y Deuda (Insolvencia si Deuda > Patrimonio * 3)
            patrimonio = int(max(100, random.gauss(ingresos * 5, 2000)))
            # Mayormente, la deuda es aceptable, pero habrá outliers (riesgo default)
            deuda_total = int(max(0, random.gauss(patrimonio * 0.5, patrimonio)))
            
            # Tasas (Cobros indebidos si tasa_cobrada > tasa_acordada)
            tasa_acordada = round(random.uniform(0.05, 0.25), 2)
            # En la mayoría de casos es igual, algunos pocos sistemas fallan y cobran de más
            tasa_cobrada = tasa_acordada if random.random() < 0.95 else round(tasa_acordada + random.uniform(0.01, 0.05), 2)
            
            # --- NOISE DATA FOR TRANSFERS ---
            # Cada usuario puede o no hacer transferencias genéricas (ruido blanco para AML)
            num_transferencias = random.randint(0, 2)
            for _ in range(num_transferencias):
                dest = random.choice(clientes)
                if dest != client_id:
                    monto = int(random.uniform(100, 2000))
                    fecha_str = f"'{datetime.now().strftime('%Y-%m-%d')}'"
                    f.write(f"transferencia({client_id}, {dest}, {monto}, {fecha_str}).\n")
              
            # CASOS DE PRUEBA FORZADOS
            if i == 1: # c_001 -> Fraude puro (Seguridad)
                country = 'rusia'
                login_attempts = 5
            if i == 2: # c_002 -> Rechazo Scoring (Moroso, ingresos bajos)
                country = 'peru'; login_attempts = 1; ingresos = 800; estado_pago = 'moroso'; antiguedad = 2; nivel_billetera = 'bajo'
            if i == 3: # c_003 -> Aprobacion Premium
                country = 'peru'; login_attempts = 1; ingresos = 5500; estado_pago = 'puntual'; antiguedad = 48; nivel_billetera = 'alto'
            if i == 4: # c_004 -> Aprobacion Estandar con Fallback
                country = 'peru'; login_attempts = 1; ingresos = 900; estado_pago = 'puntual'; antiguedad = 12; nivel_billetera = 'alto'
            if i == 5: # c_005 -> Evaluacion manual
                country = 'peru'; login_attempts = 2; ingresos = 1100; estado_pago = 'atrasado'; antiguedad = 6; nivel_billetera = 'medio'
            if i == 6: # c_006 -> Insolvencia SBS (Deuda muy superior a patrimonio)
                patrimonio = 10000; deuda_total = 35000 # 3.5x
            if i == 8: # c_008 -> Cobro Indebido
                tasa_acordada = 0.10
                tasa_cobrada = 0.15 # Discrepancia del 5%
                
            # Guardar en base de conocimientos Prolog
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
            f.write("\n")
            
        # Inyectar el caso de prueba c_007 de Triangulación fuera del loop (A -> B -> C -> A)
        f.write("% --- CASO DE PRUEBA AML (c_007) ---\n")
        f.write("% c_007 enviara a c_400, c_400 a c_401, y c_401 regresa a c_007 (Monto > 10000)\n")
        f.write("transferencia(c_007, c_400, 15000, '2026-04-20').\n")
        f.write("transferencia(c_400, c_401, 15000, '2026-04-21').\n")
        f.write("transferencia(c_401, c_007, 15000, '2026-04-22').\n")

if __name__ == '__main__':
    generate_data()
    print("Nuevos datos Neuro-Simbólicos (AML, Compliance, Auditorías) generados en hechos_base.pl")
