import random
import math

def generate_data():
    with open('hechos_base.pl', 'w') as f:
        f.write("% Archivo generado estadísticamente: hechos_base.pl\n")
        f.write("% Contiene predicados estructurados para el Sistema Experto Dual XAI\n\n")
        
        for i in range(1, 501):
            client_id = f"c_{i:03d}"
            
            # 1. ubicacion_ip
            # El 90% están en Perú, el resto simula conexiones externas.
            if random.random() < 0.90:
                country = 'peru'
            else:
                country = random.choice(['rusia', 'china', 'colombia', 'bolivia', 'espana'])
            
            # 2. intentos_login
            # Países de alto riesgo tienen más probabilidad de picos de intentos (fuerza bruta).
            if country in ['rusia', 'china']:
                login_attempts = random.randint(3, 5)
            else:
                login_attempts = random.choice([1, 1, 1, 1, 2, 2, 3, 4, 5])
            
            # 3. ingresos (soles, distribución normal trunca iterativa)
            ingresos = int(max(0, random.gauss(1800, 1000)))
            
            # 4. pago_servicios correlacionado a ingresos.
            # A mayores ingresos, mayor probabilidad de pago puntual.
            if ingresos > 2500:
                estado_pago = random.choice(['puntual', 'puntual', 'puntual', 'atrasado'])
            elif ingresos > 1200:
                estado_pago = random.choice(['puntual', 'atrasado', 'atrasado', 'moroso'])
            else:
                estado_pago = random.choice(['atrasado', 'moroso', 'moroso'])
            
            # 5. antiguedad_laboral (meses)
            # Fuerte correlación de que ingresos estables vienen de antiguedad alta.
            antiguedad = int(max(0, random.gauss(ingresos/100 + 6, 12)))
            
            # 6. billetera_digital
            nivel_billetera = random.choice(['alto', 'medio', 'bajo'])
            if estado_pago == 'moroso' and ingresos < 1000:
                nivel_billetera = random.choice(['medio', 'bajo', 'bajo'])
            elif country == 'peru' and ingresos > 0:
                nivel_billetera = random.choice(['alto', 'alto', 'medio', 'bajo'])
              
            # CASOS DE PRUEBA FORZADOS (para Task 3 del prompt)
            if i == 1: # c_001 -> Fraude puro (Seguridad)
                country = 'rusia'
                login_attempts = 5
            if i == 2: # c_002 -> Rechazo Scoring (Moroso, ingresos bajos)
                country = 'peru'
                login_attempts = 1
                ingresos = 800
                estado_pago = 'moroso'
                antiguedad = 2
                nivel_billetera = 'bajo'
            if i == 3: # c_003 -> Aprobacion Premium (Puntual, ingresos altos, mucha antiguedad)
                country = 'peru'
                login_attempts = 1
                ingresos = 5500
                estado_pago = 'puntual'
                antiguedad = 48
                nivel_billetera = 'alto'
            if i == 4: # c_004 -> Aprobacion Estandar con Fallback (Ingresos medios/bajos pero puntual y billetera alta)
                country = 'peru'
                login_attempts = 1
                ingresos = 900
                estado_pago = 'puntual'
                antiguedad = 12
                nivel_billetera = 'alto'
            if i == 5: # c_005 -> Evaluacion manual (Zona gris/incertidumbre)
                country = 'peru'
                login_attempts = 2
                ingresos = 1100
                estado_pago = 'atrasado'
                antiguedad = 6
                nivel_billetera = 'medio'

            # Guardar en base de conocimientos Prolog
            f.write(f"ubicacion_ip({client_id}, {country}).\n")
            f.write(f"intentos_login({client_id}, {login_attempts}).\n")
            f.write(f"ingresos({client_id}, {ingresos}).\n")
            f.write(f"pago_servicios({client_id}, {estado_pago}).\n")
            f.write(f"antiguedad_laboral({client_id}, {antiguedad}).\n")
            f.write(f"billetera_digital({client_id}, {nivel_billetera}).\n")
            f.write("\n")

if __name__ == '__main__':
    generate_data()
    print("Datos (3000 hechos) generados exitosamente en hechos_base.pl")
