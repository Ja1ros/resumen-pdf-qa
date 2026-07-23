import streamlit as st
from pypdf import PdfReader
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(page_title="Resumen PDF + Q&A", page_icon="📚")
st.title("📚 Generador de Resumenes de PDF con Preguntas y Respuestas")
st.write("Sube un documento PDF para obtener un resumen automatico y luego hacer preguntas sobre su contenido.")

api_key = st.sidebar.text_input("OpenAI API Key", type="password")
uploaded_file = st.file_uploader("Sube un archivo PDF", type="pdf")

if "document_text" not in st.session_state:
    st.session_state.document_text = None
if "summary" not in st.session_state:
    st.session_state.summary = None
if "messages" not in st.session_state:
    st.session_state.messages = []


def extract_text(file) -> str:
    reader = PdfReader(file)
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""
    return text


def summarize(client, text):
    truncated = text[:12000]
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Eres un asistente que resume documentos de forma clara y concisa en espanol."},
            {"role": "user", "content": f"Resume el siguiente documento en maximo 200 palabras:\n\n{truncated}"},
        ],
        temperature=0.3,
    )
    return response.choices[0].message.content


if uploaded_file and api_key and st.session_state.document_text is None:
    with st.spinner("Extrayendo texto del PDF..."):
        st.session_state.document_text = extract_text(uploaded_file)
    client = OpenAI(api_key=api_key)
    with st.spinner("Generando resumen..."):
        st.session_state.summary = summarize(client, st.session_state.document_text)

if st.session_state.summary:
    st.subheader("Resumen")
    st.write(st.session_state.summary)
    st.divider()
    st.subheader("Preguntas sobre el documento")

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    question = st.chat_input("Escribe tu pregunta sobre el documento")
    if question:
        client = OpenAI(api_key=api_key)
        st.session_state.messages.append({"role": "user", "content": question})
        with st.spinner("Pensando..."):
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "Responde preguntas basandote unicamente en el siguiente documento."},
                    {"role": "user", "content": f"Documento:\n{st.session_state.document_text[:12000]}\n\nPregunta: {question}"},
                ],
                temperature=0.2,
            )
            answer = response.choices[0].message.content
        st.session_state.messages.append({"role": "assistant", "content": answer})
        st.rerun()
else:
    st.info("Sube un PDF y proporciona tu API Key para comenzar.")
