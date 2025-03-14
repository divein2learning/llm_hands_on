import re

from pdfminer.high_level import extract_text


def parse_pdf_with_pdfminer(pdf_path):
    return extract_text(pdf_path)


def clean_text(text):
    text = re.sub(r"\s+", " ", text)  # 去除多余空白
    text = re.sub(r"\n", " ", text)  # 替换换行符
    return text.strip()


def chunk_text(text, chunk_size=200):
    words = text.split()
    chunks = [
        " ".join(words[i : i + chunk_size]) for i in range(0, len(words), chunk_size)
    ]
    return chunks


def get_chunks(pdf_path, chunk_size=50):
    pdf_content = parse_pdf_with_pdfminer(pdf_path)
    pdf_content = clean_text(pdf_content)
    chunks = chunk_text(pdf_content, chunk_size=chunk_size)
    return chunks


if __name__ == "__main__":
    pdf_path = r"D:\learn\文献\文献\Bias in error estimation when using cross-validation for model.pdf"
    text = parse_pdf_with_pdfminer(pdf_path)
    print("=========origin============", text[:100])
    cleaned_text = clean_text(text)
    print("==========after clean===========", cleaned_text[:100])
    chunks = chunk_text(cleaned_text)

    print("==========chunks===========")
    for chunk in chunks[:3]:
        print(chunk)
