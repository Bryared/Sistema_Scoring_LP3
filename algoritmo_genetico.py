import random
import numpy as np
from deap import base, creator, tools, algorithms

class OptimizadorCarteraAG:
    """
    Clase para optimizar a qué clientes prestarles dinero usando un Algoritmo Genético.
    Es una adaptación sencilla del "Problema de la Mochila" (Knapsack Problem).
    El "banco" tiene una mochila (presupuesto), y quiere meter a los clientes más rentables
    sin pasarse del peso máximo (presupuesto límite).
    """
    def __init__(self, clientes_data, presupuesto_maximo=1000000):
        self.clientes = clientes_data
        self.num_clientes = len(clientes_data)
        self.presupuesto_maximo = presupuesto_maximo
        
        # 1. PREPARACIÓN DEL ALGORITMO GENÉTICO (Librería DEAP)
        # Limpiamos variables previas si se vuelve a correr en Streamlit
        if hasattr(creator, "FitnessMax"):
            del creator.FitnessMax
        if hasattr(creator, "Individual"):
            del creator.Individual
            
        # FitnessMax: Le decimos al algoritmo que nuestro objetivo es "Maximizar" (weight=1.0) la ganancia.
        creator.create("FitnessMax", base.Fitness, weights=(1.0,))
        # Individual: Creamos un "Individuo" (Cromosoma). Será una simple lista de números (ej. [1,0,1,0,0...])
        creator.create("Individual", list, fitness=creator.FitnessMax)
        
        self.toolbox = base.Toolbox()
        
        # 2. DEFINIMOS LOS GENES Y CROMOSOMAS
        # Gen: un número aleatorio entre 0 (No darle préstamo) y 1 (Sí darle préstamo)
        self.toolbox.register("attr_bool", random.randint, 0, 1)
        # Individuo (Cromosoma): Una lista llena de 0s y 1s, tan larga como el número de clientes.
        self.toolbox.register("individual", tools.initRepeat, creator.Individual, self.toolbox.attr_bool, self.num_clientes)
        # Población: Un grupo de muchos individuos (posibles soluciones/carteras).
        self.toolbox.register("population", tools.initRepeat, list, self.toolbox.individual)
        
        # 3. REGLAS EVOLUTIVAS (Cómo evaluamos, cruzamos y mutamos)
        self.toolbox.register("evaluate", self.evaluar_cartera) # ¿Qué tan buena es esta cartera?
        self.toolbox.register("mate", tools.cxTwoPoint) # Cruce de dos padres
        self.toolbox.register("mutate", tools.mutFlipBit, indpb=0.05) # Mutación: cambiar un 0 por 1 o viceversa
        self.toolbox.register("select", tools.selTournament, tournsize=3) # Selección por torneo: los mejores sobreviven

    def evaluar_cartera(self, individual):
        """
        Esta es la FUNCIÓN DE APTITUD (Fitness Function).
        Mide matemáticamente qué tan buena es una combinación de clientes (individuo).
        """
        inversion_total = 0.0
        retorno_esperado = 0.0
        
        # Recorremos la lista de 1s y 0s del individuo
        for i in range(self.num_clientes):
            if individual[i] == 1: # Si el gen es 1, significa que le prestamos a este cliente
                cliente = self.clientes[i]
                prestamo = cliente['prestamo']
                prob_default = cliente['prob_default'] # La probabilidad que nos dio la Red Neuronal
                tasa_interes = cliente['tasa_interes']
                
                inversion_total += prestamo
                
                # GANANCIA = Interés que nos va a pagar
                ganancia_interes = prestamo * tasa_interes
                # RIESGO = Pérdida estadística si no paga
                riesgo_perdida = prestamo * prob_default
                
                # El retorno neto de este cliente
                retorno_esperado += (ganancia_interes - riesgo_perdida)
                
        # RESTRICCIÓN DEL BANCO: Penalidad proporcional si nos pasamos del presupuesto
        if inversion_total > self.presupuesto_maximo:
            exceso = inversion_total - self.presupuesto_maximo
            return retorno_esperado - (exceso * 2.0), 
            
        # Retornamos la ganancia neta. El algoritmo siempre intentará maximizar esto.
        return retorno_esperado,

    def optimizar(self, tam_poblacion=50, generaciones=40):
        """
        Ejecuta el ciclo de la vida: crea la población inicial y la hace evolucionar.
        """
        if self.num_clientes == 0:
            return [], 0, 0
            
        # Generamos la población inicial
        pop = self.toolbox.population(n=tam_poblacion)
        # Salón de la Fama: Aquí guardamos al MEJOR individuo de toda la evolución
        hof = tools.HallOfFame(1)
        
        # eaSimple: Evolutionary Algorithm Simple. El ciclo de evolución.
        algorithms.eaSimple(pop, self.toolbox, cxpb=0.5, mutpb=0.2, ngen=generaciones, 
                            halloffame=hof, verbose=False)
        
        # Rescatamos al mejor de todos los tiempos
        mejor_individuo = hof[0]
        
        # Filtramos a los clientes reales basándonos en los 1s del mejor individuo
        clientes_seleccionados = [self.clientes[i] for i in range(self.num_clientes) if mejor_individuo[i] == 1]
        
        inversion_total = sum(c['prestamo'] for c in clientes_seleccionados)
        retorno_total = self.evaluar_cartera(mejor_individuo)[0]
        
        return clientes_seleccionados, inversion_total, retorno_total
