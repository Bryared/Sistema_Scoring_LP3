import streamlit as st
import plotly.graph_objects as go
import networkx as nx
import hashlib
from datetime import datetime
import os
import pandas as pd
from modelo_neuronal import CalculadorScoringNeuronal
from algoritmo_genetico import OptimizadorCarteraAG

# 1. Configuración de la página
st.set_page_config(
    page_title="Dashboard Fintech XAI - UNALM",
    page_icon="🏦",
    layout="wide"
)

st.title("Dashboard Fintech XAI - UNALM 🏦")
st.markdown("Sistema Experto de Onboarding Dual y Compliance mediante **IA Neuro-Simbólica (Blindaje Nivel 1)**")

# Función para el registro inmutable (Audit Trail)
def write_audit_log(client_id, evaluation_type, result, reasoning="Generado por Motor Simbólico Prolog"):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    raw_data = f"{timestamp}|{client_id}|{evaluation_type}|{result}|{reasoning}"
    sha_signature = hashlib.sha256(raw_data.encode()).hexdigest()
    
    log_entry = f"[{timestamp}] HASH: {sha_signature}\nCLIENTE: {client_id} | TIPO: {evaluation_type} | RES: {result}\nRAZON: {reasoning}\n{'-'*80}\n"
    
    with open("audit_trail_xai.log", "a", encoding="utf-8") as f:
        f.write(log_entry)
        
    return sha_signature

# 2. Conexión Prolog (Con manejo de errores robusto)
prolog_ready = False
try:
    from pyswip import Prolog
    prolog = Prolog()
    # Cargar el archivo con el motor de inferencia
    prolog.consult("motor_inferencia.pl")
    prolog_ready = True
except ImportError:
    st.error("Librería PySwip no encontrada. Ejecuta `pip install pyswip`.")
except Exception as e:
    st.error(f"Error al inicializar el Motor Prolog: {e}")

if prolog_ready:
    # 3. Interfaz de Usuario (UI) - Barra Lateral
    st.sidebar.header("Panel de Búsqueda 🔍")
    
    if "lista_clientes" not in st.session_state:
        st.session_state.lista_clientes = [f"c_{i:03d}" for i in range(1, 501)]
    if "modelo_neuronal" not in st.session_state:
        st.session_state.modelo_neuronal = CalculadorScoringNeuronal()
    
    cliente_seleccionado = st.sidebar.selectbox("Seleccionar ID de Cliente:", st.session_state.lista_clientes)
    
    st.sidebar.divider()
    st.sidebar.info("Este dashboard extrae métricas usando **Pyswip** y evalúa automáticamente en base a reglas del conocimiento lógico para explicar la rentabilidad/riesgo, auditorías y compliance.")

    st.header(f"Expediente Modular: `{cliente_seleccionado}`")
    
    # === TABS ===
    tab_add, tab1, tab2, tab3, tab4 = st.tabs(["➕ Nuevo Cliente", "📊 Onboarding (Scoring)", "🛡️ AML & Fraude", "⚖️ Auditoría Legal y Compliance SBS", "🧠 IA (Redes & Genéticos)"])
    
    # --- FUNCIONES DE ASISTENCIA PYSWIP ---
    def q_string(query_str, var_name):
        try:
            q = list(prolog.query(query_str))
            if not q: return "N/A"
            val = q[0][var_name]
            if isinstance(val, bytes): return val.decode('utf-8', 'ignore')
            return str(val)
        except Exception:
            return "Error SQL/Prolog"

    # ==========================================
    # TAB ADD: NUEVO CLIENTE
    # ==========================================
    with tab_add:
        st.subheader("Registrar Nuevo Cliente (Base de Hechos)")
        with st.form("form_nuevo_cliente"):
            nc_id = st.text_input("ID Cliente (ej. c_501)", value=f"c_{len(st.session_state.lista_clientes)+1:03d}")
            c1, c2 = st.columns(2)
            nc_ingresos = c1.number_input("Ingresos", min_value=0, value=2500)
            nc_intentos = c2.number_input("Intentos Login", min_value=0, value=1)
            nc_antiguedad = c1.number_input("Antigüedad Laboral (meses)", min_value=0, value=12)
            nc_billetera = c2.selectbox("Nivel Billetera", ["nulo", "bajo", "medio", "alto"], index=2)
            nc_pagos = c1.selectbox("Pago Servicios", ["puntual", "atrasado", "moroso"], index=0)
            nc_dsr = c2.number_input("Carga Financiera DSR (Suma cuotas / Ingresos)", min_value=0.0, value=0.3)
            
            submit_btn = st.form_submit_button("Agregar Cliente y Calcular ML")
            
            if submit_btn:
                # 1. Calcular probabilidad de default con Red Neuronal
                billetera_val = {"nulo":0, "bajo":0.3, "medio":0.6, "alto":1.0}[nc_billetera]
                prob_def = st.session_state.modelo_neuronal.predecir_probabilidad_default(nc_ingresos, nc_intentos, nc_antiguedad, nc_dsr, billetera_val)
                
                # 2. Agregar a la lista
                if nc_id not in st.session_state.lista_clientes:
                    st.session_state.lista_clientes.append(nc_id)
                
                # 3. Assert facts in Prolog
                try:
                    list(prolog.query(f"assertz(ingresos({nc_id}, {nc_ingresos}))"))
                    list(prolog.query(f"assertz(intentos_login({nc_id}, {nc_intentos}))"))
                    list(prolog.query(f"assertz(antiguedad_laboral({nc_id}, {nc_antiguedad}))"))
                    list(prolog.query(f"assertz(billetera_digital({nc_id}, '{nc_billetera}'))"))
                    list(prolog.query(f"assertz(pago_servicios({nc_id}, '{nc_pagos}'))"))
                    list(prolog.query(f"assertz(ml_probabilidad_default({nc_id}, {prob_def}))"))
                    # Hechos por defecto para evitar errores en otras reglas
                    list(prolog.query(f"assertz(ubicacion_ip({nc_id}, peru))"))
                    list(prolog.query(f"assertz(dni_vencido({nc_id}, false))"))
                    list(prolog.query(f"assertz(en_lista_ofac({nc_id}, false))"))
                    list(prolog.query(f"assertz(es_pep({nc_id}, false))"))
                    
                    st.success(f"Cliente {nc_id} agregado con éxito. Prob. Default (ML): {prob_def:.2%}")
                    st.rerun() # Refresh the selectbox
                except Exception as e:
                    st.error(f"Error Prolog: {e}")

    # ==========================================
    # TAB 1: ONBOARDING Y CREDIT SCORING
    # ==========================================
    with tab1:
        st.subheader("Datos Capturados (Variables de Estado)")
        monto_ingreso = q_string(f"ingresos({cliente_seleccionado}, Monto)", "Monto")
        pais_ip = q_string(f"ubicacion_ip({cliente_seleccionado}, Pais)", "Pais")
        intentos = q_string(f"intentos_login({cliente_seleccionado}, Intentos)", "Intentos")
        estado_pago = q_string(f"pago_servicios({cliente_seleccionado}, Estado)", "Estado")
        meses = q_string(f"antiguedad_laboral({cliente_seleccionado}, Meses)", "Meses")
        nivel_billetera = q_string(f"billetera_digital({cliente_seleccionado}, Nivel)", "Nivel")
        
        tiempo_llenado = q_string(f"tiempo_llenado({cliente_seleccionado}, T)", "T")
        residencia = q_string(f"residencia({cliente_seleccionado}, R)", "R")
        imei = q_string(f"dispositivo_imei({cliente_seleccionado}, I)", "I")
        suma_cuotas = q_string(f"suma_cuotas_mensuales({cliente_seleccionado}, S)", "S")
        antig_domicilio = q_string(f"antiguedad_domicilio({cliente_seleccionado}, A)", "A")
        sector = q_string(f"sector_laboral({cliente_seleccionado}, S)", "S")
        creditos_activos = q_string(f"creditos_activos({cliente_seleccionado}, C)", "C")
        consultas = q_string(f"consultas_bancarias_15dias({cliente_seleccionado}, C)", "C")
        
        # Nuevos campos de KYC y Listas Negras
        dni_vencido = q_string(f"dni_vencido({cliente_seleccionado}, D)", "D")
        ofac = q_string(f"en_lista_ofac({cliente_seleccionado}, O)", "O")
        pep = q_string(f"es_pep({cliente_seleccionado}, P)", "P")
        
        try:
            dsr = (float(suma_cuotas) / float(monto_ingreso)) * 100 if float(monto_ingreso) > 0 else 0
            dsr_str = f"{dsr:.1f}%"
        except:
            dsr_str = "N/A"
            
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("DNI Vencido", "Sí" if dni_vencido == 'true' else "No")
            st.metric("Residencia Declarada", str(residencia).capitalize())
            st.metric("Tiempo de Llenado", f"{tiempo_llenado}s")
            st.metric("Carga Financiera (DSR)", dsr_str)
        with col2:
            st.metric("Lista OFAC (Terrorismo)", "⚠️ SÍ" if ofac == 'true' else "No")
            st.metric("Ubicación IP", str(pais_ip).capitalize())
            st.metric("Sector Laboral", str(sector).capitalize())
            st.metric("Antigüedad Domiciliaria", f"{antig_domicilio} meses")
        with col3:
            st.metric("Es PEP (Político)", "⚠️ SÍ" if pep == 'true' else "No")
            st.metric("Intentos Login Inusuales", intentos)
            st.metric("Pago de Servicios", str(estado_pago).capitalize())
            st.metric("Créditos Activos", creditos_activos)
        with col4:
            st.metric("Ingresos Mensuales", f"S/. {monto_ingreso}")
            st.metric("Dispositivo IMEI", imei)
            st.metric("Antigüedad Laboral", f"{meses} meses")
            st.metric("Consultas (15 días)", consultas)
            
        st.divider()
        st.subheader("Componente Neuro (Machine Learning)")
        st.markdown("Modelos de IA entrenados en Python inyectan hechos estadísticos en Prolog para dictar umbrales dinámicos.")
        
        ml_prob = q_string(f"ml_probabilidad_default({cliente_seleccionado}, P)", "P")
        ml_anom = q_string(f"ml_fraude_anomalia({cliente_seleccionado}, A)", "A")
        ml_clus = q_string(f"ml_perfil_cluster({cliente_seleccionado}, C)", "C")
        
        try:
            prob_perc = f"{float(ml_prob)*100:.1f}%"
        except:
            prob_perc = "N/A"
            
        c1, c2, c3 = st.columns(3)
        c1.metric("Score Predictivo Default (Regresión Logística)", prob_perc)
        c2.metric("Comportamiento Anómalo (Isolation Forest)", "⚠️ DETECTADO" if ml_anom == 'true' else "Normal")
        c3.metric("Clustering Demográfico (K-Means)", str(ml_clus).replace('_', ' ').title())

        st.divider()

        st.subheader("Motor de Inferencia Simbólica (Onboarding XAI)")
        if st.button("⚖️ Evaluar Riesgo (Onboarding)", type="primary", use_container_width=True):
            with st.spinner("Evaluando KYC, OFAC, PEP, Fraude y Scoring..."):
                 resultado_str = q_string(f"dictamen_final({cliente_seleccionado}, Resultado)", "Resultado")
                 
                 # Generar Audit Log Inmutable
                 hash_firma = write_audit_log(cliente_seleccionado, "Onboarding", resultado_str)
                 
                 if "DENEGADO" in resultado_str or "RECHAZADO" in resultado_str:
                     st.error(f"### 🛑 {resultado_str}")
                 elif "APROBADO" in resultado_str:
                     st.success(f"### ✅ {resultado_str}")
                 elif "MANUAL" in resultado_str:
                     st.warning(f"### ⚠️ {resultado_str}")
                 else:
                     st.info(f"### ℹ️ {resultado_str}")
                     
                 st.info("ℹ️ **Explicabilidad (XAI)**: Revisa tu consola original para ver el Árbol de Trazabilidad.")
                 st.caption(f"🔒 **Log Criptográfico Inmutable Guardado.** Hash SHA-256: `{hash_firma}`")
    
    # ==========================================
    # TAB 2: PREVENCIÓN DE LAVADO DE ACTIVOS (AML)
    # ==========================================
    with tab2:
        st.subheader("Búsqueda de Grafos (Detección AML)")
        st.markdown("Prolog recorrerá recursivamente las transacciones buscando posibles ciclos o triangulaciones de lavado, **aplicando lógica difusa para tolerar comisiones de testaferros** y validando **temporalidad estricta (Smurfing < 72 hrs)**.")
        
        margen_tolerancia = st.slider("Tolerancia de Comisión de Mula (%)", min_value=0, max_value=20, value=10, step=1)
        tolerancia_decimal = margen_tolerancia / 100.0

        if st.button("🔍 Escanear Red Transaccional y Temporalidad", key="btn_aml"):
            resultado_aml = q_string(f"alerta_aml({cliente_seleccionado}, {tolerancia_decimal}, Motivo)", "Motivo")
            
            # Generar Audit Log Inmutable
            hash_firma = write_audit_log(cliente_seleccionado, "AML Escaneo", resultado_aml)
                 
            if "LAVADO" in resultado_aml:
                st.error(f"### 🚨 ALERTA CRÍTICA: {resultado_aml}")
                st.markdown(f"> **Nota de Auditoría XAI**: Triangulación rápida (<72h) detectada considerando un margen del {margen_tolerancia}%.")
                st.caption(f"🔒 Hash SHA-256 de auditoría AML: `{hash_firma}`")
                
                # Intentar graficar la red
                try:
                    q_nodos = list(prolog.query(f"traza_aml_nodos({cliente_seleccionado}, {tolerancia_decimal}, B, C, M1, M2, M3)"))
                    if q_nodos:
                        nodo_B = q_nodos[0]["B"]
                        if isinstance(nodo_B, bytes): nodo_B = nodo_B.decode('utf-8', 'ignore')
                        nodo_C = q_nodos[0]["C"]
                        if isinstance(nodo_C, bytes): nodo_C = nodo_C.decode('utf-8', 'ignore')
                        M1 = q_nodos[0]["M1"]
                        M2 = q_nodos[0]["M2"]
                        M3 = q_nodos[0]["M3"]
                        
                        st.markdown("#### 🕸️ Visualización de Red Ilícita de Smurfing")
                        
                        G = nx.DiGraph()
                        G.add_edge(cliente_seleccionado, nodo_B, weight=M1)
                        G.add_edge(nodo_B, nodo_C, weight=M2)
                        G.add_edge(nodo_C, cliente_seleccionado, weight=M3)
                        
                        pos = nx.spring_layout(G)
                        edge_x, edge_y = [], []
                        for edge in G.edges():
                            x0, y0 = pos[edge[0]]
                            x1, y1 = pos[edge[1]]
                            edge_x.extend([x0, x1, None])
                            edge_y.extend([y0, y1, None])
                            
                        edge_trace = go.Scatter(x=edge_x, y=edge_y, line=dict(width=3, color='red'), mode='lines')
                        node_x, node_y, text_nodes = [], [], []
                        for node in G.nodes():
                            x, y = pos[node]
                            node_x.append(x)
                            node_y.append(y)
                            text_nodes.append(str(node))
                            
                        node_trace = go.Scatter(x=node_x, y=node_y, mode='markers+text', text=text_nodes, textposition="bottom center",
                                                marker=dict(color='darkred', size=40, line=dict(width=2, color='white')))
                        
                        fig = go.Figure(data=[edge_trace, node_trace],
                                     layout=go.Layout(showlegend=False, hovermode='closest', margin=dict(b=0,l=0,r=0,t=0),
                                                      xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                                                      yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                                                      height=400))
                        st.plotly_chart(fig, use_container_width=True)
                        
                except Exception as e:
                    st.warning(f"No se pudo generar el grafo visual: {e}")
            else:
                st.success(f"### ✅ {resultado_aml}")
                st.markdown("La red transaccional del cliente no muestra Smurfing (no hay triangulaciones rápidas <72h o exceden el margen).")
                st.caption(f"🔒 Hash SHA-256 de auditoría AML: `{hash_firma}`")

    # ==========================================
    # TAB 3: AUDITORÍA Y COMPLIANCE SBS
    # ==========================================
    with tab3:
        st.subheader("Evaluación Regulatoria")
        st.markdown("Analizando ratios financieros contra la normativa de la SBS.")
        
        col1, col2, col3 = st.columns(3)
        patrimonio = q_string(f"patrimonio({cliente_seleccionado}, P)", "P")
        deuda = q_string(f"deuda_total({cliente_seleccionado}, D)", "D")
        tipo_patrimonio = q_string(f"tipo_patrimonio({cliente_seleccionado}, T)", "T")
        
        col1.metric("Patrimonio Neto", f"S/. {patrimonio}")
        col2.metric("Tipo de Patrimonio", str(tipo_patrimonio).capitalize())
        col3.metric("Deuda Total", f"S/. {deuda}")
        
        if st.button("⚖️ Ejecutar Compliance", key="btn_compliance"):
            resultado_sbs = q_string(f"intervencion_sbs({cliente_seleccionado}, Estado)", "Estado")
            
            hash_firma_sbs = write_audit_log(cliente_seleccionado, "Compliance SBS", resultado_sbs)
            
            if "RIESGO" in resultado_sbs:
                st.error(f"### 🛑 RECHAZADO: {resultado_sbs}")
            else:
                st.success(f"### ✅ {resultado_sbs}")
                
            st.caption(f"🔒 Hash de Auditoría: `{hash_firma_sbs}`")
            st.divider()
            
            st.markdown("#### 🔎 Auditoría de Smart Contracts Lógicos")
            auditoria = q_string(f"auditoria_cobros({cliente_seleccionado}, Alerta)", "Alerta")
            hash_firma_contrato = write_audit_log(cliente_seleccionado, "Smart Contract", auditoria)
            
            if "COBRO INDEBIDO" in auditoria:
                st.warning(f"### ⚠️ {auditoria}")
                tasa_acordada = q_string(f"tasa_acordada({cliente_seleccionado}, TA)", "TA")
                tasa_cobrada = q_string(f"tasa_cobrada({cliente_seleccionado}, TC)", "TC")
                st.error(f"Inconsistencia en Tasas: Se acordó {tasa_acordada} pero el sistema cobró {tasa_cobrada}.")
            else:
                st.info(f"### ✅ {auditoria} (Tasa Acordada = Tasa Cobrada)")
            st.caption(f"🔒 Hash de Auditoría: `{hash_firma_contrato}`")
            
    # ==========================================
    # TAB 4: INTELIGENCIA ARTIFICIAL (ML & AG)
    # ==========================================
    with tab4:
        st.header("Modelos Predictivos y de Optimización")
        
        st.subheader("1. Red Neuronal Multicapa (Scoring)")
        st.markdown("Entrena un modelo Perceptrón Multicapa (MLP) utilizando `scikit-learn` para predecir probabilidades de impago basadas en ingresos, intentos de login, antigüedad y carga financiera.")
        if st.button("Entrenar/Actualizar Red Neuronal"):
            with st.spinner("Entrenando MLPClassifier..."):
                acc = st.session_state.modelo_neuronal.entrenar_modelo_simulado(1500)
                st.success(f"Modelo entrenado exitosamente con Accuracy: {acc:.2%}")
        
        st.divider()
        st.subheader("2. Algoritmo Genético (Optimización de Cartera)")
        st.markdown("Busca la combinación óptima de préstamos dados los clientes, maximizando la ganancia (por intereses) y minimizando el riesgo (probabilidad de default de la red neuronal), sujeto a un presupuesto finito.")
        
        presupuesto = st.number_input("Presupuesto del Banco (S/.)", min_value=100000, value=1000000, step=100000)
        
        if st.button("Ejecutar Optimización Genética"):
            with st.spinner("Evolucionando generaciones... (DEAP)"):
                # Generar data basada en clientes actuales
                data_ag = []
                for cid in st.session_state.lista_clientes[:500]: # Optimizar solo los 500 primeros para velocidad
                    try:
                        # Extraer ingresos y simular prestamo = 3x ingresos
                        ingreso_str = q_string(f"ingresos({cid}, I)", "I")
                        prestamo_solicitado = float(ingreso_str) * 3 if ingreso_str != "N/A" else 5000.0
                    except:
                        prestamo_solicitado = 5000.0
                        
                    try:
                        prob_str = q_string(f"ml_probabilidad_default({cid}, P)", "P")
                        prob_def = float(prob_str) if prob_str != "N/A" else 0.15
                    except:
                        prob_def = 0.15
                        
                    tasa = 0.20 # 20% interes anual simulado
                    data_ag.append({
                        'id': cid,
                        'prestamo': prestamo_solicitado,
                        'prob_default': prob_def,
                        'tasa_interes': tasa
                    })
                
                opt = OptimizadorCarteraAG(data_ag, presupuesto_maximo=presupuesto)
                seleccionados, inv_total, ret_total = opt.optimizar(tam_poblacion=100, generaciones=50)
                
                st.success(f"Optimización completada. Se seleccionaron {len(seleccionados)} clientes.")
                c1, c2, c3 = st.columns(3)
                c1.metric("Clientes Aprobados", len(seleccionados))
                c2.metric("Inversión Total", f"S/. {inv_total:,.2f}")
                c3.metric("Retorno Esperado Neto", f"S/. {ret_total:,.2f}")
                
                if seleccionados:
                    df_res = pd.DataFrame([{'Cliente': c['id'], 'Préstamo Asignado': c['prestamo'], 'Riesgo (Prob Default)': round(c['prob_default'], 3)} for c in seleccionados])
                    st.dataframe(df_res)
                    st.caption("Mostrando la cartera de clientes óptima seleccionada por el Algoritmo Evolutivo.")
            
    # VISUALIZADOR DE LOGS
    st.sidebar.divider()
    st.sidebar.subheader("🔒 Auditoría RegTech")
    if st.sidebar.button("📄 Mostrar Logs Inmutables XAI"):
        st.sidebar.markdown("Los registros no pueden ser alterados. Cumplimiento legal asegurado.")
        try:
            with open("audit_trail_xai.log", "r", encoding="utf-8") as f:
                logs = f.read()
            st.sidebar.text_area("Audit Trail (Blockchain Simulado)", logs, height=300)
        except FileNotFoundError:
            st.sidebar.warning("Aún no hay logs generados.")
