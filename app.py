import streamlit as st
import pandas as pd
import urllib.parse
import os

# 1. Configuración de la página
st.set_page_config(
    page_title="JV AUTO LED | Iluminación Automotriz",
    page_icon="💡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. Estilos CSS con Tipografía Moderna (Google Fonts: Outfit / Inter) y Estética Automotriz
st.markdown("""
<import url='https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Outfit:wght@400;600;800;900&display=swap'>
<style>
    /* Aplicar la tipografía moderna a toda la aplicación */
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
        background-color: #0e1117;
        color: #fafafa;
    }

    /* Forzar tipografía geométrica moderna en títulos y encabezados */
    h1, h2, h3, h4, h5, h6, .stSubheader {
        font-family: 'Outfit', sans-serif !important;
    }
    
    /* Contenedor del Banner con Imagen */
    .banner-container {
        text-align: center;
        background: linear-gradient(135deg, #11141d 0%, #1a1f2c 50%, #11141d 100%);
        border: 1px solid #2a3042;
        border-radius: 16px;
        padding: 20px;
        margin-bottom: 30px;
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.4);
    }

    /* Tarjetas de productos estilizadas */
    .product-card {
        background-color: #161922;
        border: 1px solid #262b3a;
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 20px;
        transition: transform 0.2s ease, border-color 0.2s ease;
    }
    .product-card:hover {
        transform: translateY(-4px);
        border-color: #ff9900;
        box-shadow: 0 6px 20px rgba(255, 153, 0, 0.15);
    }
    .price-tag {
        color: #00e676;
        font-size: 1.4rem;
        font-weight: 800;
        font-family: 'Outfit', sans-serif;
        margin: 10px 0;
    }
    .badge {
        background-color: #ff9900;
        color: #000000;
        padding: 4px 10px;
        border-radius: 6px;
        font-size: 0.75rem;
        font-weight: 800;
        display: inline-block;
        margin-bottom: 8px;
        text-transform: uppercase;
        font-family: 'Outfit', sans-serif;
    }
    .spec-text {
        color: #9da3af;
        font-size: 0.9rem;
        margin: 4px 0;
    }
    
    /* Botón de WhatsApp */
    .btn-wa {
        display: block;
        width: 100%;
        text-align: center;
        background-color: #25D366;
        color: #ffffff !important;
        padding: 11px;
        border-radius: 8px;
        text-decoration: none;
        font-weight: 700;
        font-family: 'Inter', sans-serif;
        margin-top: 15px;
        transition: background-color 0.2s;
    }
    .btn-wa:hover {
        background-color: #1ebe57;
    }
</style>
""", unsafe_allow_html=True)

# Número de WhatsApp del negocio
WHATSAPP_NUM = "573015378987"

# 3. Base de datos simulada de productos
@st.cache_data
def cargar_catalogo():
    datos = [
        {"id": 1, "nombre": "Kit Turbo LED C6 12.000 LM", "vehiculo": "Carro", "socket": "H4", "lumenes": "12,000 LM", "color": "6000K (Blanco Frío)", "precio": 85000, "garantia": "6 meses"},
        {"id": 2, "nombre": "Bombillo LED Proyector Mini Lupa", "vehiculo": "Moto", "socket": "H4", "lumenes": "16,000 LM", "color": "6000K / 3000K (Dual)", "precio": 65000, "garantia": "6 meses"},
        {"id": 3, "nombre": "Exploradoras LED Doble Color Auxiliares", "vehiculo": "Ambos", "socket": "Universal", "lumenes": "10,000 LM", "color": "Blanco + Ámbar (Antiniebla)", "precio": 110000, "garantia": "1 año"},
        {"id": 4, "nombre": "Kit LED Canbus CSP Ultra Potente", "vehiculo": "Carro", "socket": "H7", "lumenes": "22,000 LM", "color": "6500K (Blanco Puro)", "precio": 160000, "garantia": "1 año"},
        {"id": 5, "nombre": "Ojo de Ángel LED + Exploradora Moto", "vehiculo": "Moto", "socket": "Universal", "lumenes": "8,000 LM", "color": "Blanco + Aro Azul/Rojo", "precio": 48000, "garantia": "3 meses"},
        {"id": 6, "nombre": "Cocuyos LED T10 Canbus Siliconados (Par)", "vehiculo": "Ambos", "socket": "T10", "lumenes": "800 LM", "color": "Blanco / Azul Hielo", "precio": 15000, "garantia": "3 meses"},
    ]
    return pd.DataFrame(datos)

df_productos = cargar_catalogo()

# 4. Barra Lateral (Filtros)
with st.sidebar:
    st.title("⚡ JV AUTO LED")
    st.write("Filtros de Búsqueda")
    
    filtro_vehiculo = st.radio(
        "Tipo de Vehículo:",
        ["Todos", "Carro", "Moto"],
        index=0
    )
    
    sockets_disponibles = ["Todos"] + sorted(list(df_productos["socket"].unique()))
    filtro_socket = st.selectbox("Socket / Conector:", sockets_disponibles)
    
    rango_precio = st.slider(
        "Precio Máximo ($ COP):",
        min_value=10000,
        max_value=250000,
        value=250000,
        step=10000,
        format="$%d"
    )
    
    st.divider()
    st.info("📦 Envíos seguros y atención directa por WhatsApp.")

# 5. Banner Principal con la Imagen del Negocio
st.markdown('<div class="banner-container">', unsafe_allow_html=True)
col_img1, col_img2, col_img3 = st.columns([1, 8, 1])
with col_img2:
    if os.path.exists("banner.jpg"):
        st.image("banner.jpg", use_container_width=True)
    elif os.path.exists("banner.png"):
        st.image("banner.png", use_container_width=True)
    else:
        st.warning("⚠️ Recuerda subir tu imagen renombrada como **banner.jpg** al repositorio de GitHub.")
st
