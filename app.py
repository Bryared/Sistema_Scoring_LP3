import streamlit as st

# 1. Configuración de la página
st.set_page_config(
    page_title="Dashboard Fintech XAI - UNALM",
    page_icon="🏦",
    layout="wide"
)

st.title("Dashboard Fintech XAI - UNALM 🏦")
st.markdown("Sistema Experto de Onboarding Dual mediante **IA Neuro-Simbólica**")

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
    st.sidebar.info("Este dashboard extrae métricas usando **Pyswip** y evalúa automáticamente en base a reglas del conocimiento lógico para explicar la rentabilidad/riesgo.")

    st.header(f"Expediente del Cliente: `{cliente_seleccionado}`")
    
    # 4. Visualización de Datos (Consultas a Prolog)
    try:
        # Pyswip retorna un Generator, lo pasamos a list() y extraemos el primer dicccionario
        q_ingresos = list(prolog.query(f"ingresos({cliente_seleccionado}, Monto)"))
        monto_ingreso = q_ingresos[0]["Monto"] if q_ingresos else "N/A"
        
        q_ip = list(prolog.query(f"ubicacion_ip({cliente_seleccionado}, Pais)"))
        pais_ip = q_ip[0]["Pais"] if q_ip else "N/A"
        
        q_intentos = list(prolog.query(f"intentos_login({cliente_seleccionado}, Intentos)"))
        intentos = q_intentos[0]["Intentos"] if q_intentos else "N/A"
        
        q_pago = list(prolog.query(f"pago_servicios({cliente_seleccionado}, Estado)"))
        # Pyswip puede devolver Atoms como objetos o encoded bytes, utilizamos decode/str
        estado_pago = str(q_pago[0]["Estado"]) if q_pago else "N/A"
        if isinstance(q_pago[0]["Estado"], bytes): estado_pago = q_pago[0]["Estado"].decode()
        
        q_antiguedad = list(prolog.query(f"antiguedad_laboral({cliente_seleccionado}, Meses)"))
        meses = q_antiguedad[0]["Meses"] if q_antiguedad else "N/A"
        
        q_billetera = list(prolog.query(f"billetera_digital({cliente_seleccionado}, Nivel)"))
        nivel_billetera = str(q_billetera[0]["Nivel"]) if q_billetera else "N/A"
        if isinstance(q_billetera[0]["Nivel"], bytes): nivel_billetera = q_billetera[0]["Nivel"].decode()
        
        st.subheader("Datos Capturados (Variables de Estado)")
        
        # Renderizar en Columnas
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Ubicación IP", pais_ip.capitalize())
            st.metric("Ingresos Mensuales", f"S/. {monto_ingreso}")
        with col2:
            st.metric("Intentos Login Inusuales", intentos)
            st.metric("Antigüedad Laboral", f"{meses} meses")
        with col3:
            st.metric("Pago de Servicios", estado_pago.capitalize())
            st.metric("Adopción Billetera Digital", nivel_billetera.capitalize())
            
        st.divider()

        # 5. Ejecución del Motor (Output)
        st.subheader("Motor de Inferencia Simbólica (XAI)")
        st.markdown("La tecnología inferencial validará los riesgos transaccionales y crediticios en tiempo real.")
        
        # Botón gigante
        if st.button("⚖️ Evaluar Riesgo (Onboarding)", type="primary", use_container_width=True):
            with st.spinner("El motor lógico está analizando las ramificaciones algorítmicas..."):
                 
                 # Consultar la regla maestra (dictamen_final/2)
                 query_result = list(prolog.query(f"dictamen_final({cliente_seleccionado}, Resultado)"))
                 
                 if query_result:
                     # Parsear del Atom a string
                     resultado_atom = query_result[0]["Resultado"]
                     resultado_str = str(resultado_atom)
                     if isinstance(resultado_atom, bytes): 
                         resultado_str = resultado_atom.decode()
                         
                     # Lógica de colores según resultado determinista
                     if "DENEGADO" in resultado_str or "RECHAZADO" in resultado_str:
                         st.error(f"### 🛑 {resultado_str}")
                         st.markdown("> **Nota XAI:** Verifique en consola para leer el árbol de trazabilidad. El sistema bloqueó transacciones inseguras para el perfil financiero.")
                     elif "APROBADO" in resultado_str:
                         st.success(f"### ✅ {resultado_str}")
                         st.markdown("> **Nota XAI:** Verifique en consola para leer el árbol de trazabilidad. El cliente representa rentabilidad positiva dentro de márgenes de adopción y fallback.")
                     else:
                         st.warning(f"### ⚠️ {resultado_str}")
                         st.markdown("> **Nota XAI:** Verifique en consola para leer el árbol de trazabilidad. El cliente requiere gestión de analistas para mitigar incertidumbres operativas o grises numéricos.")
                 else:
                     st.warning("El motor no encontró un predicado válido para este caso. Revisa la base de conocimiento.")
                     
    except Exception as query_error:
        st.error(f"Error realizando consultas/inferencias sobre Prolog. Detalle técnico: `{query_error}`")
