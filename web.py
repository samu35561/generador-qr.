import streamlit as st
import qrcode
from io import BytesIO

# Configuración de página
st.set_page_config(page_title="Generador QR", page_icon="⚡", layout="centered")

# CSS personalizado: Fondo de QRs gigantes y desenfocados + tarjeta de cristal translúcida
st.markdown("""
    <style>
    /* Capa del fondo con degradados oscuros y Cyberpunk */
    .stApp {
        background: radial-gradient(circle at 20% 30%, #0c0822 0%, #060514 100%);
        overflow-x: hidden;
    }

    /* Generamos varios QR gigantes de fondo con desenfoque y colores vibrantes */
    .stApp::before {
        content: "";
        position: fixed;
        top: 0; left: 0; width: 100vw; height: 100vh;
        z-index: 0;
        pointer-events: none;
        opacity: 0.35;
        background-image: 
            /* QR 1 - Magenta arriba izquierda */
            url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" width="300" height="300" viewBox="0 0 29 29" fill="%23ff007f"><path d="M0 0h7v7H0zm2 2v3h3V2zm0 8h3v3H2zm8-10h7v7h-7zm2 2v3h3V2zm10-2h7v7h-7zm2 2v3h3V2zm-12 8h3v3h-3zm8 0h3v3h-3zm-6 6h3v3h-3zm8 0h3v3h-3zm-10 6h3v3H0zm4 0h3v3H4zm6 0h3v3h-3zm6 0h3v3h-3zm6-12h3v3h-3zm0 6h3v3h-3zm0 6h3v3h-3zm-14 4h3v3H8zm6 0h3v3h-3zm6 0h3v3h-3zm2-20h3v3h-3zm0 6h3v3h-3zm-10 12h3v3h-3z"/></svg>'),
            /* QR 2 - Verde/Cyan derecha medio */
            url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" width="550" height="550" viewBox="0 0 29 29" fill="%2300f0ff"><path d="M0 0h7v7H0zm2 2v3h3V2zm0 8h3v3H2zm8-10h7v7h-7zm2 2v3h3V2zm10-2h7v7h-7zm2 2v3h3V2zm-12 8h3v3h-3zm8 0h3v3h-3zm-6 6h3v3h-3zm8 0h3v3h-3zm-10 6h3v3H0zm4 0h3v3H4zm6 0h3v3h-3zm6 0h3v3h-3zm6-12h3v3h-3zm0 6h3v3h-3zm0 6h3v3h-3zm-14 4h3v3H8zm6 0h3v3h-3zm6 0h3v3h-3zm2-20h3v3h-3zm0 6h3v3h-3zm-10 12h3v3h-3z"/></svg>'),
            /* QR 3 - Verde neón abajo izquierda */
            url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" width="450" height="450" viewBox="0 0 29 29" fill="%2339ff14"><path d="M0 0h7v7H0zm2 2v3h3V2zm0 8h3v3H2zm8-10h7v7h-7zm2 2v3h3V2zm10-2h7v7h-7zm2 2v3h3V2zm-12 8h3v3h-3zm8 0h3v3h-3zm-6 6h3v3h-3zm8 0h3v3h-3zm-10 6h3v3H0zm4 0h3v3H4zm6 0h3v3h-3zm6 0h3v3h-3zm6-12h3v3h-3zm0 6h3v3h-3zm0 6h3v3h-3zm-14 4h3v3H8zm6 0h3v3h-3zm6 0h3v3h-3zm2-20h3v3h-3zm0 6h3v3h-3zm-10 12h3v3h-3z"/></svg>'),
            /* QR 4 - Púrpura derecha abajo */
            url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" width="380" height="380" viewBox="0 0 29 29" fill="%237928ca"><path d="M0 0h7v7H0zm2 2v3h3V2zm0 8h3v3H2zm8-10h7v7h-7zm2 2v3h3V2zm10-2h7v7h-7zm2 2v3h3V2zm-12 8h3v3h-3zm8 0h3v3h-3zm-6 6h3v3h-3zm8 0h3v3h-3zm-10 6h3v3H0zm4 0h3v3H4zm6 0h3v3h-3zm6 0h3v3h-3zm6-12h3v3h-3zm0 6h3v3h-3zm0 6h3v3h-3zm-14 4h3v3H8zm6 0h3v3h-3zm6 0h3v3h-3zm2-20h3v3h-3zm0 6h3v3h-3zm-10 12h3v3h-3z"/></svg>');
        background-repeat: no-repeat;
        background-position: 
            -50px 80px,       /* QR 1 */
            100% 20%,        /* QR 2 */
            -80px 75%,       /* QR 3 */
            85% 90%;         /* QR 4 */
        filter: blur(5px); /* Desenfoque exacto de fondo */
    }

    /* Tarjeta principal súper translúcida */
    .block-container {
        position: relative;
        z-index: 1;
        background: rgba(14, 15, 30, 0.45);
        padding: 3rem;
        border-radius: 24px;
        box-shadow: 0 10px 40px rgba(0, 0, 0, 0.7);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 255, 255, 0.08);
        max-width: 680px;
        margin-top: 2rem;
    }

    /* Título principal con glow */
    h1 {
        color: #FFFFFF !important;
        text-shadow: 0 0 10px rgba(255, 255, 255, 0.5);
        font-weight: 700;
        font-size: 2.2rem;
    }

    /* Subtítulo */
    .stMarkdown p {
        color: #CCCCCC !important;
    }

    /* Etiquetas de entradas */
    label, .stSubheader {
        color: #FFFFFF !important;
        font-weight: 500 !important;
    }

    /* Campos de entrada de texto */
    .stTextInput>div>div>input {
        background-color: rgba(22, 22, 38, 0.6) !important;
        color: white !important;
        border: 1px solid rgba(255, 255, 255, 0.15) !important;
        border-radius: 12px !important;
        padding: 12px !important;
    }

    .stTextInput>div>div>input:focus {
        border-color: #00f0ff !important;
        box-shadow: 0 0 10px rgba(0, 240, 255, 0.3) !important;
    }

    /* Estilos del subgrupo personalizado */
    .custom-row {
        background: rgba(255, 255, 255, 0.04);
        padding: 1.5rem;
        border-radius: 16px;
        border: 1px solid rgba(255, 255, 255, 0.06);
        margin-top: 1rem;
    }

    /* Input de selección de color */
    div[data-baseweb="color-input"] {
        background-color: rgba(22, 22, 38, 0.5) !important;
        border-radius: 10px !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
    }

    /* Botón Generar QR llamativo (Fucsia neón) */
    div.stButton > button:first-child {
        background: linear-gradient(90deg, #FF0055 0%, #A200FF 100%) !important;
        color: white !important;
        font-weight: 700;
        border-radius: 14px;
        border: none;
        padding: 14px 28px;
        font-size: 16px;
        width: 100%;
        box-shadow: 0 4px 20px rgba(255, 0, 85, 0.5);
        transition: transform 0.2s, box-shadow 0.2s;
        margin-top: 1rem;
    }
    
    div.stButton > button:first-child:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 30px rgba(255, 0, 85, 0.8);
    }

    /* Vista del QR generado */
    .stImage img {
        border-radius: 16px;
        margin-top: 1.5rem;
        border: 2px solid rgba(255, 255, 255, 0.1);
    }
    </style>
""", unsafe_allow_html=True)

# Título y Subtítulo de la App
st.title("⚡ Generador de Códigos QR")
st.write("Crea tu código QR personalizado con un diseño moderno.")

# Entrada de texto (Contenido o enlace del QR)
url = st.text_input("🔗 Contenido o enlace del QR:", value="hola")

# Subtítulo y selector de colores translúcido
st.write("")
st.subheader("🎨 Personaliza los colores")

col1, col2 = st.columns(2)
with col1:
    fill_color = st.color_picker("Color del QR", "#00F0FF")
with col2:
    back_color = st.color_picker("Color del Fondo", "#1B003A")

st.markdown("---")

if st.button("🚀 ¡Generar QR!"):
    if url:
        qr = qrcode.QRCode(
            version=1,
            box_size=10,
            border=4,
        )
        qr.add_data(url)
        qr.make(fit=True)

        # Usar los colores personalizados indicados
        img = qr.make_image(fill_color=fill_color, back_color=back_color)

        # Conversión del código QR a un buffer de bytes
        buffer = BytesIO()
        img.save(buffer, format="PNG")
        byte_im = buffer.getvalue()

        # Mostrar el resultado final
        st.image(byte_im, caption="✨ Tu código QR generado", width=260)
        
        st.download_button(
            label="📥 Descargar Código QR",
            data=byte_im,
            file_name="codigo_qr.png",
            mime="image/png"
        )
    else:
        st.warning("⚠️ Por favor ingresa un enlace o texto antes de generar.")
