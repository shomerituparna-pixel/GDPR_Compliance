import fitz

pdf_path = "data/gdpr.pdf"

doc = fitz.open(pdf_path)

print(f"Total Pages: {len(doc)}")

text = ""

for page in doc:
    text += page.get_text()

#print(text[:2000])

with open(
    "data/gdpr.txt",
    "w",
    encoding="utf-8"
) as f:
    f.write(text)

print("GDPR text saved successfully!")