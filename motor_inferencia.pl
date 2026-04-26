:- include('hechos_base.pl').

%% ============================================================================
%% MOTOR DE INFERENCIA - SISTEMA EXPERTO NEURO-SIMBÓLICO DE NIVEL 2
%% ============================================================================
%% Este sistema lee datos simbólicos y predicciones neuronales generadas por 
%% Modelos de Machine Learning (Python: Scikit-Learn).

%% ==========================================
%% MÓDULO 1: PREVENCIÓN DE FRAUDE (SEGURIDAD LÓGICA Y ANOMALÍAS ML)
%% ==========================================

pais_riesgo(rusia).
pais_riesgo(china).

es_fraude(Id) :- dni_vencido(Id, true), format('~n[XAI] ALERTA SEGURIDAD: Cliente ~w rechazado. DNI caducado.~n', [Id]).
es_fraude(Id) :- en_lista_ofac(Id, true), format('~n[XAI] ALERTA SEGURIDAD CRITICA: Cliente ~w rechazado. Coincidencia en lista OFAC.~n', [Id]).
es_fraude(Id) :- ubicacion_ip(Id, Pais), pais_riesgo(Pais), format('~n[XAI] ALERTA SEGURIDAD: Pais de alto riesgo (~w).~n', [Pais]).
es_fraude(Id) :- intentos_login(Id, Intentos), Intentos > 3, format('~n[XAI] ALERTA SEGURIDAD: Fuerza bruta.~n').
es_fraude(Id) :- tiempo_llenado(Id, S), S < 10, format('~n[XAI] ALERTA SEGURIDAD: BOT Detectado.~n').
es_fraude(Id) :- ubicacion_ip(Id, IP), residencia(Id, Res), IP \= Res, justificacion_vpn(Id, false), format('~n[XAI] ALERTA SEGURIDAD: VPN no justificada.~n').
es_fraude(Id) :- dispositivo_imei(Id, Imei), imei_en_lista_negra(Imei), format('~n[XAI] ALERTA SEGURIDAD: IMEI en lista negra.~n').

%% ==========================================
%% MÓDULO 2: EVALUACIÓN DE SCORING CREDITICIO (NEURO-SIMBÓLICA)
%% ==========================================

carga_financiera(Id, Porcentaje) :-
    ingresos(Id, Ingreso), Ingreso > 0,
    suma_cuotas_mensuales(Id, TotalCuotas),
    Porcentaje is (TotalCuotas / Ingreso) * 100.

%% REGLA NEURO-SIMBÓLICA: CLUSTERING ML (K-Means)
%% Se ajusta el límite de DSR basándose en el Perfil Predictivo.
riesgo_alto_credito(Id) :-
    carga_financiera(Id, Carga), ml_perfil_cluster(Id, joven_riesgoso), Carga > 25,
    format('~n[XAI] RECHAZO NEURO-SIMBOLICO: Cluster ML "Joven Riesgoso" supera DSR ajustado al 25%.~n').

riesgo_alto_credito(Id) :-
    carga_financiera(Id, Carga), ml_perfil_cluster(Id, emprendedor_promedio), Carga > 35,
    format('~n[XAI] RECHAZO NEURO-SIMBOLICO: Cluster ML "Emprendedor Promedio" supera DSR del 35%.~n').

riesgo_alto_credito(Id) :-
    carga_financiera(Id, Carga), ml_perfil_cluster(Id, familia_estable), Carga > 40,
    format('~n[XAI] RECHAZO NEURO-SIMBOLICO: Cluster ML "Familia Estable" supera DSR extendido al 40%.~n').

%% REGLA NEURO-SIMBÓLICA: SCORE PREDICTIVO ML (Regresión Logística)
riesgo_alto_credito(Id) :-
    ml_probabilidad_default(Id, Prob), Prob > 0.85,
    ProbPerc is Prob * 100,
    format('~n[XAI] RECHAZO NEURO-SIMBOLICO: Machine Learning predice ~2f% de probabilidad de quiebra.~n', [ProbPerc]).

%% Lógicas clásicas
riesgo_alto_credito(Id) :- creditos_activos(Id, C), C > 3, format('~n[XAI] RECHAZO SCORING: Ruleteo detectado.~n').
riesgo_alto_credito(Id) :- consultas_bancarias_15dias(Id, C), C > 5, format('~n[XAI] RECHAZO SCORING: Huella de desesperacion.~n').
riesgo_alto_credito(Id) :- pago_servicios(Id, moroso), format('~n[XAI] RECHAZO SCORING: Morosidad historica.~n').

capacidad_solida(Id) :- ingresos(Id, M), M > 2000, antiguedad_laboral(Id, Mes), Mes > 12.
historial_impecable(Id) :- pago_servicios(Id, puntual).
estabilidad_alta(Id) :- antiguedad_domicilio(Id, M), M > 24, sector_laboral(Id, S), (S = tecnologia ; S = salud ; S = educacion).
respaldo_digital_fuerte(Id) :- billetera_digital(Id, alto).

%% ==========================================
%% MÓDULO 3: DICTAMEN FINAL NEURO-SIMBÓLICO
%% ==========================================

dictamen_final(Id, 'DENEGADO POR SEGURIDAD (FRAUDE LÓGICO DETECTADO)') :-
    es_fraude(Id),
    !, format('[XAI] DICTAMEN FINAL: Onboarding Cancelado por seguridad estricta.~n').

%% REGLA NEURO-SIMBÓLICA: ANOMALÍAS ML (Isolation Forest)
dictamen_final(Id, 'REQUIERE VALIDACION BIOMETRICA FACIAL (ANOMALIA ML DETECTADA)') :-
    ml_fraude_anomalia(Id, true),
    !, format('[XAI] DICTAMEN FINAL: El modelo Isolation Forest detecto comportamiento invisible no catalogable. Obligar Biometria Liveness.~n').

dictamen_final(Id, 'REQUIERE EVALUACION MANUAL (ALERTA PEP)') :-
    es_pep(Id, true),
    !, format('[XAI] DICTAMEN FINAL: Persona Politicamente Expuesta.~n').

dictamen_final(Id, 'DENEGADO POR RIESGO CREDITICIO') :-
    riesgo_alto_credito(Id),
    !, format('[XAI] DICTAMEN FINAL: Onboarding Rechazado (Combina reglas SBS y Predicciones de Machine Learning).~n').

dictamen_final(Id, 'APROBADO PREMIUM') :-
    capacidad_solida(Id), historial_impecable(Id), estabilidad_alta(Id),
    !, format('~n[XAI] DICTAMEN FINAL: Onboarding Exitoso (Premium).~n').

dictamen_final(Id, 'APROBADO ESTANDAR') :-
    ingresos(Id, M), M >= 800, historial_impecable(Id), respaldo_digital_fuerte(Id),
    !, format('~n[XAI] DICTAMEN FINAL: Onboarding Exitoso (Estandar).~n').

dictamen_final(Id, 'REQUIERE EVALUACION MANUAL') :-
    format('~n[XAI] DICTAMEN FINAL: Zonas grises, derivar a analista humano para ~w.~n', [Id]).

evaluar_cliente(Id) :-
    format('~n======================================================~n'),
    format('>> INICIANDO MOTOR DE INFERENCIA NEURO-SIMBOLICO: ~w~n', [Id]),
    dictamen_final(Id, Resultado),         
    format('>> CONCLUSIÓN DEL SISTEMA: ~w~n', [Resultado]),
    format('======================================================~n').

%% ==========================================
%% MÓDULO 4: PREVENCIÓN DE LAVADO DE ACTIVOS (AML + NLP)
%% ==========================================

%% REGLA NEURO-SIMBÓLICA: Si el modelo NLP de Python detecta que las palabras en
%% la transferencia son "Sospechosas" (ej: 'inversion xyz'), Prolog disminuye 
%% la tolerancia a la mitad para cazar redes de lavado encubiertas.

alerta_aml(Id, ToleranciaBase, 'LAVADO DE ACTIVOS (SMURFING DETECTADO)') :-
    transferencia(Id, B, Monto1, Ts1, _, _), Monto1 > 10000,
    transferencia(B, C, _, _, _, _),
    transferencia(C, Id, Monto3, Ts3, _, _),
    Id \= B, B \= C, C \= Id,
    
    DiferenciaSegundos is Ts3 - Ts1,
    DiferenciaSegundos =< 259200,
    DiferenciaSegundos >= 0,
    
    ( ml_texto_sospechoso(Id, B, true) -> ToleranciaFinal is ToleranciaBase / 2 ; ToleranciaFinal is ToleranciaBase ),
    
    RetornoMinimo is Monto1 * (1.0 - ToleranciaFinal),
    Monto3 >= RetornoMinimo,
    Monto3 =< Monto1,
    !,
    format('~n[XAI] ALERTA AML CRITICA: Triangulacion rapida detectada (Smurfing).~n'),
    format('[XAI] COMPONENTE NEURO (NLP): Tolerancia ajustada al ~2f%.~n', [ToleranciaFinal * 100]),
    format('[XAI] TRAZA: Salio ~w a ~w. Regreso ~w a ~w.~n', [Monto1, B, Monto3, Id]).

alerta_aml(_, _, 'SIN RIESGO DE LAVADO').

traza_aml_nodos(Id, ToleranciaBase, B, C, Monto1, Monto2, Monto3) :-
    transferencia(Id, B, Monto1, Ts1, _, _), Monto1 > 10000,
    transferencia(B, C, Monto2, _, _, _),
    transferencia(C, Id, Monto3, Ts3, _, _),
    Id \= B, B \= C, C \= Id,
    DiferenciaSegundos is Ts3 - Ts1,
    DiferenciaSegundos =< 259200,
    DiferenciaSegundos >= 0,
    ( ml_texto_sospechoso(Id, B, true) -> ToleranciaFinal is ToleranciaBase / 2 ; ToleranciaFinal is ToleranciaBase ),
    RetornoMinimo is Monto1 * (1.0 - ToleranciaFinal),
    Monto3 >= RetornoMinimo,
    Monto3 =< Monto1,
    !.

%% ==========================================
%% MÓDULO 5 Y 6: COMPLIANCE E INDECOPI (ESTÁTICO)
%% ==========================================

intervencion_sbs(Id, 'RIESGO DE INSOLVENCIA (ACTIVO LIQUIDO)') :-
    tipo_patrimonio(Id, liquido), patrimonio(Id, P), deuda_total(Id, D),
    Umbral is P * 5, D > Umbral, !.

intervencion_sbs(Id, 'RIESGO DE INSOLVENCIA (ACTIVO INMOBILIARIO)') :-
    tipo_patrimonio(Id, inmobiliario), patrimonio(Id, P), deuda_total(Id, D),
    Umbral is P * 3, D > Umbral, !.

intervencion_sbs(_, 'SOLVENTE (CUMPLE POLITICAS)').

auditoria_cobros(Id, 'COBRO INDEBIDO DETECTADO') :-
    tasa_acordada(Id, TA), tasa_cobrada(Id, TC), TC > TA, !.

auditoria_cobros(_, 'CONTRATO LIMPIO').
