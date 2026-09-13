import streamlit as st
import qrcode
from io import BytesIO

# Configuración de página
st.set_page_config(page_title="Generador QR", page_icon="⚡", layout="centered")

# CSS: Patrón equilibrado de QRs neón dispersos + Blur ajustado
st.markdown("""
    <style>
    .stApp {
        background-color: #080711;
        overflow-x: hidden;
    }

    /* Patrón fluido de QRs neón desenfocados en el fondo */
    .stApp::before {
        content: "";
        position: fixed;
        top: 0; left: 0; width: 100vw; height: 100vh;
        z-index: 0;
        pointer-events: none;
        opacity: 0.35;
        background-image: 
            /* QR Cyan */
            url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" width="180" height="180" viewBox="0 0 29 29" fill="%2300f0ff"><path d="M0 0h7v7H0zm2 2v3h3V2zm0 8h3v3H2zm8-10h7v7h-7zm2 2v3h3V2zm10-2h7v7h-7zm2 2v3h3V2zm-12 8h3v3h-3zm8 0h3v3h-3zm-6 6h3v3h-3zm8 0h3v3h-3zm-10 6h3v3H0zm4 0h3v3H4zm6 0h3v3h-3zm6 0h3v3h-3zm6-12h3v3h-3zm0 6h3v3h-3zm0 6h3v3h-3zm-14 4h3v3H8zm6 0h3v3h-3zm6 0h3v3h-3zm2-20h3v3h-3zm0 6h3v3h-3zm-10 12h3v3h-3z"/></svg>'),
            /* QR Magenta */
            url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" width="220" height="220" viewBox="0 0 29 29" fill="%23ff007f"><path d="M0 0h7v7H0zm2 2v3h3V2zm0 8h3v3H2zm8-10h7v7h-7zm2 2v3h3V2zm10-2h7v7h-7zm2 2v3h3V2zm-12 8h3v3h-3zm8 0h3v3h-3zm-6 6h3v3h-3zm8 0h3v3h-3zm-10 6h3v3H0zm4 0h3v3H4zm6 0h3v3h-3zm6 0h3v3h-3zm6-12h3v3h-3zm0 6h3v3h-3zm0 6h3v3h-3zm-14 4h3v3H8zm6 0h3v3h-3zm6 0h3v3h-3zm2-20h3v3h-3zm0 6h3v3h-3zm-10 12h3v3h-3z"/></svg>'),
            /* QR Verde Neón */
            url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" width="200" height="200" viewBox="0 0 29 29" fill="%2300ff88"><path d="M0 0h7v7H0zm2 2v3h3V2zm0 8h3v3H2zm8-10h7v7h-7zm2 2v3h3V2zm10-2h7v7h-7zm2 2v3h3V2zm-12 8h3v3h-3zm8 0h3v3h-3zm-6 6h3v3h-3zm8 0h3v3h-3zm-10 6h3v3H0zm4 0h3v3H4zm6 0h3v3h-3zm6 0h3v3h-3zm6-12h3v3h-3zm0 6h3v3h-3zm0 6h3v3h-3zm-14 4h3v3H8zm6 0h3v3h-3zm6 0h3v3h-3zm2-20h3v3h-3zm0 6h3v3h-3zm-10 12h3v3h-3z"/></svg>');
        background-repeat: repeat;
        background-position: 0 0, 100px 150px, 200px 50px;
        filter: blur(5px);
    }

    /* Tarjeta principal estilo cristal translúcido */
    .block-container {
        position: relative;
        z-index: 1;
        background: rgba(14, 15, 30, 0.65);
        padding: 3rem;
        border-radius: 24px;
        box-shadow: 0 10px 40px rgba(0, 0, 0, 0.8);
        backdrop-filter: blur(16px);
        -webkit-backdrop-filter: blur(16px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        max-width: 650px;
        margin-top: 2rem;
    }

    h1 {
        color: #FFFFFF !important;
        text-shadow: 0 0 12px rgba(255, 255, 255, 0.5);
        font-weight: 800;
    }

    .stMarkdown p {
        color: #E2E8F0 !important;
        font-size: 1.1rem;
    }

    .stTextInput>div>div>input {
        background-color: rgba(10, 10, 26, 0.6) !important;
        color: white !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        border-radius: 12px !important;
        padding: 12px !important;
    }

    .stTextInput>div>div>input:focus {
        border-color: #FF0055 !important;
        box-shadow: 0 0 10px rgba(255, 0, 85, 0.5) !important;
    }

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

    .stImage img {
        border-radius: 16px;
        border: 2px solid rgba(255, 255, 255, 0.2);
    }
    </style>
""", unsafe_allow_html=True)

st.title("⚡ Generador de Códigos QR")
st.write("Crea tu código QR personalizado con un diseño moderno.")

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
