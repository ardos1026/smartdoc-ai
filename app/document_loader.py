from pypdf import PdfReader


def load_document(file_path):
    if file_path.endswith(".txt"):
        with open(file_path, "r", encoding="utf-8") as file:
            return file.read()

    elif file_path.endswith(".pdf"):
        reader = PdfReader(file_path)

        text = ""

        for page in reader.pages:
            text += page.extract_text() or ""

        return text

    else:
        raise ValueError("Unsupported file type. Use .txt or .pdf")