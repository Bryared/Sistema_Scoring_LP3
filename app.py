import streamlit as st

# 1. Configuración de la página
st.set_page_config(
    page_title="Dashboard Fintech XAI - UNALM",
    page_icon="🏦",
    layout="wide"
)

st.title("Dashboard Fintech XAI - UNALM 🏦")
st.markdown("Sistema Experto de Onboarding Dual y Compliance mediante **IA Neuro-Simbólica**")

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
    st.warning("""
    **Solución posible:** PySwip requiere que de SWI-Prolog esté instalado y añadido al **PATH** de Windows.
    Si acabas de instalar SWI-Prolog, puede que necesites cerrar la terminal y/o el editor e iniciarlos nuevamente 
    para que se refresquen las variables de entorno.
    """)

if prolog_ready:
    # 3. Interfaz de Usuario (UI) - Barra Lateral
    st.sidebar.header("Panel de Búsqueda 🔍")
    
    # Generar la lista de los 500 clientes (c_001 al c_500)
    lista_clientes = [f"c_{i:03d}" for i in range(1, 501)]
    cliente_seleccionado = st.sidebar.selectbox("Seleccionar ID de Cliente:", lista_clientes)
    
    st.sidebar.divider()
    st.sidebar.info("Este dashboard extrae métricas usando **Pyswip** y evalúa automáticamente en base a reglas del conocimiento lógico para explicar la rentabilidad/riesgo, auditorías y compliance.")

    st.header(f"Expediente Modular: `{cliente_seleccionado}`")
    
    # === TABS ===
    tab1, tab2, tab3 = st.tabs(["📊 Onboarding (Scoring)", "🛡️ AML & Riesgo", "⚖️ Auditoría y Compliance SBS"])
    
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
    # TAB 1: ONBOARDING Y CREDIT SCORING
    # ==========================================
    with tab1:
        st.subheader("Datos Capturados (Variables de Estado)")
        # Extracción de datos básicos
        monto_ingreso = q_string(f"ingresos({cliente_seleccionado}, Monto)", "Monto")
        pais_ip = q_string(f"ubicacion_ip({cliente_seleccionado}, Pais)", "Pais")
        intentos = q_string(f"intentos_login({cliente_seleccionado}, Intentos)", "Intentos")
        estado_pago = q_string(f"pago_servicios({cliente_seleccionado}, Estado)", "Estado")
        meses = q_string(f"antiguedad_laboral({cliente_seleccionado}, Meses)", "Meses")
        nivel_billetera = q_string(f"billetera_digital({cliente_seleccionado}, Nivel)", "Nivel")
        
        # Renderizar en Columnas
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Ubicación IP", str(pais_ip).capitalize())
            st.metric("Ingresos Mensuales", f"S/. {monto_ingreso}")
        with col2:
            st.metric("Intentos Login Inusuales", intentos)
            st.metric("Antigüedad Laboral", f"{meses} meses")
        with col3:
            st.metric("Pago de Servicios", str(estado_pago).capitalize())
            st.metric("Adopción Billetera Digital", str(nivel_billetera).capitalize())
            
        st.divider()

        st.subheader("Motor de Inferencia Simbólica (Onboarding XAI)")
        if st.button("⚖️ Evaluar Riesgo (Onboarding)", type="primary", use_container_width=True):
            with st.spinner("El motor lógico está analizando..."):
                 resultado_str = q_string(f"dictamen_final({cliente_seleccionado}, Resultado)", "Resultado")
                 
                 if "DENEGADO" in resultado_str or "RECHAZADO" in resultado_str:
                     st.error(f"### 🛑 {resultado_str}")
                 elif "APROBADO" in resultado_str:
                     st.success(f"### ✅ {resultado_str}")
                 elif resultado_str == "Error SQL/Prolog" or resultado_str == "N/A":
                     st.warning("El motor no encontró un predicado válido para este caso.")
                 else:
                     st.warning(f"### ⚠️ {resultado_str}")
                 st.info("ℹ️ **Explicabilidad (XAI)**: Revisa tu consola original para ver el Árbol de Trazabilidad generado por Prolog.")
    
    # ==========================================
    # TAB 2: PREVENCIÓN DE LAVADO DE ACTIVOS (AML)
    # ==========================================
    with tab2:
        st.subheader("Búsqueda de Grafos (Detección AML)")
        st.markdown("Prolog recorrerá recursivamente las transacciones buscando posibles ciclos o triangulaciones de lavado.")
        
        if st.button("🔍 Escanear Red Transaccional", key="btn_aml"):
            resultado_aml = q_string(f"alerta_aml({cliente_seleccionado}, Motivo)", "Motivo")
            if "LAVADO" in resultado_aml:
                st.error(f"### 🚨 ALERTA CRÍTICA: {resultado_aml}")
                st.markdown("> **Nota de Auditoría XAI**: Triangulación circular de 3 saltos detectada superior a S/10,000. Revisa la consola original para ver la traza exacta.")
            else:
                st.success(f"### ✅ {resultado_aml}")
                st.markdown("La red transaccional del cliente no muestra triangulaciones ilegales aparentes.")

    # ==========================================
    # TAB 3: AUDITORÍA Y COMPLIANCE SBS
    # ==========================================
    with tab3:
        st.subheader("Evaluación Regulatoria")
        st.markdown("Analizando ratios financieros contra la normativa de la SBS.")
        
        col1, col2 = st.columns(2)
        patrimonio = q_string(f"patrimonio({cliente_seleccionado}, P)", "P")
        deuda = q_string(f"deuda_total({cliente_seleccionado}, D)", "D")
        
        col1.metric("Patrimonio Neto", f"S/. {patrimonio}")
        col2.metric("Deuda Total", f"S/. {deuda}")
        
        if st.button("⚖️ Ejecutar Compliance", key="btn_compliance"):
            resultado_sbs = q_string(f"intervencion_sbs({cliente_seleccionado}, Estado)", "Estado")
            if "RIESGO" in resultado_sbs:
                st.error(f"### 🛑 RECHAZADO: {resultado_sbs}")
                st.markdown("> **Alerta**: El cliente tiene una Deuda que supera 3 veces su Patrimonio (Insolvencia Técnica).")
            else:
                st.success(f"### ✅ {resultado_sbs}")
                
            st.divider()
            
            # Sub-sección: Auditoría de Cobros (Contratos)
            st.markdown("#### 🔎 Auditoría de Smart Contracts Lógicos")
            auditoria = q_string(f"auditoria_cobros({cliente_seleccionado}, Alerta)", "Alerta")
            
            if "COBRO INDEBIDO" in auditoria:
                st.warning(f"### ⚠️ {auditoria}")
                tasa_acordada = q_string(f"tasa_acordada({cliente_seleccionado}, TA)", "TA")
                tasa_cobrada = q_string(f"tasa_cobrada({cliente_seleccionado}, TC)", "TC")
                st.error(f"Inconsistencia en Tasas: Se acordó {tasa_acordada} pero el sistema cobró {tasa_cobrada}.")
            else:
                st.info(f"### ✅ {auditoria} (Tasa Acordada = Tasa Cobrada)")
