import streamlit as st
import qrcode
from io import BytesIO

# Configuración de página
st.set_page_config(page_title="Generador QR", page_icon="⚡", layout="centered")

# CSS personalizado: Fondo con patrón de QRs coloridos y desenfocados
st.markdown("""
    <style>
    /* Fondo oscuro base */
    .stApp {
        background-color: #0a0a1a;
    }

    /* Patrón de QRs neón repetidos y desenfocados */
    .stApp::before {
        content: "";
        position: fixed;
        top: 0; left: 0; width: 100vw; height: 100vh;
        z-index: 0;
        pointer-events: none;
        opacity: 0.35;
        background-image: url('https://images.unsplash.com/photo-1526374965328-7f61d4dc18c5?q=80&w=1920&auto=format&fit=crop');
        background-size: 500px auto; /* Tamaño mediano para que se distingan los QRs */
        background-repeat: repeat;
        filter: blur(4px); /* Desenfoque ligero */
    }

    /* Tarjeta translúcida estilo Glassmorphism */
    .block-container {
        position: relative;
        z-index: 1;
        background: rgba(18, 18, 38, 0.75);
        padding: 3rem;
        border-radius: 24px;
        box-shadow: 0 10px 40px rgba(0, 0, 0, 0.8);
        backdrop-filter: blur(16px);
        -webkit-backdrop-filter: blur(16px);
        border: 1px solid rgba(0, 240, 255, 0.2);
        max-width: 650px;
        margin-top: 2rem;
    }

    /* Título con glow */
    h1 {
        color: #00F0FF !important;
        text-shadow: 0 0 12px rgba(0, 240, 255, 0.6);
        font-weight: 800;
    }

    /* Textos secundarios */
    .stMarkdown p {
        color: #E2E8F0 !important;
        font-size: 1.1rem;
    }

    /* Input de texto */
    .stTextInput>div>div>input {
        background-color: rgba(10, 10, 26, 0.6) !important;
        color: white !important;
        border: 1px solid rgba(0, 240, 255, 0.3) !important;
        border-radius: 12px !important;
        padding: 12px !important;
    }

    .stTextInput>div>div>input:focus {
        border-color: #FF0055 !important;
        box-shadow: 0 0 10px rgba(255, 0, 85, 0.5) !important;
    }

    /* Botón neón principal */
    div.stButton > button:first-child {
        background: linear-gradient(90deg, #FF0055 0%, #7928CA 100%) !important;
        color: white !important;
        font-weight: bold;
        border-radius: 14px;
        border: none;
        padding: 14px 28px;
        font-size: 18px;
        width: 100%;
        box-shadow: 0 0 20px rgba(255, 0, 85, 0.4);
        transition: 0.3s;
        margin-top: 1rem;
    }

    div.stButton > button:first-child:hover {
        transform: translateY(-2px);
        box-shadow: 0 0 30px rgba(255, 0, 85, 0.8);
    }

    /* Imagen descargable del QR */
    .stImage img {
        border-radius: 16px;
        border: 2px solid rgba(0, 240, 255, 0.3);
    }
    </style>
""", unsafe_allow_html=True)

st.title("⚡ Generador de Códigos QR")
st.write("Crea tu código QR personalizado con un diseño moderno.")

# Entrada de texto única
url = st.text_input("🔗 Contenido o enlace del QR:", placeholder="Ej. https://misitio.com")

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

        # Genera el QR estándar (Azul neón sobre fondo oscuro)
        img = qr.make_image(fill_color="#00F0FF", back_color="#101024")

        buffer = BytesIO()
        img.save(buffer, format="PNG")
        byte_im = buffer.getvalue()

        st.image(byte_im, caption="✨ Tu código QR generado", width=280)
        
        st.download_button(
            label="📥 Descargar Código QR",
            data=byte_im,
            file_name="codigo_qr.png",
            mime="image/png"
        )
    else:
        st.warning("⚠️ Por favor ingresa un enlace o texto antes de generar.")
