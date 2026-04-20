:- include('hechos_base.pl').

%% ============================================================================
%% MOTOR DE INFERENCIA - SISTEMA EXPERTO ONBOARDING DUAL (IA NEURO-SIMBÓLICA)
%% Estudiante: IA Arquitecto Senior
%% Asignatura: Lenguaje de Programación III - UNALM
%% ============================================================================
%% Este sistema evalúa clientes "Invisibles Financieros". Utiliza reglas lógicas
%% para generar un "Credit Scoring" y aplicar "Prevención de Fraude", integrando
%% un módulo XAI (Explainable AI) para resolver la "Caja Negra" exigida por SBS.

%% ==========================================
%% MÓDULO 1: PREVENCIÓN DE FRAUDE (SEGURIDAD)
%% ==========================================

%% Regla 1: Base de Conocimiento de riesgo geográfico.
%% Define los países que estadísticamente representan alto riesgo de ciberataque.
pais_riesgo(rusia).
pais_riesgo(china).

%% Regla 2: Filtro Antifraude por Ubicación IP.
%% Se evalúa si el país de conexión del cliente pertenece a la base de riesgo.
es_fraude(Id) :- 
    ubicacion_ip(Id, Pais),                %% Predicado que obtiene el país de conexión.
    pais_riesgo(Pais),                     %% Se unifica si el país pertenece a lista negra.
    format('~n[XAI] ALERTA SEGURIDAD: Cliente ~w rechazado. Conexion IP desde pais de altisimo riesgo (~w).~n', [Id, Pais]).

%% Regla 3: Filtro Antifraude por Fuerza Bruta.
%% Bloquea operaciones que exceden el límite logístico de reintentos permitidos.
es_fraude(Id) :- 
    intentos_login(Id, Intentos),          %% Predicado que obtiene los reintentos
    Intentos > 3,                          %% Operador lógico mayor estricto a 3 intentos.
    format('~n[XAI] ALERTA SEGURIDAD: Cliente ~w rechazado. Exceso de intentos de login (~w). Posible fuerza bruta.~n', [Id, Intentos]).

%% ==========================================
%% MÓDULO 2: EVALUACIÓN DE SCORING CREDITICIO
%% ==========================================

%% Regla 4: Perfil de Capacidad de Pago Sólida.
%% Verifica que se cumplan condiciones óptimas económicas (ingreso y antigüedad).
capacidad_solida(Id) :-
    ingresos(Id, Monto),                   %% Obtenemos el ingreso del usuario en la variable Monto.
    Monto > 2000,                          %% El ingreso debe ser mayor al umbral de seguridad de 2000 soles.
    antiguedad_laboral(Id, Meses),         %% Obtenemos su arraigo laboral.
    Meses > 12.                            %% Debe superar al menos un año de permanencia.

%% Regla 5: Historial Impecable de Servicios.
%% Asegura que no tenga manchas en pagos menores.
historial_impecable(Id) :-
    pago_servicios(Id, puntual).           %% Valor atómico explícito 'puntual'.

%% Regla 6: Historial Deficiente (Riesgo Crediticio).
%% Busca un perfil que represente pérdida y deudas activas.
historial_deficiente(Id) :-
    pago_servicios(Id, moroso).            %% Valor atómico explícito 'moroso'.

%% Regla 7: Fallback o Cobertura Neuro-Simbólica.
%% Identifica la inclusión mediante adopción tecnológica y datos alternativos.
respaldo_digital_fuerte(Id) :-
    billetera_digital(Id, alto).           %% Requiere uso intensivo ('alto') de la billetera digital.

%% ==========================================
%% MÓDULO 3: DECISIÓN FINAL Y XAI (EXPLICABILIDAD)
%% ==========================================

%% Regla 8: Reclamo inmediato por Fraude (Restricción dura).
%% Típicamente es el primer nodo del árbol lógico a evaluar en onboarding.
dictamen_final(Id, 'DENEGADO POR SEGURIDAD') :-
    es_fraude(Id),                         %% Invocamos las reglas de fraude.
    !,                                     %% CUT (!): Poda el árbol, si es fraude no buscamos más reglas.
    format('[XAI] DICTAMEN FINAL: Onboarding Cancelado para ~w por Riesgo de Fraude.~n', [Id]).

%% Regla 9: Aprobación Premium (Scoring perfecto).
%% Cliente con excelentes KPIs de solvencia y puntualidad probada.
dictamen_final(Id, 'APROBADO PREMIUM') :-
    capacidad_solida(Id),                  %% Validación de solvencia (Regla 4).
    historial_impecable(Id),               %% Validación de historia de pago (Regla 5).
    !,                                     %% CUT (!): Se corta porque ya categorizó primariamente.
    format('~n[XAI] DICTAMEN FINAL: Onboarding Exitoso para ~w (Nivel Premium).~n', [Id]),
    format('[XAI] RAZONAMIENTO: Alta solvencia y arraigo laboral combinada con comportamiento puntual.~n').

%% Regla 10: Rechazo por Scoring Crediticio.
%% Un moroso no puede ser calificado para un onboarding financiero sin avales extra.
dictamen_final(Id, 'DENEGADO POR SCORING') :-
    historial_deficiente(Id),              %% Aplicación estricta de la regla de deficiencia.
    !,                                     %% CUT (!): Rechazado automáticamente, fin de evaluación.
    format('~n[XAI] DICTAMEN FINAL: Onboarding Rechazado para ~w por Riesgo Crediticio.~n', [Id]),
    format('[XAI] RAZONAMIENTO: El motor logico detecto comportamiento activo MOROSO en pagos de servicios.~n').

%% Regla 11: Aprobación Estándar (Fallback para Invisibles).
%% Compensación neuronal de variables mediante lógica difusa-fallback.
dictamen_final(Id, 'APROBADO ESTANDAR (FALLBACK)') :-
    ingresos(Id, Monto), Monto >= 800,     %% Primer umbral: ingreso de al menos 800 soles.
    historial_impecable(Id),               %% Segundo umbral: debe ser un perfil puntual sí o sí.
    respaldo_digital_fuerte(Id),           %% Condición X: Su historial digital compensatorio es alto.
    !,                                     %% CUT (!): Califica, terminamos de inferir por aquí.
    format('~n[XAI] DICTAMEN FINAL: Onboarding Exitoso para ~w (Nivel Estandar).~n', [Id]),
    format('[XAI] RAZONAMIENTO: Uso de Fallback. Ingreso modesto de S/.~w mitigado por pago de servicios puntual y alto nivel de Billetera Digital.~n', [Monto]).

%% Regla 12: Evaluación Manual (Incertidumbre - Zona Gris).
%% Todo lo que escape a las reglas deterministas anteriores se lanza a revisión humana.
dictamen_final(Id, 'REQUIERE EVALUACION MANUAL') :-
    ingresos(Id, Monto),                   %% Imprimimos las variables capturadas para explicarle al auditor.
    pago_servicios(Id, Estado),            %% Estado actual.
    billetera_digital(Id, Nivel),          %% Uso digital restante.
    format('~n[XAI] DICTAMEN FINAL: Cliente ~w derivado para Evaluacion Manual por Incertidumbre.~n', [Id]),
    format('[XAI] RAZONAMIENTO: Variables difusas. Ingresos: S/.~w | Pagos: ~w | Nivel Billetera: ~w. No encaja en limites deterministas.~n', [Monto, Estado, Nivel]).

%% Regla 13: Entry Point (Query Principal).
%% Wrapper diseñado para ejecutar las simulaciones requeridas en el test.
evaluar_cliente(Id) :-
    format('~n======================================================~n'),
    format('>> INICIANDO MOTOR DE INFERENCIA PARA CLIENTE: ~w~n', [Id]),
    dictamen_final(Id, Resultado),         %% Invoca la estructura piramidal descrita anteriormente.
    format('>> CONCLUSIÓN DEL EXPERTO: ~w~n', [Resultado]),
    format('======================================================~n').
