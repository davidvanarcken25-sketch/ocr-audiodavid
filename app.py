import streamlit as st
import cv2
import numpy as np
import pytesseract
from PIL import Image
import io

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="Cyber OCR Scanner", page_icon="💠", layout="wide")

# --- ESTILO CIBERNÉTICO ---
st.markdown("""
    <style>
        [data-testid="stAppViewContainer"] {
            background: linear-gradient(135deg, #020024, #090979 40%, #00d4ff 100%);
            color: #d9faff;
        }
        [data-testid="stSidebar"] {
            background: linear-gradient(180deg, #00111f, #002d42);
            color: #d9faff;
        }
        [data-testid="stHeader"] {
            background: rgba(0, 0, 0, 0);
        }
        h1, h2, h3 {
            color: #00e5ff !important;
            text-shadow: 0 0 12px #00e5ff;
        }
        .stButton>button {
            background: linear-gradient(90deg, #00c6ff, #0072ff);
            color: white;
            border-radius: 10px;
            border: none;
            font-weight: bold;
            padding: 0.6em 1.3em;
            transition: all 0.3s ease;
            box-shadow: 0 0 12px #00e5ff;
        }
        .stButton>button:hover {
            transform: scale(1.05);
            box-shadow: 0 0 18px #00e5ff;
        }
        .stRadio label {
            color: #bffaff !important;
        }
        .stTextInput>div>div>input {
            background-color: rgba(0, 0, 20, 0.6);
            color: #00e5ff;
        }
    </style>
""", unsafe_allow_html=True)

# --- INTERFAZ ---
st.title("💠 Cyber OCR Scanner 💠")
st.subheader("Convierte imágenes en texto digital con estilo futurista ⚡")

with st.sidebar:
    st.header("⚙️ Opciones de escaneo")
    modo = st.radio("Fuente de imagen", ["Subir Imagen", "Capturar con Cámara"])
    filtros = st.checkbox("Aplicar realce de contraste", value=True)
    mostrar_cajas = st.checkbox("Mostrar cajas de texto detectado", value=True)

# --- CARGA DE IMAGEN ---
img = None
if modo == "Subir Imagen":
    uploaded_file = st.file_uploader("📂 Sube una imagen", type=["jpg", "jpeg", "png"])
    if uploaded_file:
        img = Image.open(uploaded_file)
elif modo == "Capturar con Cámara":
    camera_file = st.camera_input("📸 Captura una imagen")
    if camera_file:
        img = Image.open(camera_file)

# --- PROCESAMIENTO ---
if img is not None:
    st.image(img, caption="🧭 Imagen Original", use_container_width=True)
    img_cv = np.array(img)
    img_gray = cv2.cvtColor(img_cv, cv2.COLOR_RGB2GRAY)

    if filtros:
        img_gray = cv2.convertScaleAbs(img_gray, alpha=1.5, beta=30)

    # OCR con pytesseract
    data = pytesseract.image_to_data(img_gray, output_type=pytesseract.Output.DICT)
    text = " ".join(data["text"]).strip()

    # Dibuja cajas
    if mostrar_cajas:
        for i in range(len(data["text"])):
            if int(data["conf"][i]) > 60:  # confianza mínima
                (x, y, w, h) = (data["left"][i], data["top"][i], data["width"][i], data["height"][i])
                cv2.rectangle(img_cv, (x, y), (x + w, y + h), (0, 255, 255), 2)

    st.image(img_cv, caption="🔍 Resultado con detección", use_container_width=True)

    # Mostrar texto
    st.markdown("### 💾 Texto Detectado:")
    st.text_area("Texto extraído", text, height=200)

    # Opción para descargar el texto
    if text:
        buffer = io.BytesIO(text.encode('utf-8'))
        st.download_button("⬇️ Descargar texto", buffer, file_name="texto_detectado.txt")

else:
    st.info("👾 Sube o captura una imagen para comenzar el escaneo.")

