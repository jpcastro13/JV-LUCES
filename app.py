
import streamlit as st
import pandas as pd
import urllib.parse
import os

# 1. Configuración de la página
st.set_page_config(
    page_title="JV AUTO LED | Iluminación Automotriz",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. Estilos CSS con Tipografía Urbana y Azul Cielo
st.markdown("""
<link href='https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=Syne:wght@600;700;800&display=swap' rel='stylesheet'>
<style>
    /* ======================================================== */
    /* PEGA ESTAS LÍNEAS AQUÍ, AL INICIO DE LA ETIQUETA <style> */
    [data-testid="stToolbar"] {
        visibility: hidden;
        display: none;
    }
    header {
        visibility: hidden;
        height: 0px;
    }
    /* ======================================================== */

    /* Estilos generales de la página */
    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
        background-color: #0b0f19;
        color: #f3f4f6;
    }

    h1, h2, h3, h4, h5, h6, .stSubheader {
        font-family: 'Syne', sans-serif !important;
        letter-spacing: -0.5px;
    }

st.markdown("""
<link href='https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=Syne:wght@600;700;800&display=swap' rel='stylesheet'>
<style>
    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
        background-color: #0b0f19;
        color: #f3f4f6;
    }

    h1, h2, h3, h4, h5, h6, .stSubheader {
        font-family: 'Syne', sans-serif !important;
        letter-spacing: -0.5px;
    }
    
    /* Encabezado Superior Humano y Urbano */
    .top-header {
        text-align: center;
        padding: 10px 0 20px 0;
    }
    .top-title {
        font-family: 'Syne', sans-serif;
        font-size: 2.2rem;
        font-weight: 800;
        color: #ffffff;
        margin: 0;
    }
    .top-subtitle {
        color: #00b4d8;
        font-size: 1rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 2px;
        margin-top: 5px;
    }

    /* Contenedor del Banner Carrusel */
    .banner-container {
        text-align: center;
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 50%, #0f172a 100%);
        border: 1px solid #1e293b;
        border-radius: 16px;
        padding: 15px;
        margin-bottom: 25px;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5);
    }

    /* Tarjetas de productos */
    .product-card {
        background-color: #111827;
        border: 1px solid #1f2937;
        border-radius: 14px;
        padding: 22px;
        margin-bottom: 20px;
        transition: transform 0.25s ease, border-color 0.25s ease, box-shadow 0.25s ease;
    }
    .product-card:hover {
        transform: translateY(-5px);
        border-color: #00b4d8;
        box-shadow: 0 8px 24px rgba(0, 180, 216, 0.2);
    }
    .price-tag {
        color: #00f5d4;
        font-size: 1.4rem;
        font-weight: 800;
        font-family: 'Syne', sans-serif;
        margin: 10px 0;
    }
    .badge {
        background-color: #00b4d8;
        color: #0b0f19;
        padding: 5px 10px;
        border-radius: 6px;
        font-size: 0.75rem;
        font-weight: 800;
        display: inline-block;
        margin-bottom: 8px;
        text-transform: uppercase;
        font-family: 'Syne', sans-serif;
        letter-spacing: 0.5px;
    }
    .spec-text {
        color: #9ca3af;
        font-size: 0.9rem;
        margin: 5px 0;
    }
    
    /* Botón de WhatsApp */
    .btn-wa {
        display: block;
        width: 100%;
        text-align: center;
        background-color: #25D366;
        color: #ffffff !important;
        padding: 12px;
        border-radius: 8px;
        text-decoration: none;
        font-weight: 700;
        font-family: 'Plus Jakarta Sans', sans-serif;
        margin-top: 15px;
        transition: background-color 0.2s, transform 0.1s;
    }
    .btn-wa:hover {
        background-color: #22bf5b;
        transform: scale(1.01);
    }

    [data-testid="stSidebar"] {
        background-color: #0f172a;
        border-right: 1px solid #1e293b;
    }
</style>
""", unsafe_allow_html=True)

WHATSAPP_NUM = "573015378987"

# 3. Base de datos de productos
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
    st.caption("Filtros de Búsqueda")
    
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
    st.info("📦 Envíos seguros y asesoría directa vía WhatsApp.")

# 5. Cabecera superior humana (Justo debajo de la barra gris de Streamlit)
st.markdown("""
<div class="top-header">
    <h1 class="top-title">JV AUTO LED</h1>
    <p class="top-subtitle">Iluminación y Tecnología de Alta Gama para Carros y Motos</p>
</div>
""", unsafe_allow_html=True)

# 6. Banner Movible / Carrusel de Imágenes
st.markdown('<div class="banner-container">', unsafe_allow_html=True)

# Buscamos las imágenes disponibles en tu repositorio (puedes agregar banner1.jpg, banner2.jpg, etc.)
imagenes_banner = []
for img_name in ["banner.jpg", "banner.png", "banner1.jpg", "banner2.jpg"]:
    if os.path.exists(img_name):
        imagenes_banner.append(img_name)

if imagenes_banner:
    # Si hay varias imágenes, Streamlit permite hacer un selector o pestañas estilo carrusel interactivo
    if len(imagenes_banner) > 1:
        opcion_banner = st.radio(
            "Banner interactivo", 
            [f"Promoción {i+1}" for i in range(len(imagenes_banner))], 
            horizontal=True, 
            label_visibility="collapsed"
        )
        idx_activo = int(opcion_banner.split(" ")[1]) - 1
        st.image(imagenes_banner[idx_activo], use_container_width=True)
    else:
        st.image(imagenes_banner[0], use_container_width=True)
else:
    st.warning("⚠️ Sube tu imagen como **banner.jpg** a GitHub para activarla aquí.")

st.markdown('</div>', unsafe_allow_html=True)

# 7. Pestañas de Navegación principal
tab_catalogo, tab_guia, tab_contacto = st.tabs([
    "🛒 Catálogo de Luces", 
    "💡 Guía de Bombillos", 
    "📲 Contacto y Pedidos"
])

# --- PESTAÑA 1: CATÁLOGO ---
with tab_catalogo:
    df_filtrado = df_productos.copy()
    
    if filtro_vehiculo == "Carro":
        df_filtrado = df_filtrado[df_filtrado["vehiculo"].isin(["Carro", "Ambos"])]
    elif filtro_vehiculo == "Moto":
        df_filtrado = df_filtrado[df_filtrado["vehiculo"].isin(["Moto", "Ambos"])]
        
    if filtro_socket != "Todos":
        df_filtrado = df_filtrado[df_filtrado["socket"] == filtro_socket]
        
    df_filtrado = df_filtrado[df_filtrado["precio"] <= rango_precio]

    st.subheader(f"Productos Disponibles ({len(df_filtrado)})")
    
    if df_filtrado.empty:
        st.warning("No hay productos que coincidan con los filtros seleccionados.")
    else:
        columnas = st.columns(3)
        for idx, (_, prod) in enumerate(df_filtrado.iterrows()):
            with columnas[idx % 3]:
                mensaje_wa = f"Hola JV Auto LED! Me interesa el producto *{prod['nombre']}* (Socket {prod['socket']}) por valor de ${prod['precio']:,.0f}."
                url_wa = f"https://wa.me/{WHATSAPP_NUM}?text={urllib.parse.quote(mensaje_wa)}"
                
                st.markdown(f"""
                <div class="product-card">
                    <span class="badge">{prod['vehiculo'].upper()} | {prod['socket']}</span>
                    <h4 style="margin: 5px 0 10px 0; color: #ffffff;">{prod['nombre']}</h4>
                    <p class="spec-text">🔆 <b>Lúmenes:</b> {prod['lumenes']}</p>
                    <p class="spec-text">🎨 <b>Tono:</b> {prod['color']}</p>
                    <p class="spec-text">🛡️ <b>Garantía:</b> {prod['garantia']}</p>
                    <div class="price-tag">${prod['precio']:,.0f} COP</div>
                    <a href="{url_wa}" target="_blank" class="btn-wa">🛒 Comprar por WhatsApp</a>
                </div>
                """, unsafe_allow_html=True)

# --- PESTAÑA 2: GUÍA DE COMPATIBILIDAD ---
with tab_guia:
    st.subheader("Guía de Referencias y Conectores")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        ### 🚗 Automóveis
        * **Chevrolet (Spark / Sail / Aveo):** H4
        * **Renault (Logan / Sandero / Duster):** H7 / H1
        * **Mazda (2 / 3):** H11
        * **Kia (Picanto / Rio):** H4 o H7
        """)
    with col2:
        st.markdown("""
        ### 🏍️ Motocicletas
        * **Bajaj (Pulsar NS200 / Dominar):** H4
        * **Yamaha (FZ / R15 / MT-03):** H4 / H7
        * **Honda (CB 190R / XR 150):** H4
        * **AKT (NKD 125 / TTR):** H4 / BA20D
        """)

# --- PESTAÑA 3: CONTACTO ---
with tab_contacto:
    st.subheader("Atención Directa - JV AUTO LED")
    
    url_wa_general = f"https://wa.me/{WHATSAPP_NUM}?text={urllib.parse.quote('Hola JV Auto LED, quiero asesoría personalizada para las luces de mi vehículo.')}"
    
    col_c1, col_c2 = st.columns(2)
    with col_c1:
        st.markdown(f"""
        * **📱 WhatsApp:** [301 537 8987]({url_wa_general})
        * **💡 Especialidad:** Iluminación LED de alta gama para carros y motos.
        * **📍 Cobertura:** Envíos a todo el país.
        """)
        st.markdown(f'<a href="{url_wa_general}" target="_blank" class="btn-wa" style="padding: 15px; font-size: 1.1rem;">💬 Chatear con un asesor ahora</a>', unsafe_allow_html=True)
    with col_c2:
        st.info("¿Tienes un taller o necesitas precios al por mayor? Escríbenos directamente a nuestro WhatsApp corporativo para brindarte atención prioritaria.")
