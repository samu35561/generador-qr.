import streamlit as st
import qrcode
from io import BytesIO

# Configuración de página
st.set_page_config(page_title="Generador QR", page_icon="⚡", layout="centered")

# CSS personalizado para agregar un fondo de pantalla con patrón de códigos QR
st.markdown("""
    <style>
    /* Fondo con patrón decorativo de marcas/patrones de QR */
    .stApp {
        background-color: #0f172a;
        background-image: radial-gradient(#334155 1px, transparent 1px), radial-gradient(#334155 1px, #0f172a 1px);
        background-size: 40px 40px;
        background-position: 0 0, 20px 20px;
    }

    /* Estilo para la caja principal del contenido */
    .block-container {
        background: rgba(30, 41, 59, 0.85);
        padding: 2.5rem;
        border-radius: 20px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.5);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1);
    }

    /* Estilo del botón principal */
    div.stButton > button:first-child {
        background-color: #FF0055;
        color: white;
        font-weight: bold;
        border-radius: 12px;
        border: none;
        padding: 12px 28px;
        font-size: 18px;
        width: 100%;
        transition: 0.3s;
    }
    div.stButton > button:first-child:hover {
        background-color: #FF3300;
        color: white;
        transform: translateY(-2px);
    }
    </style>
""", unsafe_allow_html=True)

st.title("⚡ Generador de Códigos QR")
st.write("Crea tu código QR personalizado con un diseño moderno.")

# Entrada de texto
url = st.text_input("🔗 Contenido o enlace del QR:", placeholder="Ej. https://misitio.com")

st.subheader("🎨 Personaliza los colores")

# Contenedor para elegir colores
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

        img = qr.make_image(fill_color=fill_color, back_color=back_color)

        buffer = BytesIO()
        img.save(buffer, format="PNG")
        byte_im = buffer.getvalue()

        st.image(byte_im, caption="✨ Tu código QR personalizado", width=300)
        
        st.download_button(
            label="📥 Descargar Código QR",
            data=byte_im,
            file_name="codigo_qr_personalizado.png",
            mime="image/png"
        )
    else:
        st.warning("⚠️ Por favor ingresa un enlace o texto antes de generar.")
