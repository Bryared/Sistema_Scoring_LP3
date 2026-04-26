import numpy as np
import pandas as pd
from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
import random

class CalculadorScoringNeuronal:
    def __init__(self):
        self.modelo = MLPClassifier(hidden_layer_sizes=(16, 8), activation='relu', solver='adam', max_iter=500, random_state=42)
        self.scaler = StandardScaler()
        self.entrenado = False

    def entrenar_modelo_simulado(self, num_muestras=1000):
        # Generar datos simulados para entrenar la red neuronal
        np.random.seed(42)
        
        # Características: Ingresos, intentos_login, meses_antiguedad, DSR (Carga Financiera), ratio_billetera
        ingresos = np.random.normal(2500, 1000, num_muestras)
        intentos = np.random.poisson(1.5, num_muestras)
        antiguedad = np.random.randint(0, 120, num_muestras)
        dsr = np.random.uniform(0.1, 0.8, num_muestras)
        billetera = np.random.uniform(0, 1, num_muestras)

        X = pd.DataFrame({
            'ingresos': ingresos,
            'intentos': intentos,
            'antiguedad': antiguedad,
            'dsr': dsr,
            'billetera': billetera
        })

        # Lógica oculta para generar la variable objetivo (default = 1, pago_ok = 0)
        prob_default = (
            (intentos * 0.1) + 
            (dsr * 0.4) - 
            (ingresos / 10000) - 
            (antiguedad / 200) -
            (billetera * 0.1)
        )
        # Convertir a probabilidad entre 0 y 1
        prob_default = 1 / (1 + np.exp(-prob_default)) # Sigmoide
        y = (prob_default > 0.5).astype(int)

        # Escalar datos
        X_scaled = self.scaler.fit_transform(X)
        
        # Entrenar Red Neuronal Multicapa
        self.modelo.fit(X_scaled, y)
        self.entrenado = True
        return self.modelo.score(X_scaled, y) # Retorna el accuracy de entrenamiento

    def predecir_probabilidad_default(self, ingresos, intentos, antiguedad, dsr, billetera):
        if not self.entrenado:
            self.entrenar_modelo_simulado()
            
        X_nuevo = pd.DataFrame({
            'ingresos': [ingresos],
            'intentos': [intentos],
            'antiguedad': [antiguedad],
            'dsr': [dsr],
            'billetera': [billetera]
        })
        X_scaled = self.scaler.transform(X_nuevo)
        
        # La probabilidad de la clase 1 (Default)
        prob = self.modelo.predict_proba(X_scaled)[0][1]
        return float(prob)
