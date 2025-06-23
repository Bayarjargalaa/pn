import pdfplumber
import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
file_path = BASE_DIR.parent / 'PN' / "data" / "All stsrs ТНА.pdf"
excel_path = BASE_DIR.parent / 'PN' / "data" / "output.xlsx"

tables = []

with pdfplumber.open(file_path) as pdf:
    for page in pdf.pages:
        table = page.extract_table()
        if table:
            tables.extend(table)

if tables:
    df = pd.DataFrame(tables[1:], columns=tables[0])  # Эхний мөрийг толгой гэж үзнэ
    df.to_excel(excel_path, index=False)
    print(f"Excel файл үүсгэлээ: {excel_path}")
else:
    print("PDF-ээс хүснэгт олдсонгүй. PDF файлд хүснэгт байгаа эсэхийг шалгана уу.")
print(f"Excel файл үүсгэлээ: {excel_path}")