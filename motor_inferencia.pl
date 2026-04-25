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
%% MÓDULO 1: PREVENCIÓN DE FRAUDE (SEGURIDAD - 6 FILTROS)
%% ==========================================

%% Regla 1.1: Base de Conocimiento de riesgo geográfico.
pais_riesgo(rusia).
pais_riesgo(china).

%% Regla 1.2: Filtro KYC (Identidad).
es_fraude(Id) :-
    dni_vencido(Id, true),
    format('~n[XAI] ALERTA SEGURIDAD: Cliente ~w rechazado. DNI caducado, KYC fallido.~n', [Id]).

%% Regla 1.3: Filtro Compliance Internacional (OFAC).
es_fraude(Id) :-
    en_lista_ofac(Id, true),
    format('~n[XAI] ALERTA SEGURIDAD CRITICA: Cliente ~w rechazado. Coincidencia en lista OFAC (Terrorismo/Sancionados).~n', [Id]).

%% Regla 1.4: Filtro Antifraude por Ubicación IP (Geolocalización).
es_fraude(Id) :- 
    ubicacion_ip(Id, Pais),                
    pais_riesgo(Pais),                     
    format('~n[XAI] ALERTA SEGURIDAD: Cliente ~w rechazado. Conexion IP desde pais de altisimo riesgo (~w).~n', [Id, Pais]).

%% Regla 1.5: Filtro Antifraude por Fuerza Bruta.
es_fraude(Id) :- 
    intentos_login(Id, Intentos),          
    Intentos > 3,                          
    format('~n[XAI] ALERTA SEGURIDAD: Cliente ~w rechazado. Exceso de intentos de login (~w). Posible fuerza bruta.~n', [Id, Intentos]).

%% Regla 1.6: Filtro Anti-Bots (Velocidad de Llenado).
es_fraude(Id) :-
    tiempo_llenado(Id, Segundos),
    Segundos < 10,
    format('~n[XAI] ALERTA SEGURIDAD: Cliente ~w rechazado. Tiempo de interaccion (~ws) indica que es un BOT.~n', [Id, Segundos]).

%% Regla 1.7: Suplantación IP vs Residencia (Filtro VPN).
es_fraude(Id) :-
    ubicacion_ip(Id, IP),
    residencia(Id, Residencia),
    IP \= Residencia,
    justificacion_vpn(Id, false),
    format('~n[XAI] ALERTA SEGURIDAD: Cliente ~w rechazado. IP de conexion (~w) no coincide con pais de residencia (~w) y no hay justificacion VPN.~n', [Id, IP, Residencia]).

%% Regla 1.8: Lista Negra de Dispositivos (IMEI).
es_fraude(Id) :-
    dispositivo_imei(Id, Imei),
    imei_en_lista_negra(Imei),
    format('~n[XAI] ALERTA SEGURIDAD: Cliente ~w rechazado. Dispositivo IMEI (~w) figura en Lista Negra de OSIPTEL.~n', [Id, Imei]).

%% ==========================================
%% MÓDULO 2: EVALUACIÓN DE SCORING CREDITICIO (EMBUDO FINAL)
%% ==========================================

%% Regla 2.1: DSR (Carga Financiera). Limite 35%.
carga_financiera(Id, Porcentaje) :-
    ingresos(Id, Ingreso),
    Ingreso > 0,
    suma_cuotas_mensuales(Id, TotalCuotas),
    Porcentaje is (TotalCuotas / Ingreso) * 100.

riesgo_alto_credito(Id) :-
    carga_financiera(Id, Carga),
    Carga > 35,
    format('~n[XAI] RECHAZO SCORING: Cliente ~w con Carga Financiera (DSR) del ~2f%. Sobreendeudamiento critico.~n', [Id, Carga]).

%% Regla 2.2: Filtro de Ruleteo.
riesgo_alto_credito(Id) :-
    creditos_activos(Id, Cantidad),
    Cantidad > 3,
    format('~n[XAI] RECHAZO SCORING: Cliente ~w tiene demasiadas lineas de credito activas (~w). Riesgo de ruleteo.~n', [Id, Cantidad]).

%% Regla 2.3: Huella de Desesperacion.
riesgo_alto_credito(Id) :-
    consultas_bancarias_15dias(Id, Consultas),
    Consultas > 5,
    format('~n[XAI] RECHAZO SCORING: Cliente ~w con Huella de Desesperacion (~w consultas en 15 dias). Multiples rechazos previos probables.~n', [Id, Consultas]).

%% Regla 2.4: Historial Deficiente Clasico.
riesgo_alto_credito(Id) :-
    pago_servicios(Id, moroso),
    format('~n[XAI] RECHAZO SCORING: El motor logico detecto comportamiento activo MOROSO en pagos de servicios.~n').

%% --- FACTORES POSITIVOS (Para Aprobacion Premium o Estandar) ---

capacidad_solida(Id) :-
    ingresos(Id, Monto), Monto > 2000,
    antiguedad_laboral(Id, Meses), Meses > 12.

historial_impecable(Id) :-
    pago_servicios(Id, puntual).

estabilidad_alta(Id) :-
    antiguedad_domicilio(Id, Meses), Meses > 24,
    sector_laboral(Id, Sector), (Sector = tecnologia ; Sector = salud ; Sector = educacion).

respaldo_digital_fuerte(Id) :-
    billetera_digital(Id, alto).

%% ==========================================
%% MÓDULO 3: DECISIÓN FINAL Y XAI (EXPLICABILIDAD)
%% ==========================================

dictamen_final(Id, 'DENEGADO POR SEGURIDAD (FRAUDE DETECTADO)') :-
    es_fraude(Id),
    !, format('[XAI] DICTAMEN FINAL: Onboarding Cancelado para ~w por Riesgo Critico de Fraude.~n', [Id]).

dictamen_final(Id, 'REQUIERE EVALUACION MANUAL (ALERTA PEP)') :-
    es_pep(Id, true),
    !, format('[XAI] DICTAMEN FINAL: Cliente ~w es Persona Politicamente Expuesta (PEP). Requiere validacion de Alta Gerencia.~n', [Id]).

dictamen_final(Id, 'DENEGADO POR RIESGO CREDITICIO') :-
    riesgo_alto_credito(Id),
    !, format('[XAI] DICTAMEN FINAL: Onboarding Rechazado para ~w por incumplir politicas de Riesgo Crediticio SBS/Internas.~n', [Id]).

dictamen_final(Id, 'APROBADO PREMIUM') :-
    capacidad_solida(Id),
    historial_impecable(Id),
    estabilidad_alta(Id),
    !, format('~n[XAI] DICTAMEN FINAL: Onboarding Exitoso para ~w (Nivel Premium).~n', [Id]),
    format('[XAI] RAZONAMIENTO: Alta solvencia, arraigo domiciliario >24m, sector estable y DSR saludable.~n').

dictamen_final(Id, 'APROBADO ESTANDAR (FALLBACK NEURO-SIMBÓLICO)') :-
    ingresos(Id, Monto), Monto >= 800,
    historial_impecable(Id),
    respaldo_digital_fuerte(Id),
    !, format('~n[XAI] DICTAMEN FINAL: Onboarding Exitoso para ~w (Nivel Estandar).~n', [Id]),
    format('[XAI] RAZONAMIENTO: Ingreso modesto de S/.~w mitigado por pago puntual, buena huella digital y ausencia de señales de fraude o ruleteo.~n', [Monto]).

dictamen_final(Id, 'REQUIERE EVALUACION MANUAL') :-
    ingresos(Id, Monto),
    pago_servicios(Id, Estado),
    format('~n[XAI] DICTAMEN FINAL: Cliente ~w derivado para Evaluacion Manual por Incertidumbre.~n', [Id]),
    format('[XAI] RAZONAMIENTO: Variables difusas que no permiten asignacion automatica ni rechazo directo.~n').

evaluar_cliente(Id) :-
    format('~n======================================================~n'),
    format('>> INICIANDO MOTOR DE INFERENCIA PARA CLIENTE: ~w~n', [Id]),
    dictamen_final(Id, Resultado),         
    format('>> CONCLUSIÓN DEL EXPERTO: ~w~n', [Resultado]),
    format('======================================================~n').

%% ==========================================
%% MÓDULO 4: PREVENCIÓN DE LAVADO DE ACTIVOS (AML DIFUSO + TEMPORALIDAD)
%% ==========================================

%% Regla AML: Detectar triangulación financiera considerando comisiones de mula y VELOCIDAD (Smurfing).
%% Condición: A -> B -> C -> A. Con montos considerables, margen de tolerancia y dentro de 72 horas (259200 segundos).

alerta_aml(Id, ToleranciaDecimal, 'LAVADO DE ACTIVOS (SMURFING DETECTADO)') :-
    transferencia(Id, B, Monto1, Ts1, _), Monto1 > 10000,
    transferencia(B, C, Monto2, _, _),
    transferencia(C, Id, Monto3, Ts3, _),
    Id \= B, B \= C, C \= Id,
    
    %% Temporalidad Estricta: La operacion debe cerrarse en menos de 72 horas
    DiferenciaSegundos is Ts3 - Ts1,
    DiferenciaSegundos =< 259200,
    DiferenciaSegundos >= 0,
    
    %% Logica Difusa: El dinero que regresa no es el 100% por comisiones.
    RetornoMinimo is Monto1 * (1.0 - ToleranciaDecimal),
    Monto3 >= RetornoMinimo,
    Monto3 =< Monto1,
    !,
    format('~n[XAI] ALERTA AML CRITICA: Triangulacion rapida detectada (Smurfing/U-Turn Laundering).~n'),
    format('[XAI] TEMPORALIDAD: Ciclo completado en menos de 72 horas (~w segundos).~n', [DiferenciaSegundos]),
    format('[XAI] TRAZA: Salio ~w a ~w. Luego paso por ~w. Finalmente regreso ~w a ~w.~n', [Monto1, B, C, Monto3, Id]),
    format('[XAI] PARAMETROS: Dentro del margen de tolerancia del ~2f%.~n', [ToleranciaDecimal * 100]).

%% Fallback
alerta_aml(_, _, 'SIN RIESGO DE LAVADO').

%% Predicado auxiliar para el Grafo Visual
traza_aml_nodos(Id, ToleranciaDecimal, B, C, Monto1, Monto2, Monto3) :-
    transferencia(Id, B, Monto1, Ts1, _), Monto1 > 10000,
    transferencia(B, C, Monto2, _, _),
    transferencia(C, Id, Monto3, Ts3, _),
    Id \= B, B \= C, C \= Id,
    DiferenciaSegundos is Ts3 - Ts1,
    DiferenciaSegundos =< 259200,
    DiferenciaSegundos >= 0,
    RetornoMinimo is Monto1 * (1.0 - ToleranciaDecimal),
    Monto3 >= RetornoMinimo,
    Monto3 =< Monto1,
    !.

%% ==========================================
%% MÓDULO 5: COMPLIANCE SBS E INSOLVENCIA DIFERENCIADA
%% ==========================================

intervencion_sbs(Id, 'RIESGO DE INSOLVENCIA (SBS - ACTIVO LIQUIDO)') :-
    tipo_patrimonio(Id, liquido),
    patrimonio(Id, Patrimonio),
    deuda_total(Id, Deuda),
    Umbral is Patrimonio * 5,
    Deuda > Umbral,
    !, format('~n[XAI] COMPLIANCE: Insolvencia por liquidez (>5x).~n').

intervencion_sbs(Id, 'RIESGO DE INSOLVENCIA (SBS - ACTIVO INMOBILIARIO)') :-
    tipo_patrimonio(Id, inmobiliario),
    patrimonio(Id, Patrimonio),
    deuda_total(Id, Deuda),
    Umbral is Patrimonio * 3,
    Deuda > Umbral,
    !, format('~n[XAI] COMPLIANCE: Insolvencia por riesgo inmobiliario (>3x).~n').

intervencion_sbs(_, 'SOLVENTE (CUMPLE POLITICAS DE RIESGO)').

%% ==========================================
%% MÓDULO 6: AUDITORÍA DE COBROS INDEBIDOS
%% ==========================================

auditoria_cobros(Id, 'COBRO INDEBIDO DETECTADO') :-
    tasa_acordada(Id, TAcordada),
    tasa_cobrada(Id, TCobrada),
    TCobrada > TAcordada,
    !,
    Diferencia is TCobrada - TAcordada,
    format('~n[XAI] AUDITORIA: Diferencia en contrato detectada.~n'),
    format('[XAI] TRAZA: Tasa cobrada (~w) es mayor a la acordada (~w). Diferencia: ~w.~n', [TCobrada, TAcordada, Diferencia]).

auditoria_cobros(_, 'CONTRATO LIMPIO').
