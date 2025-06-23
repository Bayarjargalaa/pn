import pandas as pd
from pathlib import Path
import streamlit as st

# Файлын зам
BASE_DIR = Path(__file__).resolve().parent
file_path = BASE_DIR.parent / "data" / "ЕЖ.xlsx"

# Excel файл унших
df = pd.read_excel(file_path)

# 11-р эхэлсэн харилцахын Дебет талын мөрүүдийг шүүх
df_debet = df[df["Дебет"].astype(str).str.startswith("11")]

# Дебет талын харилцах болон Кредит талын харилцахаар бүлэглэж, Дүн баганын нийлбэрийг авах
if "Дебет" in df_debet.columns and "Кредит" in df_debet.columns and "Дүн" in df_debet.columns:
    grouped = (
        df_debet
        .groupby(["Дебет", "Кредит"])["Дүн"]
        .sum()
        .reset_index()
    )
    
    total_row = pd.DataFrame([{
        "Дебет": "Нийт",
        "Кредит": "",
        "Дүн": grouped["Дүн"].sum()
    }])
    grouped_with_total = pd.concat([grouped, total_row], ignore_index=True)
    
    st.subheader("11-р эхэлсэн харилцахын Дебет тал, харгалзах Кредит талын нийлбэр")
    st.dataframe(
        grouped_with_total.style.format({"Дүн": "{:,.0f}"}),
        use_container_width=True
    )
else:
    st.warning("Дебет харилцах, Кредит харилцах эсвэл Дүн багана олдсонгүй. Файлын бүтэц шалгана уу.")
    
    
    
import pandas as pd
from pathlib import Path
import streamlit as st

# Файлын зам
BASE_DIR = Path(__file__).resolve().parent
file_path = BASE_DIR.parent / "data" / "ЕЖ.xlsx"

# Excel файл унших
df = pd.read_excel(file_path)

# 11-р эхэлсэн харилцахын Дебет талын мөрүүдийг шүүх
df_debet = df[df["Дебет"].astype(str).str.startswith("11")]

# Кредит талын 10 болон 11-р эхэлсэн дүнгүүдийг оруулахгүй
df_debet = df_debet[
    #     ~df_debet["Кредит"].astype(str).str.startswith("10")
    # & ~df_debet["Кредит"].astype(str).str.startswith("11")
    
     ~df_debet["Кредит"].astype(str).str.startswith("11")
]

# Дебет талын харилцах болон Кредит талын харилцахаар бүлэглэж, Дүн баганын нийлбэрийг авах
if "Дебет" in df_debet.columns and "Кредит" in df_debet.columns and "Дүн" in df_debet.columns:
    grouped = (
        df_debet
        .groupby(["Дебет", "Кредит"])["Дүн"]
        .sum()
        .reset_index()
    )
    # Хөл дүн нэмэх
    total_row = pd.DataFrame([{
        "Дебет": "Нийт",
        "Кредит": "",
        "Дүн": grouped["Дүн"].sum()
    }])
    grouped_with_total = pd.concat([grouped, total_row], ignore_index=True)

    st.subheader("11-р эхэлсэн харилцахын Дебет тал, харгалзах Кредит талын нийлбэр (11-р эхэлсэн Кредит хассан)")
    st.dataframe(
        grouped_with_total.style.format({"Дүн": "{:,.0f}"}),
        use_container_width=True
    )
else:
    st.warning("Дебет, Кредит эсвэл Дүн багана олдсонгүй. Файлын бүтэц шалгана уу.")
    
    
    
import pandas as pd
from pathlib import Path
import streamlit as st

# Файлын зам
BASE_DIR = Path(__file__).resolve().parent
file_path = BASE_DIR.parent / "data" / "Харилцах евро зарлага.xlsx"

# Excel файл унших
df = pd.read_excel(file_path)

# Харилцагч байхгүй мөрүүдэд "Харилцагчгүй" гэж онооно
if "Харилцагчийн нэр" in df.columns and "Кредит" in df.columns:
    df["Харилцагчийн нэр"] = df["Харилцагчийн нэр"].fillna("Харилцагчгүй")
    grouped = df.groupby("Харилцагчийн нэр")["Кредит"].sum().reset_index()
    # Хөл дүн нэмэх
    total_row = pd.DataFrame([{
        "Харилцагчийн нэр": "Нийт",
        "Кредит": grouped["Кредит"].sum()
    }])
    grouped_with_total = pd.concat([grouped, total_row], ignore_index=True)
    st.subheader("Харилцагчийн нэрээр бүлэглэсэн евро зарлагын Кредит дүн (хөл дүнтэй)")
    st.dataframe(grouped_with_total.style.format({"Кредит": "{:,.2f}"}), use_container_width=True)
else:
    st.warning("'Харилцагчийн нэр' эсвэл 'Кредит' багана олдсонгүй.")