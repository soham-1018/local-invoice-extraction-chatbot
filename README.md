# Local AI-Powered Invoice Extraction Chatbot

A locally running PDF invoice extraction and question-answering chatbot built using Python, Streamlit, Ollama and Llama 3.2 1B.

## 1. Project Overview

This application allows users to:

- Upload PDF invoices.
- Extract invoice text.
- Extract structured invoice information using a locally running Llama model.
- Display extracted information in a user-friendly interface.
- Download extracted information as JSON.
- Ask questions about the uploaded invoice.

All LLM processing happens locally using Ollama. No cloud-based LLM API is required.

## 2. Technology Stack

| Technology | Purpose |
|---|---|
| Python 3.12 | Programming language |
| VS Code | Development environment |
| Ollama | Local LLM runtime |
| Llama 3.2 1B | Invoice information extraction |
| PyMuPDF | PDF text extraction |
| Streamlit | Web interface |
| Requests | Communication with Ollama API |
| Pydantic | Data validation dependency |

## 3. Prerequisites

Install the following software:

1. Python 3.12: https://www.python.org/downloads/
2. Visual Studio Code: https://code.visualstudio.com/
3. Ollama for Windows: https://ollama.com/download/windows
4. Git: https://git-scm.com/downloads

During Python installation, enable **Add Python to PATH**.

## 4. Download the Project

Clone the repository:

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
```

Navigate into the project:

```bash
cd local-invoice-extraction-chatbot
```

Alternatively, download the repository as a ZIP file from GitHub and extract it.

Open the folder in VS Code.

## 5. Create a Python Virtual Environment

Open the VS Code terminal.

Create the environment:

```powershell
py -3.12 -m venv myenv
```

Activate it:

```powershell
.\myenv\Scripts\Activate.ps1
```

If PowerShell blocks script execution, run:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

Then activate the environment again:

```powershell
.\myenv\Scripts\Activate.ps1
```

Upgrade pip:

```powershell
python -m pip install --upgrade pip
```

## 6. Install Python Dependencies

Make sure the virtual environment is activated.

Run:

```powershell
pip install -r requirements.txt
```

This installs all required Python packages.

## 7. Install and Configure Ollama

Download and install Ollama for Windows:

https://ollama.com/download/windows

Verify installation:

```powershell
ollama --version
```

Download the Llama model:

```powershell
ollama pull llama3.2:1b
```

This downloads the model to the local machine.

Verify that the model is available:

```powershell
ollama list
```

Expected model:

```text
llama3.2:1b
```

Ollama runs as a local service. Ensure it is running before starting the application.

The local API endpoint is:

```text
http://localhost:11434
```

## 8. Run the Application

From the project directory, with the virtual environment activated, run:

```powershell
streamlit run app.py
```

The application should open in your browser.

If it does not open automatically, visit:

http://localhost:8501

## 9. How to Use

1. Open the Invoice AI Assistant.
2. Upload a PDF invoice.
3. Click **Extract Invoice Details**.
4. Wait for Llama to process the invoice.
5. View the extracted invoice information.
6. Expand the JSON section to inspect structured output.
7. Download the extracted JSON.
8. Ask questions about the uploaded invoice using the chat interface.

## 10. Extracted Invoice Fields

The application currently extracts:

- Invoice number
- Vendor name
- Customer name
- Invoice date
- Due date
- Subtotal
- GST amount
- Total amount

## 11. Project Limitations

- Currently supports one invoice at a time.
- Initial PDF extraction supports text-based PDFs.
- Scanned PDFs require OCR support, which is not yet implemented.
- Extraction accuracy depends on the PDF layout and LLM performance.
- Conversation history is not currently supported.
- The model requires sufficient local RAM and disk space.

## 12. Troubleshooting

**Ollama connection error**

Make sure Ollama is installed and running. Check:

```powershell
ollama list
```

**Model not found**

Run:

```powershell
ollama pull llama3.2:1b
```

**Python module not found**

Activate the virtual environment and run:

```powershell
pip install -r requirements.txt
```

**PDF extraction returns empty text**

The PDF may be scanned or image-based. The current version requires OCR for such documents.

**Port 8501 already in use**

Run:

```powershell
streamlit run app.py --server.port 8502
```

## 13. Privacy

The application sends invoice text to the locally running Ollama service on the same machine. It does not require an external LLM API.

Use only sample or authorized invoice documents. Avoid uploading confidential company or customer documents to public repositories.

---

**Project:** Local AI-Powered Invoice Extraction Chatbot  
**Model:** Llama 3.2 1B  
**Runtime:** Ollama  
**Interface:** Streamlit