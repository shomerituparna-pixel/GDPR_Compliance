from PyPDF2 import PdfReader

print("Script started")


def extract_pdf_text(pdf_path):
    print(f"Opening: {pdf_path}")

    reader = PdfReader(pdf_path)
    print(f"Pages found: {len(reader.pages)}")

    pages = []

    for i, page in enumerate(reader.pages):
        text = page.extract_text()
        print(f"Reading page {i + 1}")

        if text:
            pages.append(text)

    return "\n".join(pages)


if __name__ == "__main__":
    text = extract_pdf_text("data/GDPR.pdf")

    print("Characters extracted:", len(text))
    print(text[:1000])