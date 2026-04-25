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
pais_riesgo(rusia).
pais_riesgo(china).

%% Regla 2: Filtro Antifraude por Ubicación IP.
es_fraude(Id) :- 
    ubicacion_ip(Id, Pais),                
    pais_riesgo(Pais),                     
    format('~n[XAI] ALERTA SEGURIDAD: Cliente ~w rechazado. Conexion IP desde pais de altisimo riesgo (~w).~n', [Id, Pais]).

%% Regla 3: Filtro Antifraude por Fuerza Bruta.
es_fraude(Id) :- 
    intentos_login(Id, Intentos),          
    Intentos > 3,                          
    format('~n[XAI] ALERTA SEGURIDAD: Cliente ~w rechazado. Exceso de intentos de login (~w). Posible fuerza bruta.~n', [Id, Intentos]).

%% ==========================================
%% MÓDULO 2: EVALUACIÓN DE SCORING CREDITICIO
%% ==========================================

%% Regla 4: Perfil de Capacidad de Pago Sólida.
capacidad_solida(Id) :-
    ingresos(Id, Monto),                   
    Monto > 2000,                          
    antiguedad_laboral(Id, Meses),         
    Meses > 12.                            

%% Regla 5: Historial Impecable de Servicios.
historial_impecable(Id) :-
    pago_servicios(Id, puntual).           

%% Regla 6: Historial Deficiente (Riesgo Crediticio).
historial_deficiente(Id) :-
    pago_servicios(Id, moroso).            

%% Regla 7: Fallback o Cobertura Neuro-Simbólica.
respaldo_digital_fuerte(Id) :-
    billetera_digital(Id, alto).           

%% ==========================================
%% MÓDULO 3: DECISIÓN FINAL Y XAI (EXPLICABILIDAD)
%% ==========================================

dictamen_final(Id, 'DENEGADO POR SEGURIDAD') :-
    es_fraude(Id),                         
    !,                                     
    format('[XAI] DICTAMEN FINAL: Onboarding Cancelado para ~w por Riesgo de Fraude.~n', [Id]).

dictamen_final(Id, 'APROBADO PREMIUM') :-
    capacidad_solida(Id),                  
    historial_impecable(Id),               
    !,                                     
    format('~n[XAI] DICTAMEN FINAL: Onboarding Exitoso para ~w (Nivel Premium).~n', [Id]),
    format('[XAI] RAZONAMIENTO: Alta solvencia y arraigo laboral combinada con comportamiento puntual.~n').

dictamen_final(Id, 'DENEGADO POR SCORING') :-
    historial_deficiente(Id),              
    !,                                     
    format('~n[XAI] DICTAMEN FINAL: Onboarding Rechazado para ~w por Riesgo Crediticio.~n', [Id]),
    format('[XAI] RAZONAMIENTO: El motor logico detecto comportamiento activo MOROSO en pagos de servicios.~n').

dictamen_final(Id, 'APROBADO ESTANDAR (FALLBACK)') :-
    ingresos(Id, Monto), Monto >= 800,     
    historial_impecable(Id),               
    respaldo_digital_fuerte(Id),           
    !,                                     
    format('~n[XAI] DICTAMEN FINAL: Onboarding Exitoso para ~w (Nivel Estandar).~n', [Id]),
    format('[XAI] RAZONAMIENTO: Uso de Fallback. Ingreso modesto de S/.~w mitigado por pago de servicios puntual y alto nivel de Billetera Digital.~n', [Monto]).

dictamen_final(Id, 'REQUIERE EVALUACION MANUAL') :-
    ingresos(Id, Monto),                   
    pago_servicios(Id, Estado),            
    billetera_digital(Id, Nivel),          
    format('~n[XAI] DICTAMEN FINAL: Cliente ~w derivado para Evaluacion Manual por Incertidumbre.~n', [Id]),
    format('[XAI] RAZONAMIENTO: Variables difusas. Ingresos: S/.~w | Pagos: ~w | Nivel Billetera: ~w. No encaja en limites deterministas.~n', [Monto, Estado, Nivel]).

evaluar_cliente(Id) :-
    format('~n======================================================~n'),
    format('>> INICIANDO MOTOR DE INFERENCIA PARA CLIENTE: ~w~n', [Id]),
    dictamen_final(Id, Resultado),         
    format('>> CONCLUSIÓN DEL EXPERTO: ~w~n', [Resultado]),
    format('======================================================~n').

%% ==========================================
%% MÓDULO 4: PREVENCIÓN DE LAVADO DE ACTIVOS (AML)
%% ==========================================

%% Regla AML: Detectar triangulación financiera (Max 3 saltos).
%% Condición: A -> B -> C -> A. Con montos considerables (> S/10000).
alerta_aml(Id, 'LAVADO DE ACTIVOS (TRIANGULACION)') :-
    transferencia(Id, B, Monto1, _), Monto1 > 10000,
    transferencia(B, C, Monto2, _), Monto2 > 10000,
    transferencia(C, Id, Monto3, _), Monto3 > 10000,
    Id \= B, B \= C, C \= Id,
    !,
    format('~n[XAI] ALERTA AML: Triangulacion detectada (Ciclo Cerrado 3 saltos).~n'),
    format('[XAI] TRAZA: ~w -> ~w -> ~w -> ~w.~n', [Id, B, C, Id]).

%% Si no hay alerta, predicado fallback para la UI
alerta_aml(_, 'SIN RIESGO DE LAVADO').

%% ==========================================
%% MÓDULO 5: COMPLIANCE SBS E INSOLVENCIA
%% ==========================================

%% Regla SBS: Insolvencia Técnica.
%% Si la Deuda Total es mayor a 3 veces el Patrimonio Neto.
intervencion_sbs(Id, 'RIESGO DE INSOLVENCIA (SBS)') :-
    patrimonio(Id, Patrimonio),
    deuda_total(Id, Deuda),
    Umbral is Patrimonio * 3,
    Deuda > Umbral,
    !,
    get_time(TimeStamp), format_time(atom(TimeStr), '%Y-%m-%d %H:%M:%S', TimeStamp),
    format('~n[XAI] COMPLIANCE: Insolvencia detectada. Timestamp Audit: ~w~n', [TimeStr]),
    format('[XAI] TRAZA: Deuda (S/.~w) supera 3x el Patrimonio (S/.~w).~n', [Deuda, Patrimonio]).

%% Fallback
intervencion_sbs(_, 'SOLVENTE (CUMPLE SBS)').

%% ==========================================
%% MÓDULO 6: AUDITORÍA DE COBROS INDEBIDOS
%% ==========================================

%% Regla Auditoría: Tasa Cobrada > Tasa Acordada.
auditoria_cobros(Id, 'COBRO INDEBIDO DETECTADO') :-
    tasa_acordada(Id, TAcordada),
    tasa_cobrada(Id, TCobrada),
    TCobrada > TAcordada,
    !,
    Diferencia is TCobrada - TAcordada,
    format('~n[XAI] AUDITORIA: Diferencia en contrato detectada.~n'),
    format('[XAI] TRAZA: Tasa cobrada (~w) es mayor a la acordada (~w). Diferencia: ~w.~n', [TCobrada, TAcordada, Diferencia]).

%% Fallback
auditoria_cobros(_, 'CONTRATO LIMPIO').
