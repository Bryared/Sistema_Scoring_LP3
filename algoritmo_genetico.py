import random
import numpy as np
from deap import base, creator, tools, algorithms

class OptimizadorCarteraAG:
    def __init__(self, clientes_data, presupuesto_maximo=1000000):
        """
        clientes_data: Lista de diccionarios con {'id': str, 'prestamo': float, 'prob_default': float, 'tasa_interes': float}
        presupuesto_maximo: Dinero total disponible para prestar.
        """
        self.clientes = clientes_data
        self.num_clientes = len(clientes_data)
        self.presupuesto_maximo = presupuesto_maximo
        
        # Resetear el creador por si se instancia múltiples veces en Streamlit
        if hasattr(creator, "FitnessMax"):
            del creator.FitnessMax
        if hasattr(creator, "Individual"):
            del creator.Individual
            
        # Definir problema de maximización
        creator.create("FitnessMax", base.Fitness, weights=(1.0,))
        creator.create("Individual", list, fitness=creator.FitnessMax)
        
        self.toolbox = base.Toolbox()
        # Generador de atributos (0 o 1)
        self.toolbox.register("attr_bool", random.randint, 0, 1)
        # Inicializador de individuos y población
        self.toolbox.register("individual", tools.initRepeat, creator.Individual, self.toolbox.attr_bool, self.num_clientes)
        self.toolbox.register("population", tools.initRepeat, list, self.toolbox.individual)
        
        # Registrar operadores genéticos
        self.toolbox.register("evaluate", self.evaluar_cartera)
        self.toolbox.register("mate", tools.cxTwoPoint)
        self.toolbox.register("mutate", tools.mutFlipBit, indpb=0.05)
        self.toolbox.register("select", tools.selTournament, tournsize=3)

    def evaluar_cartera(self, individual):
        inversion_total = 0.0
        retorno_esperado = 0.0
        
        for i in range(self.num_clientes):
            if individual[i] == 1:
                cliente = self.clientes[i]
                prestamo = cliente['prestamo']
                prob_default = cliente['prob_default']
                tasa_interes = cliente['tasa_interes']
                
                inversion_total += prestamo
                
                # Cálculo simplificado del retorno: Ganancia por interés - Pérdida por probabilidad de default
                ganancia_interes = prestamo * tasa_interes
                riesgo_perdida = prestamo * prob_default
                retorno_esperado += (ganancia_interes - riesgo_perdida)
                
        # Penalización severa si supera el presupuesto
        if inversion_total > self.presupuesto_maximo:
            return -1000000.0, # Retorno fuertemente negativo
            
        return retorno_esperado,

    def optimizar(self, tam_poblacion=50, generaciones=40):
        if self.num_clientes == 0:
            return [], 0, 0
            
        pop = self.toolbox.population(n=tam_poblacion)
        hof = tools.HallOfFame(1)
        stats = tools.Statistics(lambda ind: ind.fitness.values)
        stats.register("avg", np.mean)
        stats.register("max", np.max)
        
        # Algoritmo genético simple
        algorithms.eaSimple(pop, self.toolbox, cxpb=0.5, mutpb=0.2, ngen=generaciones, 
                            stats=stats, halloffame=hof, verbose=False)
        
        mejor_individuo = hof[0]
        clientes_seleccionados = [self.clientes[i] for i in range(self.num_clientes) if mejor_individuo[i] == 1]
        
        inversion_total = sum(c['prestamo'] for c in clientes_seleccionados)
        retorno_total = self.evaluar_cartera(mejor_individuo)[0]
        
        return clientes_seleccionados, inversion_total, retorno_total
