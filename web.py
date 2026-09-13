import streamlit as st
import qrcode
from io import BytesIO

# Configuración de página
st.set_page_config(page_title="Generador QR", page_icon="⚡", layout="centered")

# CSS personalizado: Fondo con QR desenfocados y tarjeta de cristal translúcida
st.markdown("""
    <style>
    /* Fondo que utiliza un patrón de QRs desenfocados y oscurecidos en tonos neón */
    .stApp {
        background: linear-gradient(rgba(10, 10, 26, 0.88), rgba(15, 12, 35, 0.9)),
                    url('https://images.unsplash.com/photo-1526374965328-7f61d4dc18c5?q=80&w=1920&auto=format&fit=crop');
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
        filter: backdrop-blur(8px); /* Aplica un desenfoque extra al fondo */
    }

    /* Tarjeta principal estilo Glassmorphism */
    .block-container {
        background: rgba(18, 18, 38, 0.75);
        padding: 3rem;
        border-radius: 24px;
        box-shadow: 0 10px 40px rgba(0, 0, 0, 0.9);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border: 1px solid rgba(0, 240, 255, 0.25);
        max-width: 650px;
        margin-top: 2rem;
    }

    /* Título llamativo con glow */
    h1 {
        color: #00F0FF !important;
        text-shadow: 0 0 15px rgba(0, 240, 255, 0.6);
        font-weight: 800;
    }

    /* Estilo para los textos informativos */
    .stMarkdown p {
        color: #E2E8F0 !important;
        font-size: 1.1rem;
    }

    /* Cuadro de texto personalizado */
    .stTextInput>div>div>input {
        background-color: rgba(10, 10, 26, 0.6) !important;
        color: white !important;
        border: 1px solid rgba(0, 240, 255, 0.4) !important;
        border-radius: 12px !important;
        padding: 12px !important;
    }
    
    .stTextInput>div>div>input:focus {
        border-color: #FF0055 !important;
        box-shadow: 0 0 10px rgba(255, 0, 85, 0.5) !important;
    }

    /* Botón principal llamativo neón */
    div.stButton > button:first-child {
        background: linear-gradient(90deg, #FF0055 0%, #7928CA 100%);
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
        color: white !important;
    }

    /* Imagen generada */
    .stImage img {
        border-radius: 16px;
        border: 2px solid rgba(0, 240, 255, 0.3);
    }
    </style>
""", unsafe_allow_html=True)

st.title("⚡ Generador de Códigos QR")
st.write("Crea tu código QR personalizado en segundos con el mejor diseño moderno.")

# Entrada de texto (URL o contenido)
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

        # Genera el código en su versión llamativa predeterminada (Azul eléctrico sobre fondo oscuro)
        img = qr.make_image(fill_color="#00F0FF", back_color="#121226")

        # Conversión de la imagen a Bytes
        buffer = BytesIO()
        img.save(buffer, format="PNG")
        byte_im = buffer.getvalue()

        # Mostrar el resultado final
        st.image(byte_im, caption="✨ Tu código QR generado", width=300)
        
        st.download_button(
            label="📥 Descargar Código QR",
            data=byte_im,
            file_name="codigo_qr.png",
            mime="image/png"
        )
    else:
        st.warning("⚠️ Por favor ingresa un enlace o texto antes de generar.")
