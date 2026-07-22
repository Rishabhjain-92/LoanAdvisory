import os
import streamlit as st

from chatbot import ask_question
from pdf_loader import read_pdf
from text_splitter import split_text
from vector_store import create_vector_store


# ---------- PAGE CONFIGURATION ----------

st.set_page_config(
    page_title="AI Loan Advisory Chatbot",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ---------- SESSION STATE ----------

if "messages" not in st.session_state:
    st.session_state.messages = []

if "current_pdf" not in st.session_state:
    st.session_state.current_pdf = "loan_policy.pdf"


# ---------- SIDEBAR ----------

with st.sidebar:

    st.title("🏦 AI Loan Advisor")

    st.divider()

    st.subheader("📤 Upload Loan Policy")

    uploaded_file = st.file_uploader(
        "Choose a PDF file",
        type=["pdf"]
    )

    if uploaded_file is not None:

        if st.button(
            "Process PDF",
            use_container_width=True
        ):

            with st.spinner("Reading and processing the PDF..."):

                # Create the data folder if it does not exist
                os.makedirs("data", exist_ok=True)

                # Save the uploaded PDF
                file_path = os.path.join(
                    "data",
                    uploaded_file.name
                )

                with open(file_path, "wb") as file:

                    file.write(
                        uploaded_file.getbuffer()
                    )

                # Read PDF text
                text = read_pdf(file_path)

                # Split text into chunks
                chunks = split_text(text)

                # Create a new vector database
                create_vector_store(chunks)

                # Save current PDF name
                st.session_state.current_pdf = uploaded_file.name

                # Clear old chat messages
                st.session_state.messages = []

            st.success(
                "PDF processed successfully!"
            )


    st.divider()

    st.subheader("📄 Current PDF")

    st.info(
        st.session_state.current_pdf
    )


    st.divider()

    st.subheader("📊 Status")

    st.success(
        "✅ Vector Database Ready"
    )


    st.divider()

    if st.button(
        "🗑️ Clear Chat",
        use_container_width=True
    ):

        st.session_state.messages = []

        st.rerun()


# ---------- MAIN PAGE ----------

st.title("🏦 AI Loan Advisory Chatbot")

st.write(
    "Upload a loan policy PDF and ask questions about it."
)


# ---------- DISPLAY CHAT HISTORY ----------

for message in st.session_state.messages:

    with st.chat_message(
        message["role"]
    ):

        st.markdown(
            message["content"]
        )


# ---------- CHAT INPUT ----------

question = st.chat_input(
    "Ask your question here..."
)


if question:

    # Save user message

    st.session_state.messages.append(
        {
            "role": "user",
            "content": question
        }
    )


    # Display user message

    with st.chat_message("user"):

        st.markdown(question)


    # Generate chatbot response

    with st.chat_message("assistant"):

        with st.spinner(
            "Searching the loan policy..."
        ):

            answer, sources = ask_question(
                question
            )

            st.markdown(answer)

            with st.expander("📚 View Sources"):

                st.caption(
                    "These document sections were used to generate the answer."
                )

                for index, source in enumerate(
                    sources,
                    start=1
                ):

                    with st.expander(
                        f"📄 Source {index}"
                    ):

                        st.write(source)
    # Save chatbot response

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": answer
        }
    )