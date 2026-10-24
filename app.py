import streamlit as st
import pandas as pd
import urllib.parse
import os
from PIL import Image

# 1. Configuración de la página
st.set_page_config(
    page_title="JV AUTO LED | Iluminación Automotriz",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. Estilos CSS (Tipografía Urbana Syne + Plus Jakarta Sans, Azul Cielo y Ocultar Barra)
st.markdown("""
<link href='https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=Syne:wght@600;700;800&display=swap' rel='stylesheet'>
<style>
    /* Ocultar barra superior de Streamlit e iconos de la derecha */
    [data-testid="stToolbar"] {
        visibility: hidden;
        display: none;
    }
    header {
        visibility: hidden;
        height: 0px;
    }

    /* Tipografía general */
    html, body, [class*="css"], [data-testid="stSidebar"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
        background-color: #0b0f19;
        color: #f3f4f6;
    }

    /* Títulos urbanos con fuente Syne */
    h1, h2, h3, h4, h5, h6, .stSubheader, [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3 {
        font-family: 'Syne', sans-serif !important;
        letter-spacing: -0.5px;
    }

    /* Forzar tipografía moderna en filtros laterales y selectores */
    .stRadio label, .stSelectbox label, .stSlider label, [data-baseweb="radio"] div, [data-testid="stMarkdownContainer"] p {
        font-family: 'Plus Jakarta Sans', sans-serif !important;
    }

    /* Estilo de las Pestañas (Tabs) */
    [data-baseweb="tab"] {
        font-family: 'Syne', sans-serif !important;
        font-weight: 700 !important;
        font-size: 1rem !important;
    }

    /* Encabezado Superior */
    .top-header {
        text-align: center;
        padding: 5px 0 15px 0;
    }
    .top-title {
        font-family: 'Syne', sans-serif;
        font-size: 2.3rem;
        font-weight: 800;
        color: #ffffff;
        margin: 0;
    }
    .top-subtitle {
        color: #00b4d8;
        font-size: 0.95rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 2px;
        margin-top: 4px;
    }

    /* Contenedor del Banner */
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
    div[data-testid="stVerticalBlockBorderWrapper"] {
        background-color: #111827 !important;
        border: 1px solid #1f2937 !important;
        border-radius: 14px !important;
        padding: 10px !important;
        transition: transform 0.25s ease, border-color 0.25s ease, box-shadow 0.25s ease;
    }
    div[data-testid="stVerticalBlockBorderWrapper"]:hover {
        transform: translateY(-4px);
        border-color: #00b4d8 !important;
        box-shadow: 0 8px 24px rgba(0, 180, 216, 0.2);
    }

    .price-tag {
        color: #00f5d4;
        font-size: 1.45rem;
        font-weight: 800;
        font-family: 'Syne', sans-serif;
        margin: 6px 0;
    }
    .badge {
        background-color: #00b4d8;
        color: #0b0f19;
        padding: 4px 10px;
        border-radius: 6px;
        font-size: 0.72rem;
        font-weight: 800;
        display: inline-block;
        margin-bottom: 6px;
        text-transform: uppercase;
        font-family: 'Syne', sans-serif;
        letter-spacing: 0.5px;
    }
    .prod-title {
        font-family: 'Syne', sans-serif;
        font-size: 1.15rem;
        font-weight: 700;
        color: #ffffff;
        margin: 4px 0 8px 0;
    }

    /* Puntos de colores visuales */
    .color-dot {
        display: inline-block;
        width: 14px;
        height: 14px;
        border-radius: 50%;
        margin-right: 5px;
        border: 1px solid rgba(255,255,255,0.4);
        vertical-align: middle;
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
        font-weight: 700;
        font-family: 'Plus Jakarta Sans', sans-serif;
        margin-top: 10px;
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

# 3. Función que recorta automáticamente cada producto de tus 2 imágenes de catálogo
@st.cache_data
def extraer_imagenes_catalogo():
    os.makedirs("productos_crop", exist_ok=True)
    
    # Coordenadas proporcionales (x1, y1, x2, y2) de la foto limpia de cada producto en catalogo1.jpg
    coords_cat1 = {
        1: (0.068, 0.080, 0.264, 0.380),  # Feeston - techo
        2: (0.292, 0.080, 0.488, 0.380),  # H4 - S1CSP
        3: (0.517, 0.080, 0.713, 0.380),  # H4 - M8PRO
        4: (0.744, 0.080, 0.940, 0.380),  # EXP. BICOLOR FEDERAL
        5: (0.068, 0.545, 0.264, 0.845),  # EXP. BICOLOR TIPO LUPA
        6: (0.292, 0.545, 0.488, 0.845),  # TIRA LED SECUENCIAL(PAR)
        7: (0.517, 0.545, 0.713, 0.845),  # TIRAS RGB CONTROL BLUETOOH (4)
        8: (0.744, 0.545, 0.940, 0.845),  # EXP. BICOLOR TIPO BUHO
    }
    
    # Coordenadas proporcionales de la foto limpia de cada producto en catalogo2.jpg
    coords_cat2 = {
        9:  (0.063, 0.280, 0.262, 0.525), # T5 FIJA
        10: (0.292, 0.280, 0.490, 0.525), # T10 TABLERO
        11: (0.518, 0.280, 0.715, 0.525), # T10 FIJA
        12: (0.744, 0.280, 0.940, 0.525), # T10 STROBBE
        13: (0.063, 0.650, 0.262, 0.895), # T10 MULTICOLOR
        14: (0.292, 0.650, 0.490, 0.895), # STOP STROBBE
        15: (0.518, 0.650, 0.715, 0.895), # DIRECCIONAL STROBBE
        16: (0.744, 0.650, 0.940, 0.895), # MODULO LED
    }

    # Procesar Catalogo 1 si existe
    for ext in ["jpg", "jpeg", "png"]:
        if os.path.exists(f"catalogo1.{ext}"):
            img1 = Image.open(f"catalogo1.{ext}")
            w, h = img1.size
            for prod_id, (x1, y1, x2, y2) in coords_cat1.items():
                crop_img = img1.crop((int(w * x1), int(h * y1), int(w * x2), int(h * y2)))
                crop_img.save(f"productos_crop/prod_{prod_id}.png")
            break

    # Procesar Catalogo 2 y el Logo superior si existe
    for ext in ["jpg", "jpeg", "png"]:
        if os.path.exists(f"catalogo2.{ext}"):
            img2 = Image.open(f"catalogo2.{ext}")
            w, h = img2.size
            # Extraer logo superior de JV AUTO LED
            logo_crop = img2.crop((int(w * 0.26), int(h * 0.04), int(w * 0.74), int(h * 0.23)))
            logo_crop.save("productos_crop/logo_jv.png")
            for prod_id, (x1, y1, x2, y2) in coords_cat2.items():
                crop_img = img2.crop((int(w * x1), int(h * y1), int(w * x2), int(h * y2)))
                crop_img.save(f"productos_crop/prod_{prod_id}.png")
            break

extraer_imagenes_catalogo()

# 4. Catálogo Oficial con tus 16 Referencias Reales, Precios y Colores
@st.cache_data
def cargar_catalogo():
    datos = [
        # --- LÁMINA 1: FAROLAS, EXPLORADORAS, TIRAS Y TECHO ---
        {
            "id": 1,
            "nombre": "Feeston - Techo",
            "categoria": "Interior / Techo",
            "vehiculo": "Carro",
            "socket": "Festoon (31mm/36mm)",
            "colores_lista": ["Blanco"],
            "hex_colores": ["#FFFFFF"],
            "precio": 1390
        },
        {
            "id": 2,
            "nombre": "H4 - S1CSP",
            "categoria": "Bombillos Principales",
            "vehiculo": "Ambos",
            "socket": "H4",
            "colores_lista": ["Blanco (6000K)"],
            "hex_colores": ["#FFFFFF"],
            "precio": 19500
        },
        {
            "id": 3,
            "nombre": "H4 - M8PRO",
            "categoria": "Bombillos Principales",
            "vehiculo": "Ambos",
            "socket": "H4",
            "colores_lista": ["Blanco Ultra Potente"],
            "hex_colores": ["#FFFFFF"],
            "precio": 33500
        },
        {
            "id": 4,
            "nombre": "Exp. Bicolor Federal",
            "categoria": "Exploradoras",
            "vehiculo": "Ambos",
            "socket": "Universal",
            "colores_lista": ["Blanco + Amarillo + Estrobo Azul/Rojo"],
            "hex_colores": ["#FFFFFF", "#FFD600", "#2962FF", "#D50000"],
            "precio": 16500
        },
        {
            "id": 5,
            "nombre": "Exp. Bicolor Tipo Lupa",
            "categoria": "Exploradoras",
            "vehiculo": "Ambos",
            "socket": "Universal",
            "colores_lista": ["Blanco + Amarillo (Cuerpo Negro)", "Blanco + Amarillo + Rojo"],
            "hex_colores": ["#FFFFFF", "#FFD600", "#D50000"],
            "precio": 16500
        },
        {
            "id": 6,
            "nombre": "Tira LED Secuencial (Par)",
            "categoria": "Tiras y Módulos",
            "vehiculo": "Ambos",
            "socket": "Universal 12V",
            "colores_lista": ["Blanco DRL + Giro Ámbar Secuencial"],
            "hex_colores": ["#FFFFFF", "#FFAB00"],
            "precio": 27000
        },
        {
            "id": 7,
            "nombre": "Tiras RGB Control Bluetooth (x4)",
            "categoria": "Tiras y Módulos",
            "vehiculo": "Ambos",
            "socket": "Universal 12V",
            "colores_lista": ["Multicolor RGB (Control + App)"],
            "hex_colores": ["#FF1744", "#00E676", "#2979FF", "#E040FB"],
            "precio": 39000
        },
        {
            "id": 8,
            "nombre": "Exp. Bicolor Tipo Búho",
            "categoria": "Exploradoras",
            "vehiculo": "Ambos",
            "socket": "Universal",
            "colores_lista": ["Blanco + Amarillo (Doble Lupa)"],
            "hex_colores": ["#FFFFFF", "#FFD600"],
            "precio": 16500
        },

        # --- LÁMINA 2: COCUYOS T5/T10, STOPS, DIRECCIONALES Y MÓDULOS ---
        {
            "id": 9,
            "nombre": "T5 Fija",
            "categoria": "Cocuyos y Tablero",
            "vehiculo": "Ambos",
            "socket": "T5",
            "colores_lista": ["Rojo", "Azul Hielo", "Azul Rey", "Verde", "Blanco", "Rosado / Fucsia"],
            "hex_colores": ["#FF1744", "#80D8FF", "#2962FF", "#00C853", "#FFFFFF", "#F50057"],
            "precio": 530
        },
        {
            "id": 10,
            "nombre": "T10 Tablero",
            "categoria": "Cocuyos y Tablero",
            "vehiculo": "Ambos",
            "socket": "T10",
            "colores_lista": ["Rojo", "Azul Hielo", "Azul Rey", "Verde", "Blanco", "Rosado / Fucsia"],
            "hex_colores": ["#FF1744", "#80D8FF", "#2962FF", "#00C853", "#FFFFFF", "#F50057"],
            "precio": 1100
        },
        {
            "id": 11,
            "nombre": "T10 Fija",
            "categoria": "Cocuyos y Tablero",
            "vehiculo": "Ambos",
            "socket": "T10",
            "colores_lista": ["Rojo", "Azul Hielo", "Azul Rey", "Verde", "Blanco", "Rosado / Fucsia"],
            "hex_colores": ["#FF1744", "#80D8FF", "#2962FF", "#00C853", "#FFFFFF", "#F50057"],
            "precio": 1700
        },
        {
            "id": 12,
            "nombre": "T10 Strobbe",
            "categoria": "Cocuyos y Tablero",
            "vehiculo": "Ambos",
            "socket": "T10",
            "colores_lista": ["Rojo", "Azul Hielo", "Azul Rey", "Verde", "Blanco", "Rosado / Fucsia"],
            "hex_colores": ["#FF1744", "#80D8FF", "#2962FF", "#00C853", "#FFFFFF", "#F50057"],
            "precio": 2400
        },
        {
            "id": 13,
            "nombre": "T10 Multicolor",
            "categoria": "Cocuyos y Tablero",
            "vehiculo": "Ambos",
            "socket": "T10",
            "colores_lista": ["Multicolor RGB Automático"],
            "hex_colores": ["#2962FF", "#FF1744", "#FFFFFF"],
            "precio": 2700
        },
        {
            "id": 14,
            "nombre": "Stop Strobbe",
            "categoria": "Stop y Direccionales",
            "vehiculo": "Ambos",
            "socket": "1157 / P21/5W (2 Contactos)",
            "colores_lista": ["Rojo", "Blanco"],
            "hex_colores": ["#FF1744", "#FFFFFF"],
            "precio": 2950
        },
        {
            "id": 15,
            "nombre": "Direccional Strobbe",
            "categoria": "Stop y Direccionales",
            "vehiculo": "Ambos",
            "socket": "1156 / BAU15S (1 Contacto)",
            "colores_lista": ["Rojo", "Blanco", "Amarillo / Ámbar"],
            "hex_colores": ["#FF1744", "#FFFFFF", "#FFD600"],
            "precio": 2950
        },
        {
            "id": 16,
            "nombre": "Módulo LED",
            "categoria": "Tiras y Módulos",
            "vehiculo": "Ambos",
            "socket": "Universal 12V",
            "colores_lista": ["Rojo", "Amarillo", "Azul Rey", "Verde", "Blanco", "Rosado / Fucsia"],
            "hex_colores": ["#FF1744", "#FFD600", "#2962FF", "#00C853", "#FFFFFF", "#F50057"],
            "precio": 1100
        },
    ]
    return pd.DataFrame(datos)

df_productos = cargar_catalogo()

# 5. Barra Lateral (Filtros actualizados a tus productos reales)
with st.sidebar:
    if os.path.exists("productos_crop/logo_jv.png"):
        st.image("productos_crop/logo_jv.png", use_container_width=True)
    else:
        st.title("⚡ JV AUTO LED")
        
    st.caption("Filtros de Catálogo")
    
    categorias_disp = ["Todas"] + list(df_productos["categoria"].unique())
    filtro_categoria = st.selectbox("Categoría de Luz:", categorias_disp)
    
    sockets_disp = ["Todos"] + sorted(list(df_productos["socket"].unique()))
    filtro_socket = st.selectbox("Socket / Referencia:", sockets_disp)
    
    rango_precio = st.slider(
        "Precio Máximo ($ COP):",
        min_value=500,
        max_value=45000,
        value=45000,
        step=500,
        format="$%d"
    )
    
    busqueda_texto = st.text_input("🔍 Buscar por nombre (ej. Búho, T10, H4):")
    
    st.divider()
    st.info("📦 Envíos seguros a todo el país y atención directa por WhatsApp.")

# 6. Cabecera Superior (Muestra el logo extraído si existe, o texto urbano)
if os.path.exists("productos_crop/logo_jv.png"):
    col_l1, col_l2, col_l3 = st.columns([2, 3, 2])
    with col_l2:
        st.image("productos_crop/logo_jv.png", use_container_width=True)
else:
    st.markdown("""
    <div class="top-header">
        <h1 class="top-title">JV AUTO LED</h1>
        <p class="top-subtitle">Iluminación Automotriz para Carros y Motos</p>
    </div>
    """, unsafe_allow_html=True)

# 7. Banner Principal Movible
st.markdown('<div class="banner-container">', unsafe_allow_html=True)
imagenes_banner = [img for img in ["banner.jpg", "banner.png", "banner1.jpg", "banner2.jpg"] if os.path.exists(img)]

if imagenes_banner:
    if len(imagenes_banner) > 1:
        opcion_banner = st.radio(
            "Promociones",
            [f"Vista {i+1}" for i in range(len(imagenes_banner))],
            horizontal=True,
            label_visibility="collapsed"
        )
        idx_activo = int(opcion_banner.split(" ")[1]) - 1
        st.image(imagenes_banner[idx_activo], use_container_width=True)
    else:
        st.image(imagenes_banner[0], use_container_width=True)
else:
    st.info("💡 Sube `banner.jpg`, `catalogo1.jpg` y `catalogo2.jpg` a tu repositorio en GitHub para visualizar todas las imágenes.")
st.markdown('</div>', unsafe_allow_html=True)

# 8. Pestañas de Navegación
tab_catalogo, tab_guia, tab_contacto = st.tabs([
    "🛒 Catálogo Oficial (16 Referencias)", 
    "💡 Guía de Bombillos", 
    "📲 Contacto y Pedidos"
])

# --- PESTAÑA 1: CATÁLOGO DE PRODUCTOS ---
with tab_catalogo:
    df_filtrado = df_productos.copy()
    
    if filtro_categoria != "Todas":
        df_filtrado = df_filtrado[df_filtrado["categoria"] == filtro_categoria]
        
    if filtro_socket != "Todos":
        df_filtrado = df_filtrado[df_filtrado["socket"] == filtro_socket]
        
    df_filtrado = df_filtrado[df_filtrado["precio"] <= rango_precio]
    
    if busqueda_texto:
        df_filtrado = df_filtrado[df_filtrado["nombre"].str.contains(busqueda_texto, case=False, na=False)]

    st.subheader(f"Referencias Disponibles ({len(df_filtrado)})")
    
    if df_filtrado.empty:
        st.warning("No encontramos referencias con esos filtros. Intenta ampliar el rango de precio o cambiar la categoría.")
    else:
        # Cuadrícula de 4 columnas igual que en tu catálogo original
        columnas = st.columns(4)
        for idx, (_, prod) in enumerate(df_filtrado.iterrows()):
            with columnas[idx % 4]:
                with st.container(border=True):
                    # 1. Mostrar imagen recortada independiente del producto
                    ruta_img_crop = f"productos_crop/prod_{prod['id']}.png"
                    ruta_img_manual = f"img/prod_{prod['id']}.jpg"
                    
                    if os.path.exists(ruta_img_crop):
                        st.image(ruta_img_crop, use_container_width=True)
                    elif os.path.exists(ruta_img_manual):
                        st.image(ruta_img_manual, use_container_width=True)
                    else:
                        st.caption("📷 *(Sube catalogo1.jpg y catalogo2.jpg a GitHub para ver la foto)*")

                    # 2. Etiqueta y Nombre
                    dots_html = "".join([f'<span class="color-dot" style="background-color:{hx};"></span>' for hx in prod["hex_colores"]])
                    st.markdown(f"""
                        <span class="badge">{prod['categoria']}</span>
                        <div class="prod-title">{prod['nombre']}</div>
                        <div style="margin-bottom: 6px;">{dots_html}</div>
                    """, unsafe_allow_html=True)

                    # 3. Selector de color interactivo para que el cliente elija
                    if len(prod["colores_lista"]) > 1:
                        color_elegido = st.selectbox(
                            "Elige el color:",
                            prod["colores_lista"],
                            key=f"color_{prod['id']}"
                        )
                    else:
                        color_elegido = prod["colores_lista"][0]
                        st.caption(f"🎨 **Tono:** {color_elegido}")

                    # 4. Precio y Botón directo a WhatsApp con el color elegido
                    mensaje_wa = (
                        f"Hola JV Auto LED! Me interesa comprar:\n"
                        f"• *Referencia:* {prod['nombre']}\n"
                        f"• *Color:* {color_elegido}\n"
                        f"• *Precio unitario:* ${prod['precio']:,.0f} COP"
                    )
                    url_wa = f"https://wa.me/{WHATSAPP_NUM}?text={urllib.parse.quote(mensaje_wa)}"
                    
                    st.markdown(f"""
                        <div class="price-tag">${prod['precio']:,.0f} COP</div>
                        <a href="{url_wa}" target="_blank" class="btn-wa">🛒 Pedir en {color_elegido.split()[0]}</a>
                    """, unsafe_allow_html=True)

# --- PESTAÑA 2: GUÍA DE COMPATIBILIDAD ---
with tab_guia:
    st.subheader("Guía Rápida de Referencias")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        ### 🚗 Aplicaciones en Carros y Motos
        * **H4 (S1CSP / M8PRO):** Luz principal de altas y bajas integradas (Chevrolet Spark/Sail, motos Pulsar, FZ, CB, NKD, etc.).
        * **T10 (Fija / Tablero / Strobbe / Multicolor):** Cocuyos delanteros, luz de placa y luz de techo o tablero.
        * **T5 Fija:** Bombillo mini para retroiluminación de tableros, tacómetros y consolas de aire acondicionado.
        * **Feeston - Techo:** Luz central de cortesía / domo interior del techo en automóviles.
        """)
    with col2:
        st.markdown("""
        ### 🚨 Exploradoras, Stops y Tiras
        * **Exploradoras (Federal / Tipo Lupa / Búho):** Auxiliares externas universales de doble tono (Blanco para ruta despejada y Amarillo para lluvia o neblina).
        * **Stop Strobbe y Direccional Strobbe:** Reemplazo directo para bombillos traseros de freno y giro con destello de alta visibilidad.
        * **Tira LED Secuencial y RGB Bluetooth:** Personalización estética para farolas (DRL con giro secuencial) o luz ambiental controlada desde el celular.
        """)

# --- PESTAÑA 3: CONTACTO ---
with tab_contacto:
    st.subheader("Atención Directa - JV AUTO LED")
    url_wa_general = f"https://wa.me/{WHATSAPP_NUM}?text={urllib.parse.quote('Hola JV Auto LED, quiero hacer un pedido de luces.')}"
    
    col_c1, col_c2 = st.columns(2)
    with col_c1:
        st.markdown(f"""
        * **📱 WhatsApp Directo:** [301 537 8987]({url_wa_general})
        * **🌐 Catálogo Web:** www.jvautoled.com
        * **📍 Cobertura:** Envíos a todo el país.
        """)
        st.markdown(f'<a href="{url_wa_general}" target="_blank" class="btn-wa" style="padding: 14px; font-size: 1.05rem;">💬 Hablar por WhatsApp</a>', unsafe_allow_html=True)
    with col_c2:
        st.info("💡 **¿Compras al por mayor o quieres armar un combo completo para tu carro o moto?** Escríbenos por WhatsApp con las referencias que te gustaron y te armamos tu cotización al instante.")


