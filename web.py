import streamlit as st
import qrcode
from PIL import Image
import io

st.set_page_config(page_title="Generador QR", page_icon="📱", layout="centered")

st.title("📱 Generador de Códigos QR")
st.write("Ingresa texto, un enlace o cualquier información para crear un código QR listo para escanear.")

contenido = st.text_input("Contenido del QR:", placeholder="Ej. https://misitio.com o Hola mundo")

if st.button("Generar QR", type="primary"):
    if contenido.strip():
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=10,
            border=2,
        )
        qr.add_data(contenido)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white").convert('RGB')

        st.image(img, caption="Tu código QR generado", width=250)

        buf = io.BytesIO()
        img.save(buf, format="PNG")
        byte_im = buf.getvalue()

        st.download_button(
            label="💾 Descargar Código QR",
            data=byte_im,
            file_name="codigo_qr.png",
            mime="image/png"
        )
    else:
        st.warning("Por favor escribe algún texto antes de generar.")