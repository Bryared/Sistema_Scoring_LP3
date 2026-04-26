import numpy as np
import pandas as pd
from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import StandardScaler

class CalculadorScoringNeuronal:
    """
    Esta clase implementa una Red Neuronal Multicapa (Perceptrón Multicapa) simple.
    Su objetivo es predecir si un cliente va a pagar o no (probabilidad de impago/default),
    basándose en su historial de datos (Ingresos, Intentos de login, Antigüedad, etc.).
    """
    def __init__(self):
        # Creamos la Red Neuronal:
        # hidden_layer_sizes=(8, 4) significa 2 capas ocultas: la primera con 8 neuronas y la segunda con 4 neuronas.
        # Es lo suficientemente pequeña para que corra muy rápido.
        self.modelo = MLPClassifier(hidden_layer_sizes=(8, 4), activation='relu', solver='adam', max_iter=500, random_state=42)
        
        # El StandardScaler sirve para normalizar los datos. Por ejemplo, los ingresos son de 3000
        # y los intentos de login son de 1. La red neuronal se confunde si no los ponemos en la misma escala.
        self.scaler = StandardScaler()
        self.entrenado = False

    def entrenar_modelo_simulado(self, num_muestras=1000):
        # 1. GENERAMOS DATOS DE ENTRENAMIENTO
        # Como no tenemos un Excel con miles de clientes reales, generamos datos estadísticos "simulados"
        np.random.seed(42)
        
        ingresos = np.random.normal(2500, 1000, num_muestras)
        intentos = np.random.poisson(1.5, num_muestras)
        antiguedad = np.random.randint(0, 120, num_muestras)
        dsr = np.random.uniform(0.1, 0.8, num_muestras) # Carga financiera
        billetera = np.random.uniform(0, 1, num_muestras) # Uso de billetera digital (0 a 1)

        # X son nuestras "Características" o "Variables de entrada"
        X = pd.DataFrame({
            'ingresos': ingresos,
            'intentos': intentos,
            'antiguedad': antiguedad,
            'dsr': dsr,
            'billetera': billetera
        })

        # 2. DEFINIMOS LA RESPUESTA CORRECTA (y) PARA QUE LA RED APRENDA
        # Fórmula lógica matemática simple: a más ingresos y antigüedad, menos riesgo.
        # A más intentos de login y carga financiera, más riesgo.
        riesgo_matematico = (intentos * 0.1) + (dsr * 0.4) - (ingresos / 10000) - (antiguedad / 200) - (billetera * 0.1)
        
        # Convertimos esa fórmula en una probabilidad de 0 a 1 usando la fórmula sigmoide matemática
        prob_default = 1 / (1 + np.exp(-riesgo_matematico)) 
        
        # Si la probabilidad es mayor a 50%, decimos que es un cliente malo (1). Si no, bueno (0).
        # y es nuestra variable "Objetivo" (Target)
        y = (prob_default > 0.5).astype(int)

        # 3. ENTRENAMOS LA RED NEURONAL
        # Primero normalizamos X
        X_normalizado = self.scaler.fit_transform(X)
        
        # Luego entrenamos la red con los datos de entrada (X) y las respuestas correctas (y)
        self.modelo.fit(X_normalizado, y)
        self.entrenado = True
        
        # Retornamos qué tan precisa fue la red neuronal al aprender (su "nota" de 0 a 1)
        return self.modelo.score(X_normalizado, y)

    def predecir_probabilidad_default(self, ingresos, intentos, antiguedad, dsr, billetera):
        """
        Esta función se usa cuando registramos un Nuevo Cliente en la interfaz.
        Le pasamos sus datos, y la red neuronal escupe la probabilidad de que se vuelva moroso.
        """
        if not self.entrenado:
            self.entrenar_modelo_simulado()
            
        # 1. Armamos el dato del nuevo cliente igual a como entrenamos
        X_nuevo = pd.DataFrame({
            'ingresos': [ingresos],
            'intentos': [intentos],
            'antiguedad': [antiguedad],
            'dsr': [dsr],
            'billetera': [billetera]
        })
        
        # 2. Normalizamos el dato
        X_normalizado = self.scaler.transform(X_nuevo)
        
        # 3. Le pedimos a la red que prediga las probabilidades
        # predict_proba nos devuelve dos números: [Prob de NO ser moroso, Prob de SÍ ser moroso]
        # Tomamos el segundo número (índice 1).
        prob = self.modelo.predict_proba(X_normalizado)[0][1]
        
        return float(prob)
