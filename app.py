import streamlit as st
import pandas as pd
import urllib.parse

# 1. Configuración de la página
st.set_page_config(
    page_title="AutoLum LED | Iluminación Automotriz",
    page_icon="💡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. Estilos CSS personalizados (Estética Automotriz Dark + Neón)
st.markdown("""
<style>
    /* Tarjetas de productos */
    .product-card {
        background-color: #1a1c23;
        border: 1px solid #2d303e;
        border-radius: 12px;
        padding: 18px;
        margin-bottom: 20px;
        transition: transform 0.2s ease, border-color 0.2s ease;
    }
    .product-card:hover {
        transform: translateY(-5px);
        border-color: #ff9900;
        box-shadow: 0 6px 15px rgba(255, 153, 0, 0.15);
    }
    .price-tag {
        color: #00e676;
        font-size: 1.4rem;
        font-weight: 800;
        margin: 10px 0;
    }
    .badge {
        background-color: #ff9900;
        color: #000000;
        padding: 3px 10px;
        border-radius: 6px;
        font-size: 0.75rem;
        font-weight: bold;
        display: inline-block;
        margin-bottom: 8px;
    }
    .spec-text {
        color: #a0a6b5;
        font-size: 0.9rem;
        margin: 3px 0;
    }
    /* Botón de WhatsApp */
    .btn-wa {
        display: block;
        width: 100%;
        text-align: center;
        background-color: #25D366;
        color: #ffffff !important;
        padding: 10px;
        border-radius: 8px;
        text-decoration: none;
        font-weight: bold;
        margin-top: 12px;
        transition: background-color 0.2s;
    }
    .btn-wa:hover {
        background-color: #1ebe57;
    }
    /* Banner Principal */
    .hero-banner {
        background: linear-gradient(90deg, #111318 0%, #1f2430 100%);
        border-left: 5px solid #ff9900;
        padding: 25px;
        border-radius: 10px;
        margin-bottom: 25px;
    }
</style>
""", unsafe_allow_html=True)

# Configura aquí el número de WhatsApp del negocio (con código de país, sin el +)
WHATSAPP_NUM = "573000000000"

# 3. Base de datos simulada (Luego la podemos conectar a un Excel/CSV o SQL)
@st.cache_data
def cargar_catalogo():
    datos = [
        {"id": 1, "nombre": "Kit Turbo LED C6 12.000 LM", "vehiculo": "Carro", "socket": "H4", "lumenes": "12,000 LM", "color": "6000K (Blanco Frío)", "precio": 85000, "garantia": "6 meses"},
        {"id": 2, "nombre": "Bombillo LED Proyector Mini Lupa", "vehiculo": "Moto", "socket": "H4", "lumenes": "16,000 LM", "color": "6000K / 3000K (Dual)", "precio": 65000, "garantia": "6 meses"},
        {"id": 3, "nombre": "Exploradoras LED Doble Color Auxiliares", "vehiculo": "Ambos", "socket": "Universal", "lumenes": "10,000 LM", "color": "Blanco + Ámbar (Antiniebla)", "precio": 110000, "garantia": "1 año"},
        {"id": 4, "nombre": "Kit LED Canbus CSP Ultra Potente", "vehiculo": "Carro", "socket": "H7", "lumenes": "22,000 LM", "color": "6500K (Blanco Puro)", "precio": 160000, "garantia": "1 año"},
        {"id": 5, "nombre": "Ojo de Ángel LED + Exploradora", "vehiculo": "Moto", "socket": "Universal", "lumenes": "8,000 LM", "color": "Blanco + Aro Azul/Rojo", "precio": 48000, "garantia": "3 meses"},
        {"id": 6, "nombre": "Cocuyos LED T10 Canbus Siliconados (Par)", "vehiculo": "Ambos", "socket": "T10", "lumenes": "800 LM", "color": "Blanco / Azul Hielo", "precio": 15000, "garantia": "3 meses"},
    ]
    return pd.DataFrame(datos)

df_productos = cargar_catalogo()

# 4. Barra Lateral (Filtros rápidos)
with st.sidebar:
    st.title("🔧 Filtros de Búsqueda")
    st.write("Encuentra la referencia exacta para tu vehículo:")
    
    filtro_vehiculo = st.radio(
        "Tipo de Vehículo:",
        ["Todos", "Carro", "Moto"],
        index=0
    )
    
    sockets_disponibles = ["Todos"] + sorted(list(df_productos["socket"].unique()))
    filtro_socket = st.selectbox("Tipo de Conector (Socket):", sockets_disponibles)
    
    rango_precio = st.slider(
        "Presupuesto máximo ($ COP):",
        min_value=10000,
        max_value=250000,
        value=250000,
        step=10000,
        format="$%d"
    )
    
    st.divider()
    st.caption("📍 Envíos a todo el país e instalación garantizada.")

# 5. Cabecera Principal (Hero Banner)
st.markdown("""
<div class="hero-banner">
    <h1 style="margin:0; color:#ffffff;">⚡ AUTOLUM LED</h1>
    <p style="color:#ff9900; font-size:1.1rem; margin-top:5px; margin-bottom:0;">
        Especialistas en Iluminación Automotriz para Carros y Motocicletas
    </p>
</div>
""", unsafe_allow_html=True)

# 6. Navegación por Pestañas
tab_catalogo, tab_compatibilidad, tab_contacto = st.tabs([
    "🛒 Catálogo de Luces", 
    "🔍 ¿Qué bombillo usa mi vehículo?", 
    "📲 Instalación y Contacto"
])

# --- PESTAÑA 1: CATÁLOGO ---
with tab_catalogo:
    # Lógica de filtrado
    df_filtrado = df_productos.copy()
    
    if filtro_vehiculo == "Carro":
        df_filtrado = df_filtrado[df_filtrado["vehiculo"].isin(["Carro", "Ambos"])]
    elif filtro_vehiculo == "Moto":
        df_filtrado = df_filtrado[df_filtrado["vehiculo"].isin(["Moto", "Ambos"])]
        
    if filtro_socket != "Todos":
        df_filtrado = df_filtrado[df_filtrado["socket"] == filtro_socket]
        
    df_filtrado = df_filtrado[df_filtrado["precio"] <= rango_precio]

    st.subheader(f"Productos disponibles ({len(df_filtrado)})")
    
    if df_filtrado.empty:
        st.warning("No encontramos luces con esos filtros exactos. Intenta ampliar el rango de precio o cambiar el conector.")
    else:
        # Mostrar en cuadrícula de 3 columnas
        columnas = st.columns(3)
        for idx, (_, prod) in enumerate(df_filtrado.iterrows()):
            with columnas[idx % 3]:
                # Crear enlace de WhatsApp personalizado por producto
                mensaje_wa = f"Hola! Me interesa el *{prod['nombre']}* (Conector {prod['socket']}) de ${prod['precio']:,.0f}."
                url_wa = f"https://wa.me/{WHATSAPP_NUM}?text={urllib.parse.quote(mensaje_wa)}"
                
                st.markdown(f"""
                <div class="product-card">
                    <span class="badge">{prod['vehiculo'].upper()} | Socket: {prod['socket']}</span>
                    <h4 style="margin: 5px 0 10px 0; color: #ffffff;">{prod['nombre']}</h4>
                    <p class="spec-text">🔆 <b>Potencia:</b> {prod['lumenes']}</p>
                    <p class="spec-text">🎨 <b>Tono:</b> {prod['color']}</p>
                    <p class="spec-text">🛡️ <b>Garantía:</b> {prod['garantia']}</p>
                    <div class="price-tag">${prod['precio']:,.0f} COP</div>
                    <a href="{url_wa}" target="_blank" class="btn-wa">💬 Pedir por WhatsApp</a>
                </div>
                """, unsafe_allow_html=True)

# --- PESTAÑA 2: BUSCADOR DE COMPATIBILIDAD ---
with tab_compatibilidad:
    st.subheader("Guía rápida de conectores (Sockets)")
    st.write("Si no sabes qué referencia de bombillo usa tu carro o moto, consulta esta tabla rápida o escríbenos:")
    
    col_guia1, col_guia2 = st.columns(2)
    with col_guia1:
        st.info("""
        **🚗 Automóviles comunes:**
        * **Chevrolet Spark / Sail / Aveo:** H4 (Bajas y Altas en el mismo bombillo)
        * **Renault Logan / Sandero / Duster:** H7 (Bajas) y H1 (Altas)
        * **Mazda 2 / Mazda 3:** H11 (Bajas) y HB3/9005 (Altas)
        * **Kia Picanto / Rio:** H4 o H7 (según modelo/año)
        """)
    with col_guia2:
        st.info("""
        **🏍️ Motocicletas comunes:**
        * **Bajaj Pulsar NS200 / Dominar:** H4
        * **Yamaha FZ / MT-03 / R15:** H4 / H7
        * **Honda CB 190R / XR 150:** H4
        * **AKT NKD 125 / TTR:** H4 / BA20D
        """)

# --- PESTAÑA 3: CONTACTO Y COTIZACIÓN ---
with tab_contacto:
    col_form, col_info = st.columns([3, 2])
    
    with col_form:
        st.subheader("Solicitar Cotización o Agendar Instalación")
        with st.form("form_cotizacion"):
            nombre_cliente = st.text_input("Tu Nombre:")
            modelo_vehiculo = st.text_input("Marca, Modelo y Año de tu Carro/Moto (Ej: Mazda 3 2018 o Pulsar NS 200):")
            tipo_servicio = st.selectbox("¿Qué estás buscando?", [
                "Solo comprar las luces (Envío a domicilio)",
                "Compra + Instalación en punto físico",
                "Asesoría porque no sé cuál le sirve a mi vehículo"
            ])
            notas = st.text_area("Detalles adicionales (¿Buscas luz blanca, amarilla antiniebla, exploradoras?):")
            
            enviado = st.form_submit_button("Generar solicitud para WhatsApp")
            
            if enviado:
                if nombre_cliente and modelo_vehiculo:
                    msg_cot = f"Hola! Soy *{nombre_cliente}*. Tengo un *{modelo_vehiculo}*. Busco: {tipo_servicio}. Detalles: {notas}"
                    link_cot = f"https://wa.me/{WHATSAPP_NUM}?text={urllib.parse.quote(msg_cot)}"
                    st.success("¡Solicitud lista! Haz clic en el botón de abajo para enviarla a nuestro WhatsApp:")
                    st.markdown(f'<a href="{link_cot}" target="_blank" class="btn-wa">📲 Enviar datos por WhatsApp</a>', unsafe_allow_html=True)
                else:
                    st.error("Por favor ingresa al menos tu nombre y el modelo de tu vehículo.")
                    
    with col_info:
        st.subheader("¿Por qué elegir nuestras luces LED?")
        st.markdown("""
        * ✅ **No encandilan:** Corte de luz definido para no molestar a otros conductores.
        * ✅ **Sistema Canbus:** Evita testigos de error en el tablero en carros modernos.
        * ✅ **Disipación Térmica:** Ventiladores silenciosos de alta revolución y cuerpo en aluminio de aviación.
        * ✅ **Resistencia al agua:** Certificación IP67 / IP68 (ideales para lluvia fuerte en moto o carro).
        """)
