
import pymupdf


def extract_text_from_pdf(pdf_path):

    document = pymupdf.open(pdf_path)

    extracted_text = ""

    for page_number, page in enumerate(document):

        text = page.get_text()

        extracted_text += f"\n--- Page {page_number + 1} ---\n"
        extracted_text += text

    document.close()

    return extracted_text


if __name__ == "__main__":

    pdf_path = "sample_invoices/invoice.pdf"

    text = extract_text_from_pdf(pdf_path)

    print("\nExtracted Invoice Text:")
    print("-----------------------")

    print(text)