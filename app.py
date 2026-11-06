
import streamlit as st
import tempfile
import os
import json

from pdf_extractor import extract_text_from_pdf
from llm_extractor import extract_invoice_details


# Page configuration
st.set_page_config(
    page_title="Invoice AI Assistant",
    page_icon="📄",
    layout="wide"
)


# Title
st.title("📄 Invoice AI Assistant")

st.write(
    "Upload a PDF invoice and extract structured information "
    "using a locally running Llama model."
)

st.caption("Powered by Ollama + Llama 3.2 1B")


# Initialize session state
if "invoice_data" not in st.session_state:
    st.session_state.invoice_data = None

if "invoice_text" not in st.session_state:
    st.session_state.invoice_text = None

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []


# PDF upload
uploaded_file = st.file_uploader(
    "Upload your invoice PDF",
    type=["pdf"]
)


if uploaded_file is not None:

    st.success(f"Uploaded: {uploaded_file.name}")

    if st.button("Extract Invoice Details"):

        try:

            # Save uploaded PDF temporarily
            with tempfile.NamedTemporaryFile(
                delete=False,
                suffix=".pdf"
            ) as temp_file:

                temp_file.write(uploaded_file.getvalue())

                temp_path = temp_file.name

            with st.spinner("Reading PDF..."):

                invoice_text = extract_text_from_pdf(temp_path)

            # Remove temporary file
            os.remove(temp_path)

            if not invoice_text.strip():

                st.error(
                    "No text found in this PDF. "
                    "It may be a scanned document."
                )

            else:

                with st.spinner(
                    "Llama is extracting invoice information..."
                ):

                    invoice_data = extract_invoice_details(
                        invoice_text
                    )

                if invoice_data:

                    st.session_state.invoice_data = invoice_data

                    st.session_state.invoice_text = invoice_text

                    st.session_state.chat_history = []

                    st.success("Invoice extraction completed!")

                else:

                    st.error("Invoice extraction failed.")

        except Exception as error:

            st.error(f"An error occurred: {error}")

        finally:

            if "temp_path" in locals() and os.path.exists(temp_path):
                os.remove(temp_path)


# Display extracted information
if st.session_state.invoice_data:

    st.divider()

    st.subheader("Extracted Invoice Details")

    invoice_data = st.session_state.invoice_data

    # Display fields
    col1, col2 = st.columns(2)

    fields = list(invoice_data.items())

    for index, (key, value) in enumerate(fields):

        with [col1, col2][index % 2]:

            st.metric(
                label=key.replace("_", " ").title(),
                value=str(value) if value is not None else "Not found"
            )

    # JSON output
    with st.expander("View extracted JSON"):

        st.json(invoice_data)

    # Download JSON
    json_data = json.dumps(
        invoice_data,
        indent=4,
        ensure_ascii=False
    )

    st.download_button(
        label="Download JSON",
        data=json_data,
        file_name="invoice_extracted.json",
        mime="application/json"
    )

    st.divider()

    # Chatbot section
    st.subheader("💬 Chat with your Invoice")

    # Display previous messages
    for message in st.session_state.chat_history:

        with st.chat_message(message["role"]):

            st.write(message["content"])

    # User input
    user_question = st.chat_input(
        "Ask something about this invoice..."
    )

    if user_question:

        st.session_state.chat_history.append(
            {
                "role": "user",
                "content": user_question
            }
        )

        with st.chat_message("user"):

            st.write(user_question)

        with st.chat_message("assistant"):

            with st.spinner("Thinking..."):

                try:

                    prompt = f"""
You are an invoice assistant.

Answer the user's question using ONLY the invoice information below.

Do not invent information.
If the answer is unavailable, say so.

INVOICE TEXT:
{st.session_state.invoice_text}

EXTRACTED DATA:
{json.dumps(st.session_state.invoice_data, ensure_ascii=False)}

USER QUESTION:
{user_question}
"""

                    import requests

                    response = requests.post(
                        "http://localhost:11434/api/chat",
                        json={
                            "model": "llama3.2:1b",
                            "messages": [
                                {
                                    "role": "user",
                                    "content": prompt
                                }
                            ],
                            "stream": False
                        },
                        timeout=180
                    )

                    response.raise_for_status()

                    answer = response.json()["message"]["content"]

                    st.write(answer)

                    st.session_state.chat_history.append(
                        {
                            "role": "assistant",
                            "content": answer
                        }
                    )

                except Exception as error:

                    st.error(f"Chat error: {error}")


else:

    st.info(
        "Upload an invoice PDF and click "
        "'Extract Invoice Details' to get started."
    )