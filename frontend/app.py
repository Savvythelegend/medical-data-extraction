import streamlit as st
import requests

st.title("OCR Application")
st.write("Upload a file to extract text using OCR.")

uploaded_file = st.file_uploader("Choose a file...", type=["pdf", "png", "jpg", "jpeg"])

# ask user for file format required by backend
file_format = st.selectbox("Select file format", ["patient_details", "prescription"])

if uploaded_file and st.button("Extract"):
    # FastAPI endpoint
    url = "http://127.0.0.1:8000/extractor"

    # prepare multipart form-data
    files = {
        "file": (uploaded_file.name, uploaded_file, uploaded_file.type)
    }
    data = {
        "file_format": file_format
    }

    with st.spinner("Extracting..."):
        response = requests.post(url, data=data, files=files)

    if response.status_code == 200:
        result = response.json()
        if result.get("success"):
            st.subheader("Extraction Result:")
            st.json(result["data"])
        else:
            st.error("Error: " + result.get("error", "Unknown error"))
    else:
        st.error("Failed to reach backend API.")
