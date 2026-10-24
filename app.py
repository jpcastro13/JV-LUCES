import os
import urllib.parse

import pandas as pd
import streamlit as st
from PIL import Image

st.set_page_config(
    page_title="JV Auto LED | Luces LED para carro y moto",
    page_icon="productos_crop/logo_jv.png" if os.path.exists("productos_crop/logo_jv.png") else None,
    layout="wide",
    initial_sidebar_state="collapsed",
)

WHATSAPP_NUM = "573015378987"

# ---------------------------------------------------------------- estilos
ESTILOS = """
<link href="https://fonts.googleapis.com/css2?family=Barlow:wght@400;500;600&family=Barlow+Semi+Condensed:wght@500;600;700&display=swap" rel="stylesheet">
<style>
:root {
    --fondo: #EEF0F2;
    --superficie: #FFFFFF;
    --tinta: #16212E;
    --tinta-suave: #5B6675;
    --linea: #D3D8DE;
    --acento: #E8A100;
    --wa: #1FA855;
}
[data-testid="stSidebar"], [data-testid="collapsedControl"],
[data-testid="stToolbar"], header, footer { display: none !important; }

.stApp, html, body { background: var(--fondo); color: var(--tinta); }
html, body, [class*="css"], .stMarkdown, label, input {
    font-family: 'Barlow', sans-serif;
}
.block-container { max-width: 1200px; padding-top: 1.6rem; }

h1, h2, h3, .titulo {
    font-family: 'Barlow Semi Condensed', sans-serif !important;
    color: var(--tinta);
    letter-spacing: 0;
}

/* Encabezado */
.cabecera {
    display: flex; justify-content: space-between; align-items: baseline;
    border-bottom: 2px solid var(--tinta); padding-bottom: 10px; margin-bottom: 18px;
}
.cabecera .marca { font-family: 'Barlow Semi Condensed'; font-weight: 700; font-size: 1.9rem; }
.cabecera .detalle { color: var(--tinta-suave); font-size: .95rem; }
.cabecera a { color: var(--tinta); font-weight: 600; text-decoration: underline; text-underline-offset: 3px; }

/* Pestañas */
[data-baseweb="tab"] { font-family: 'Barlow Semi Condensed' !important; font-size: 1.05rem !important; font-weight: 600 !important; }
[data-baseweb="tab-highlight"] { background-color: var(--tinta) !important; }

/* Producto */
div[data-testid="stVerticalBlockBorderWrapper"] {
    background: var(--superficie) !important;
    border: 1px solid var(--linea) !important;
    border-radius: 4px !important;
    padding: 12px !important;
}
.prod-nombre { font-family: 'Barlow Semi Condensed'; font-size: 1.2rem; font-weight: 600; line-height: 1.2; margin: 6px 0 2px; }
.prod-meta { color: var(--tinta-suave); font-size: .86rem; margin-bottom: 8px; }
.muestras { margin: 4px 0 8px; }
.muestra { display: inline-block; width: 13px; height: 13px; border-radius: 2px; margin-right: 4px; border: 1px solid rgba(0,0,0,.25); vertical-align: middle; }
.precio { font-family: 'Barlow Semi Condensed'; font-size: 1.5rem; font-weight: 700; font-variant-numeric: tabular-nums; margin: 8px 0 2px; }
.precio small { font-size: .8rem; font-weight: 500; color: var(--tinta-suave); }

/* Botón WhatsApp */
.btn-wa {
    display: block; text-align: center; background: var(--wa); color: #fff !important;
    padding: 9px 10px; border-radius: 3px; text-decoration: none !important;
    font-weight: 600; margin-top: 8px;
}
.btn-wa:hover { background: #188a46; }
.btn-wa:focus-visible, .cabecera a:focus-visible { outline: 3px solid var(--acento); outline-offset: 2px; }
</style>
"""
# Markdown corta el bloque HTML en la primera línea en blanco: se eliminan todas
st.markdown("\n".join(l for l in ESTILOS.splitlines() if l.strip()), unsafe_allow_html=True)


# ---------------------------------------------------- recorte de imágenes
@st.cache_data
def extraer_imagenes_catalogo():
    os.makedirs("productos_crop", exist_ok=True)

    cat1 = {
        1: (0.068, 0.080, 0.264, 0.380), 2: (0.292, 0.080, 0.488, 0.380),
        3: (0.517, 0.080, 0.713, 0.380), 4: (0.744, 0.080, 0.940, 0.380),
        5: (0.068, 0.545, 0.264, 0.845), 6: (0.292, 0.545, 0.488, 0.845),
        7: (0.517, 0.545, 0.713, 0.845), 8: (0.744, 0.545, 0.940, 0.845),
    }
    cat2 = {
        9: (0.063, 0.280, 0.262, 0.525), 10: (0.292, 0.280, 0.490, 0.525),
        11: (0.518, 0.280, 0.715, 0.525), 12: (0.744, 0.280, 0.940, 0.525),
        13: (0.063, 0.650, 0.262, 0.895), 14: (0.292, 0.650, 0.490, 0.895),
        15: (0.518, 0.650, 0.715, 0.895), 16: (0.744, 0.650, 0.940, 0.895),
    }

    def recortar(nombre, coords, logo=False):
        for ext in ("jpg", "jpeg", "png"):
            ruta = f"{nombre}.{ext}"
            if os.path.exists(ruta):
                img = Image.open(ruta)
                w, h = img.size
                if logo:
                    img.crop((int(w * .26), int(h * .04), int(w * .74), int(h * .23))).save("productos_crop/logo_jv.png")
                for pid, (x1, y1, x2, y2) in coords.items():
                    img.crop((int(w * x1), int(h * y1), int(w * x2), int(h * y2))).save(f"productos_crop/prod_{pid}.png")
                return

    recortar("catalogo1", cat1)
    recortar("catalogo2", cat2, logo=True)


extraer_imagenes_catalogo()

# ---------------------------------------------------------------- catálogo
SEIS = ["Rojo", "Azul hielo", "Azul rey", "Verde", "Blanco", "Rosado / Fucsia"]
SEIS_HEX = ["#FF1744", "#80D8FF", "#2962FF", "#00C853", "#FFFFFF", "#F50057"]


@st.cache_data
def cargar_catalogo():
    # id, nombre, categoría, socket, colores, hex, precio
    filas = [
        (1, "Festoon para techo", "Interior y techo", "Festoon (31 mm / 36 mm)", ["Blanco"], ["#FFFFFF"], 1390),
        (2, "H4 S1CSP", "Bombillos principales", "H4", ["Blanco (6000K)"], ["#FFFFFF"], 19500),
        (3, "H4 M8PRO", "Bombillos principales", "H4", ["Blanco ultra potente"], ["#FFFFFF"], 33500),
        (4, "Exploradora bicolor Federal", "Exploradoras", "Universal",
         ["Blanco + amarillo + estrobo azul/rojo"], ["#FFFFFF", "#FFD600", "#2962FF", "#D50000"], 16500),
        (5, "Exploradora bicolor tipo lupa", "Exploradoras", "Universal",
         ["Blanco + amarillo (cuerpo negro)", "Blanco + amarillo + rojo"], ["#FFFFFF", "#FFD600", "#D50000"], 16500),
        (6, "Tira LED secuencial (par)", "Tiras y módulos", "Universal 12V",
         ["Blanco DRL + giro ámbar secuencial"], ["#FFFFFF", "#FFAB00"], 27000),
        (7, "Tiras RGB con control Bluetooth (x4)", "Tiras y módulos", "Universal 12V",
         ["Multicolor RGB (control + app)"], ["#FF1744", "#00E676", "#2979FF", "#E040FB"], 39000),
        (8, "Exploradora bicolor tipo búho", "Exploradoras", "Universal",
         ["Blanco + amarillo (doble lupa)"], ["#FFFFFF", "#FFD600"], 16500),
        (9, "T5 fija", "Cocuyos y tablero", "T5", SEIS, SEIS_HEX, 530),
        (10, "T10 tablero", "Cocuyos y tablero", "T10", SEIS, SEIS_HEX, 1100),
        (11, "T10 fija", "Cocuyos y tablero", "T10", SEIS, SEIS_HEX, 1700),
        (12, "T10 strobbe", "Cocuyos y tablero", "T10", SEIS, SEIS_HEX, 2400),
        (13, "T10 multicolor", "Cocuyos y tablero", "T10",
         ["Multicolor RGB automático"], ["#2962FF", "#FF1744", "#FFFFFF"], 2700),
        (14, "Stop strobbe", "Stop y direccionales", "1157 / P21/5W (2 contactos)",
         ["Rojo", "Blanco"], ["#FF1744", "#FFFFFF"], 2950),
        (15, "Direccional strobbe", "Stop y direccionales", "1156 / BAU15S (1 contacto)",
         ["Rojo", "Blanco", "Amarillo / Ámbar"], ["#FF1744", "#FFFFFF", "#FFD600"], 2950),
        (16, "Módulo LED", "Tiras y módulos", "Universal 12V",
         ["Rojo", "Amarillo", "Azul rey", "Verde", "Blanco", "Rosado / Fucsia"],
         ["#FF1744", "#FFD600", "#2962FF", "#00C853", "#FFFFFF", "#F50057"], 1100),
    ]
    return pd.DataFrame(filas, columns=["id", "nombre", "categoria", "socket", "colores", "hex", "precio"])


df = cargar_catalogo()


def link_wa(texto):
    return f"https://wa.me/{WHATSAPP_NUM}?text={urllib.parse.quote(texto)}"


# --------------------------------------------------------------- cabecera
logo = "productos_crop/logo_jv.png"
if os.path.exists(logo):
    st.image(logo, width=220)

st.markdown(f"""
<div class="cabecera">
    <div>
        <div class="marca">JV Auto LED</div>
        <div class="detalle">Bombillos y luces LED para carro y moto. Envíos a todo el país.</div>
    </div>
    <div class="detalle">Pedidos: <a href="{link_wa('Hola JV Auto LED, quiero hacer un pedido de luces.')}" target="_blank">301 537 8987</a></div>
</div>
""", unsafe_allow_html=True)

banners = [b for b in ("banner.jpg", "banner.png", "banner1.jpg", "banner2.jpg") if os.path.exists(b)]
if banners:
    if len(banners) > 1:
        opcion = st.radio("Promociones", [f"Promoción {i + 1}" for i in range(len(banners))],
                          horizontal=True, label_visibility="collapsed")
        st.image(banners[int(opcion.split()[1]) - 1], use_container_width=True)
    else:
        st.image(banners[0], use_container_width=True)

tab_catalogo, tab_guia, tab_contacto = st.tabs(["Catálogo", "Guía de referencias", "Contacto y pedidos"])

# --------------------------------------------------------------- catálogo
with tab_catalogo:
    f1, f2, f3, f4 = st.columns([1, 1, 1, 1.2])
    categoria = f1.selectbox("Categoría", ["Todas"] + list(df["categoria"].unique()))
    socket = f2.selectbox("Socket", ["Todos"] + sorted(df["socket"].unique()))
    precio_max = f3.slider("Precio máximo (COP)", 500, 45000, 45000, step=500, format="$%d")
    texto = f4.text_input("Buscar", placeholder="Ej: H4, T10, búho")

    res = df
    if categoria != "Todas":
        res = res[res["categoria"] == categoria]
    if socket != "Todos":
        res = res[res["socket"] == socket]
    res = res[res["precio"] <= precio_max]
    if texto:
        res = res[res["nombre"].str.contains(texto, case=False, na=False)]

    st.markdown(f"**{len(res)}** de {len(df)} referencias")

    if res.empty:
        st.info("Ninguna referencia coincide con esos filtros. Sube el precio máximo o elige otra categoría.")
    else:
        cols = st.columns(4)
        for i, (_, p) in enumerate(res.iterrows()):
            with cols[i % 4]:
                with st.container(border=True):
                    foto = f"productos_crop/prod_{p['id']}.png"
                    foto_manual = f"img/prod_{p['id']}.jpg"
                    if os.path.exists(foto):
                        st.image(foto, use_container_width=True)
                    elif os.path.exists(foto_manual):
                        st.image(foto_manual, use_container_width=True)

                    muestras = "".join(f'<span class="muestra" style="background:{h}"></span>' for h in p["hex"])
                    st.markdown(f"""
                        <div class="prod-nombre">{p['nombre']}</div>
                        <div class="prod-meta">{p['categoria']} · Socket {p['socket']}</div>
                        <div class="muestras">{muestras}</div>
                    """, unsafe_allow_html=True)

                    if len(p["colores"]) > 1:
                        color = st.selectbox("Color", p["colores"], key=f"color_{p['id']}")
                    else:
                        color = p["colores"][0]
                        st.caption(f"Color: {color}")

                    msg = (f"Hola JV Auto LED, me interesa:\n"
                           f"- Referencia: {p['nombre']}\n- Color: {color}\n"
                           f"- Precio unitario: ${p['precio']:,.0f} COP")
                    st.markdown(f"""
                        <div class="precio">${p['precio']:,.0f} <small>COP</small></div>
                        <a href="{link_wa(msg)}" target="_blank" class="btn-wa">Pedir por WhatsApp</a>
                    """, unsafe_allow_html=True)

# ------------------------------------------------------------------ guía
with tab_guia:
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("""
### Bombillos y cocuyos
- **H4 (S1CSP, M8PRO):** luz principal con altas y bajas integradas. Sirve para Chevrolet Spark y Sail, y motos como Pulsar, FZ, CB y NKD.
- **T10 (fija, tablero, strobbe, multicolor):** cocuyos delanteros, luz de placa y luz de techo o tablero.
- **T5 fija:** bombillo mini para tableros, tacómetros y consolas de aire acondicionado.
- **Festoon para techo:** luz central de cortesía en el techo del carro.
""")
    with c2:
        st.markdown("""
### Exploradoras, stops y tiras
- **Exploradoras (Federal, lupa, búho):** auxiliares universales de dos tonos. Blanco para vía despejada, amarillo para lluvia o neblina.
- **Stop y direccional strobbe:** reemplazo directo de los bombillos traseros de freno y giro, con destello de alta visibilidad.
- **Tira secuencial y RGB Bluetooth:** la secuencial hace de luz diurna y giro en las farolas; la RGB se controla desde el celular.
""")

# -------------------------------------------------------------- contacto
with tab_contacto:
    st.subheader("Hacer un pedido")
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("""
- **WhatsApp:** 301 537 8987
- **Catálogo web:** www.jvautoled.com
- **Cobertura:** envíos a todo el país
""")
        st.markdown(f'<a href="{link_wa("Hola JV Auto LED, quiero hacer un pedido de luces.")}" target="_blank" class="btn-wa">Escribir por WhatsApp</a>',
                    unsafe_allow_html=True)
    with c2:
        st.markdown("Si compras por mayor o quieres armar un combo para tu carro o moto, "
                    "mándanos las referencias que te interesan y te enviamos la cotización.")
  

