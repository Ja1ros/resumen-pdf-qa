# Generador de Resumenes de PDF con Q&A

Aplicacion que genera un resumen automatico de un documento PDF y permite hacer preguntas sobre su contenido usando un LLM.

## Caracteristicas

- Extraccion de texto de archivos PDF.
- Resumen automatico de hasta 200 palabras.
- Sistema de preguntas y respuestas basado en el contenido del documento.
- Interfaz de chat para consultas adicionales.

## Stack tecnologico

- Python 3.10+
- Streamlit
- pypdf
- OpenAI API

## Instalacion

```bash
git clone https://github.com/Ja1ros/resumen-pdf-qa.git
cd resumen-pdf-qa
pip install -r requirements.txt
```

## Uso

```bash
streamlit run app.py
```

1. Ingresa tu API Key de OpenAI en la barra lateral.
2. Sube un documento PDF.
3. Revisa el resumen generado.
4. Haz preguntas adicionales sobre el contenido.

## Variables de entorno

Crea un archivo `.env` basado en `.env.example` si prefieres no ingresar la API Key manualmente.

## Proximas mejoras

- Exportar el resumen a PDF o Word.
- Soporte para documentos muy extensos mediante chunking.
- Despliegue en Streamlit Cloud.

## Licencia

Proyecto con fines educativos y de portafolio.
