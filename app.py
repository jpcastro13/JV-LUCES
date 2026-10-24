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

# 2. Estilos CSS personalizados
st.markdown("""
<style>
    .main {
        background-color: #0e1117;
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

    /* Tarjetas de productos */
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
        font-weight: bold;
        margin-top: 15px;
        transition: background-color 0.2s;
    }
    .btn-wa:hover {
        background-color: #1ebe57;
    }
</style>
""", unsafe_allow_html=True)

# Número de WhatsApp extraído de tu imagen (301 537 8987 -> Formato internacional Colombia +57)
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
    else:
        # Mensaje de apoyo por si aún no han subido el archivo con ese nombre exacto
        st.warning("⚠️ Sube la imagen del banner a tu repositorio de GitHub con el nombre exacto **`banner.jpg`** para que aparezca aquí.")
st.markdown('</div>', unsafe_allow_html=True)

# 6. Pestañas de Navegación
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
        ### 🚗 Automóviles
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
