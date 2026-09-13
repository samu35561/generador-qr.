import streamlit as st
import qrcode
from io import BytesIO

# Configuración de página
st.set_page_config(page_title="Generador QR", page_icon="⚡", layout="centered")

# CSS personalizado: Fondo exacto de la imagen con QRs gigantes desenfocados
st.markdown("""
    <style>
    /* Fondo oscuro base */
    .stApp {
        background: radial-gradient(circle at 20% 30%, #0c0822 0%, #060514 100%);
        overflow-x: hidden;
    }

    /* Patrón exacto de QRs gigantes coloridos desenfocados */
    .stApp::before {
        content: "";
        position: fixed;
        top: 0; left: 0; width: 100vw; height: 100vh;
        z-index: 0;
        pointer-events: none;
        opacity: 0.45;
        background-image: 
            /* QR Verde Neón gigante (Izquierda) */
            url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" width="600" height="600" viewBox="0 0 29 29" fill="%2300ff66"><path d="M0 0h7v7H0zm2 2v3h3V2zm0 8h3v3H2zm8-10h7v7h-7zm2 2v3h3V2zm10-2h7v7h-7zm2 2v3h3V2zm-12 8h3v3h-3zm8 0h3v3h-3zm-6 6h3v3h-3zm8 0h3v3h-3zm-10 6h3v3H0zm4 0h3v3H4zm6 0h3v3h-3zm6 0h3v3h-3zm6-12h3v3h-3zm0 6h3v3h-3zm0 6h3v3h-3zm-14 4h3v3H8zm6 0h3v3h-3zm6 0h3v3h-3zm2-20h3v3h-3zm0 6h3v3h-3zm-10 12h3v3h-3z"/></svg>'),
            /* QR Cyan / Azul neón gigante (Derecha) */
            url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" width="700" height="700" viewBox="0 0 29 29" fill="%2300f0ff"><path d="M0 0h7v7H0zm2 2v3h3V2zm0 8h3v3H2zm8-10h7v7h-7zm2 2v3h3V2zm10-2h7v7h-7zm2 2v3h3V2zm-12 8h3v3h-3zm8 0h3v3h-3zm-6 6h3v3h-3zm8 0h3v3h-3zm-10 6h3v3H0zm4 0h3v3H4zm6 0h3v3h-3zm6 0h3v3h-3zm6-12h3v3h-3zm0 6h3v3h-3zm0 6h3v3h-3zm-14 4h3v3H8zm6 0h3v3h-3zm6 0h3v3h-3zm2-20h3v3h-3zm0 6h3v3h-3zm-10 12h3v3h-3z"/></svg>'),
            /* QR Magenta/Morado neón gigante (Abajo) */
            url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" width="550" height="550" viewBox="0 0 29 29" fill="%23d900ff"><path d="M0 0h7v7H0zm2 2v3h3V2zm0 8h3v3H2zm8-10h7v7h-7zm2 2v3h3V2zm10-2h7v7h-7zm2 2v3h3V2zm-12 8h3v3h-3zm8 0h3v3h-3zm-6 6h3v3h-3zm8 0h3v3h-3zm-10 6h3v3H0zm4 0h3v3H4zm6 0h3v3h-3zm6 0h3v3h-3zm6-12h3v3h-3zm0 6h3v3h-3zm0 6h3v3h-3zm-14 4h3v3H8zm6 0h3v3h-3zm6 0h3v3h-3zm2-20h3v3h-3zm0 6h3v3h-3zm-10 12h3v3h-3z"/></svg>');
        background-repeat: no-repeat;
        background-position: 
            -180px 30%,      /* Verde Neón */
            115% 10%,       /* Cyan */
            50% 115%;       /* Magenta */
        filter: blur(8px);  /* Desenfoque pronunciado */
    }

    /* Tarjeta translúcida estilo Glassmorphism */
    .block-container {
        position: relative;
        z-index: 1;
        background: rgba(14, 15, 30, 0.45);
        padding: 3rem;
        border-radius: 24px;
        box-shadow: 0 10px 40px rgba(0, 0, 0, 0.7);
        backdrop-filter: blur(14px);
        -webkit-backdrop-filter: blur(14px);
        border: 1px solid rgba(255, 255, 255, 0.08);
        max-width: 650px;
        margin-top: 2rem;
    }

    /* Título principal con brillo neón */
    h1 {
        color: #FFFFFF !important;
        text-shadow: 0 0 12px rgba(255, 255, 255, 0.6);
        font-weight: 700;
    }

    /* Texto secundario */
    .stMarkdown p {
        color: #CCCCCC !important;
    }

    /* Entrada de texto */
    .stTextInput>div>div>input {
        background-color: rgba(22, 22, 38, 0.6) !important;
        color: white !important;
        border: 1px solid rgba(255, 255, 255, 0.15) !important;
        border-radius: 12px !important;
        padding: 12px !important;
    }

    .stTextInput>div>div>input:focus {
        border-color: #FF0055 !important;
        box-shadow: 0 0 12px rgba(255, 0, 85, 0.4) !important;
    }

    /* Botón principal (Fucsia neón) */
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

    /* Imagen del QR final */
    .stImage img {
        border-radius: 16px;
        margin-top: 1.5rem;
        border: 2px solid rgba(255, 255, 255, 0.1);
    }
    </style>
""", unsafe_allow_html=True)

st.title("⚡ Generador de Códigos QR")
st.write("Crea tu código QR personalizado con un diseño moderno.")

# Entrada de texto única
url = st.text_input("🔗 Contenido o enlace del QR:", value="hola")

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

        # Genera el QR estándar en blanco y negro
        img = qr.make_image(fill_color="black", back_color="white")

        buffer = BytesIO()
        img.save(buffer, format="PNG")
        byte_im = buffer.getvalue()

        st.image(byte_im, caption="✨ Tu código QR generado", width=260)
        
        st.download_button(
            label="📥 Descargar Código QR",
            data=byte_im,
            file_name="codigo_qr.png",
            mime="image/png"
        )
    else:
        st.warning("⚠️ Por favor ingresa un enlace o texto antes de generar.")
