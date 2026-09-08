import streamlit as st
import qrcode
from io import BytesIO

# Configuración de página
st.set_page_config(page_title="Generador QR", page_icon="⚡", layout="centered")

# CSS personalizado para fondo con QRs desenfocados y tarjeta flotante neón
st.markdown("""
    <style>
    /* Fondo con matriz de QRs y desenfoque */
    .stApp {
        background: linear-gradient(rgba(10, 10, 26, 0.8), rgba(10, 10, 26, 0.8)),
                    url('https://images.unsplash.com/photo-1526374965328-7f61d4dc18c5?q=80&w=1920&auto=format&fit=crop');
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }

    /* Tarjeta principal estilo Glassmorphism */
    .block-container {
        background: rgba(15, 23, 42, 0.75);
        padding: 2.5rem;
        border-radius: 20px;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.8);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border: 1px solid rgba(0, 240, 255, 0.2);
        max-width: 650px;
    }

    /* Título llamativo */
    h1 {
        color: #FFFFFF !important;
        text-shadow: 0 0 10px rgba(0, 240, 255, 0.6);
    }

    /* Botón principal llamativo */
    div.stButton > button:first-child {
        background: #FF0055;
        color: white;
        font-weight: bold;
        border-radius: 12px;
        border: none;
        padding: 12px 28px;
        font-size: 18px;
        width: 100%;
        box-shadow: 0 0 15px rgba(255, 0, 85, 0.5);
        transition: 0.3s;
    }
    div.stButton > button:first-child:hover {
        background: #FF2A75;
        color: white;
        transform: translateY(-2px);
        box-shadow: 0 0 25px rgba(255, 0, 85, 0.8);
    }
    </style>
""", unsafe_allow_html=True)

st.title("⚡ Generador de Códigos QR")
st.write("Crea tu código QR personalizado con un diseño moderno.")

# Entrada de texto
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

        # Genera el QR estándar (negro sobre blanco)
        img = qr.make_image(fill_color="black", back_color="white")

        buffer = BytesIO()
        img.save(buffer, format="PNG")
        byte_im = buffer.getvalue()

        st.image(byte_im, caption="✨ Tu código QR generado", width=300)
        
        st.download_button(
            label="📥 Descargar Código QR",
            data=byte_im,
            file_name="codigo_qr.png",
            mime="image/png"
        )
    else:
        st.warning("⚠️ Por favor ingresa un enlace o texto antes de generar.")
