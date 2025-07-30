import os
from pathlib import Path
import pandas as pd
import streamlit as st

# 📌 Одоогийн Python скрипт байрлаж буй хавтас
BASE_DIR = Path(__file__).resolve().parent

# 📌 data хавтас дахь файлын зам
file_path = BASE_DIR.parent / "data" / "ЕЖ.xlsx"
print(f"Файл байрлах зам: {file_path}")

st.set_page_config(page_title="Сар бүрийн ашиг алдагдлын тайлан", layout="centered")

df = pd.read_excel(file_path)

# 70, 71, 87, 88, 91 дансны дебет талын нийлбэрийг гаргах
debet_starts = ["70", "71", "87", "88", "91"]
df["Дебет"] = df["Дебет"].astype(str)
filtered = df[df["Дебет"].str[:2].isin(debet_starts)]

if "Дебет" in filtered.columns and "Дүн" in filtered.columns:
    grouped = filtered.groupby("Дебет")["Дүн"].sum().reset_index()
    total_row = pd.DataFrame([{
        "Дебет": "Нийт",
        "Дүн": grouped["Дүн"].sum()
    }])
    grouped_with_total = pd.concat([grouped, total_row], ignore_index=True)
    st.subheader("70, 71, 87, 88, 91 дансны дебет талын нийлбэр")
    st.dataframe(grouped_with_total.style.format({"Дүн": "{:,.2f}"}), use_container_width=True)
else:
    st.warning("Дебет эсвэл Дүн багана олдсонгүй. Файлын бүтэц шалгана уу.")



# 70, 71, 87, 88, 91 данснуудтай харьцсан кредит дүнг дебетээр бүлэглэж, дүнг гаргах
debet_starts = ["70", "71", "87", "88", "91"]
df["Кредит"] = df["Кредит"].astype(str)
df["Дебет"] = df["Дебет"].astype(str)

# Зөвхөн дебет тал нь 70, 71, 87, 88, 91-р эхэлсэн мөрүүдийг сонгоно
df_credit = df[df["Дебет"].str[:2].isin(debet_starts)]

if "Кредит" in df_credit.columns and "Дебет" in df_credit.columns and "Дүн" in df_credit.columns:
    grouped_credit = (
        df_credit
        .groupby([ "Дебет", "Кредит"])["Дүн"]
        .sum()
        .reset_index()
    )
    # Хөл дүн нэмэх
    total_row_credit = pd.DataFrame([{
        "Кредит": "Нийт",
        "Дебет": "",
        "Дүн": grouped_credit["Дүн"].sum()
    }])
    grouped_credit_with_total = pd.concat([grouped_credit, total_row_credit], ignore_index=True)

    st.subheader("Кредит талын харилцах болон 70, 71, 87, 88, 91-р эхэлсэн дебет талын нийлбэр")
    st.dataframe(
        grouped_credit_with_total.style.format({"Дүн": "{:,.0f}"}),
        use_container_width=True
    )
else:
    st.warning("Кредит, Дебет эсвэл Дүн багана олдсонгүй. Файлын бүтэц шалгана уу.")