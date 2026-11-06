
import requests
import json

from pdf_extractor import extract_text_from_pdf


def extract_invoice_details(invoice_text):

    url = "http://localhost:11434/api/chat"

    prompt = f"""
Read the following invoice and extract its information.

Find these eight values:

1. invoice_number
2. vendor_name
3. customer_name
4. invoice_date
5. due_date
6. subtotal
7. gst_amount
8. total_amount

IMPORTANT:
- Look carefully through the invoice text.
- Extract the actual values written in the document.
- Do not return null if the value is present.
- Do not invent information.
- Use null only when a value is genuinely missing.
- Amounts must be numbers without currency symbols.

Return a JSON object with these exact keys:
invoice_number, vendor_name, customer_name,
invoice_date, due_date, subtotal, gst_amount,
total_amount.

INVOICE:
{invoice_text}
"""

    data = {
        "model": "llama3.2:1b",
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ],
        "format": "json",
        "stream": False,
        "options": {
            "temperature": 0,
            "num_predict": 500
        }
    }

    try:

        response = requests.post(
            url,
            json=data,
            timeout=180
        )

        response.raise_for_status()

        result = response.json()

        raw_response = result["message"]["content"]

        print("\nRAW LLAMA RESPONSE:")
        print(raw_response)

        extracted_data = json.loads(raw_response)

        return extracted_data

    except requests.exceptions.RequestException as error:

        print("Ollama error:", error)
        return None

    except (json.JSONDecodeError, KeyError) as error:

        print("JSON parsing error:", error)
        return None


if __name__ == "__main__":

    pdf_path = "sample_invoices/invoice.pdf"

    print("Reading invoice...\n")

    invoice_text = extract_text_from_pdf(pdf_path)

    print("Invoice text length:", len(invoice_text))

    print("\nSending invoice to Llama...\n")

    details = extract_invoice_details(invoice_text)

    if details:

        print("\nEXTRACTED INVOICE DETAILS")
        print("------------------------")

        print(json.dumps(details, indent=4))

    else:

        print("Extraction failed.")