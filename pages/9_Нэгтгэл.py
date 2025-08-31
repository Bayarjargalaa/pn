import os
from pathlib import Path
import pandas as pd
import streamlit as st


# 📌 Одоогийн Python скрипт байрлаж буй хавтас
BASE_DIR = Path(__file__).resolve().parent

# 📌 data хавтас дахь файлын зам
file_path_c1 = BASE_DIR.parent / "data" / "PN тооцоо.xlsx"

# ✅ Excel файл унших
df_c1 = pd.read_excel(file_path_c1, sheet_name='Барааны С1 2023.03.17',)

# Хөл дүн тооцоолох (тоон багануудын нийлбэр)
numeric_cols = df_c1.select_dtypes(include="number").columns
total_row = pd.DataFrame([{
    **{col: df_c1[col].sum() for col in numeric_cols},
    **{col: "Нийт дүн" if col == "Нэр" else "" for col in df_c1.columns if col not in numeric_cols}
}])
df_c1_with_total = pd.concat([df_c1, total_row], ignore_index=True)

# 📊 Хүснэгтээр харуулах
# st.subheader("Барааны эхний үлдэгдэл 2023.03.17-ны байдлаар (хөл дүнтэй)")
# st.dataframe(df_c1_with_total, use_container_width=True)

# ...existing code...

# Зөвхөн "Нийт үлдэгдэл" баганын "Нийт дүн" гэсэн мөрийг харуулах
if "Нийт үлдэгдэл" in df_c1_with_total.columns:
    total_only = df_c1_with_total[df_c1_with_total["Нэр"] == "Нийт дүн"][["Нэр", "Нийт үлдэгдэл"]]
    st.subheader("Барааны нийт үлдэгдэл тоо ширхэгээр 2023.03.17-ны байдлаар")
    st.dataframe(total_only.style.format({"Нийт үлдэгдэл":"{:,.2f}"}), use_container_width=True)
else:
    st.warning("'Нийт үлдэгдэл' багана олдсонгүй.")