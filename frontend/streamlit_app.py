import requests
import streamlit as st

BACKEND_BASE_URL = "http://127.0.0.1:8080"

if "last_uploaded_file" not in st.session_state:
    st.session_state.last_uploaded_file = None

st.set_page_config(
    page_title="Intellexa AI",
    layout="wide"
)

st.title("Intellexa AI")
st.subheader("Enterprise Knowledge Intelligence Platform")

uploaded_file = st.sidebar.file_uploader(
    "Upload PDF",
    type=["pdf"]
)

if (
    uploaded_file is not None
    and uploaded_file.name != st.session_state.last_uploaded_file
    ):
    files = {
        "file": (
            uploaded_file.name,
            uploaded_file,
            "application/pdf"
        )
    }

    response = requests.post(
        f"{BACKEND_BASE_URL}/upload",
        files=files
    )

    if response.status_code == 200:

        st.session_state.last_uploaded_file = uploaded_file.name

        st.sidebar.success(
            "File uploaded successfully"
        )

    else:
        st.sidebar.error("Upload failed")


question = st.text_input(
    "Ask a question about the document"
)

ask_button = st.button("Ask")

if ask_button and question:

    payload = {
        "question": question
    }

    response = requests.post(
        f"{BACKEND_BASE_URL}/query",
        json=payload
    )

    if response.status_code == 200:

        data = response.json()

        st.subheader("Answer")
        st.write(data["answer"])

        st.subheader("Retrieved Chunks")

        for chunk in data["retrieved_chunks"]:
            st.info(chunk)

    else:
        st.error("Query failed")