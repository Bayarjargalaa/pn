
import os
from pathlib import Path
import pandas as pd
import streamlit as st


# 📌 Одоогийн Python скрипт байрлаж буй хавтас
BASE_DIR = Path(__file__).resolve().parent

# 📌 data хавтас дахь файлын зам
file_path = BASE_DIR.parent / "data" / "2023,03,18-2025,5,31 борлуулалт.xlsx"
print(f"Файл байрлах зам: {file_path}")

st.set_page_config(page_title="Сар бүрийн ашиг алдагдлын тайлан", layout="centered")

df= pd.read_excel(file_path)

print(df.columns)

# ...existing code...

# Дансны нэрийг PN тооцоо.xlsx файлаас унших
accounts_file = BASE_DIR.parent / "data" / "PN тооцоо.xlsx"
accounts_df = pd.read_excel(accounts_file, sheet_name="дансны нэр")
# Дансны код болон нэрийг агуулсан баганыг зөв тохируулна уу!

accounts_df["Код"] = accounts_df["Код"].astype(str)





# "Харьцсан данс" баганаар бүлэглэж "Нийт" баганын дүнг гаргах
if "Кредит данс" in df.columns and "Кредит - ₮" in df.columns:
    grouped = df.groupby("Кредит данс")["Кредит - ₮"].sum().reset_index()
    grouped["Кредит данс"] = grouped["Кредит данс"].astype(str)
    accounts_df["Код"] = accounts_df["Код"].astype(str)
    
    
    
    grouped = grouped.merge(accounts_df[["Код", "Нэр"]], left_on="Кредит данс", right_on="Код", how="left")
    grouped["Данс"] = grouped["Кредит данс"] + " - " + grouped["Нэр"].fillna("")
    grouped = grouped[["Данс", "Кредит - ₮"]]    
    
    total_row = pd.DataFrame([{
        "Данс": "Кредит - ₮",
        "Кредит - ₮": grouped["Кредит - ₮"].sum()
    }])
    grouped_with_total = pd.concat([grouped, total_row], ignore_index=True)
    # st.subheader("📊 Борлуулалттай харьцсан кредит талын нийт")
    # st.dataframe(grouped_with_total.style.format({"Кредит - ₮": "{:,.2f}"}), use_container_width=True)
else:
    st.warning("Харьцсан данс эсвэл Нийт багана олдсонгүй.")
    

# "Харьцсан данс" баганаар бүлэглэж "Нийт" баганын дүнг гаргах
if "Дебет данс" in df.columns and "Дебет - ₮" in df.columns:
    grouped = df.groupby("Дебет данс")["Дебет - ₮"].sum().reset_index()
    grouped["Дебет данс"] = grouped["Дебет данс"].astype(str)
    accounts_df["Код"] = accounts_df["Код"].astype(str)
    grouped = grouped.merge(accounts_df[["Код", "Нэр"]], left_on="Дебет данс", right_on="Код", how="left")
    grouped["Данс"] = grouped["Дебет данс"] + " - " + grouped["Нэр"].fillna("")
    grouped = grouped[["Данс", "Дебет - ₮"]]
    # Хөл дүн нэмэх
    total_row = pd.DataFrame([{
        "Данс": "Дебет - ₮",
        "Дебет - ₮": grouped["Дебет - ₮"].sum()
    }])
    grouped_with_total = pd.concat([grouped, total_row], ignore_index=True)
    # st.subheader("📊 Борлуулалттай харьцсан дебет талын нийт")
    # st.dataframe(grouped_with_total.style.format({"Дебет - ₮": "{:,.2f}"}), use_container_width=True)
else:
    st.warning("Харьцсан данс эсвэл Нийт багана олдсонгүй.")


# "Харьцсан данс" баганаар бүлэглэж "Нийт" баганын дүнг гаргах
if "Дебет данс" in df.columns and "Дебет - ₮" in df.columns:
    # Зөвхөн 610101 - Борлуулсан бүтээгдэхүүний өртөг дансыг шүүх
    filtered_df = df[df["Дебет данс"].astype(str) == "610101"]
    grouped = filtered_df.groupby("Дебет данс")["Дебет - ₮"].sum().reset_index()
    grouped["Дебет данс"] = grouped["Дебет данс"].astype(str)
    accounts_df["Код"] = accounts_df["Код"].astype(str)
    grouped = grouped.merge(accounts_df[["Код", "Нэр"]], left_on="Дебет данс", right_on="Код", how="left")
    grouped["Данс"] = grouped["Дебет данс"] + " - " + grouped["Нэр"].fillna("")
    grouped = grouped[["Данс", "Дебет - ₮"]]
    # Хөл дүн нэмэх
    total_row = pd.DataFrame([{
        "Данс": "Дебет - ₮",
        "Дебет - ₮": grouped["Дебет - ₮"].sum()
    }])
    grouped_with_total = pd.concat([grouped, total_row], ignore_index=True)
    # st.subheader("📊 610101 - Борлуулсан бүтээгдэхүүний өртөг дансны дебет талын нийт")
    # st.dataframe(grouped_with_total.style.format({"Дебет - ₮": "{:,.2f}"}), use_container_width=True)
else:
    st.warning("Харьцсан данс эсвэл Нийт багана олдсонгүй.")




# Сонгох дансны жагсаалт
selected_accounts = ["310601", "311301", "510101"]

# ...existing code...

if "Кредит данс" in df.columns and "Кредит - ₮" in df.columns:
    filtered_df = df[df["Кредит данс"].astype(str).isin(selected_accounts)]
    grouped = filtered_df.groupby("Кредит данс")["Кредит - ₮"].sum().reset_index()
    # Төрлийг ижил болгоно
    grouped["Кредит данс"] = grouped["Кредит данс"].astype(str)
    accounts_df["Код"] = accounts_df["Код"].astype(str)
    # Дансны нэрийг нэмэх
    grouped = grouped.merge(accounts_df[["Код", "Нэр"]], left_on="Кредит данс", right_on="Код", how="left")
    grouped["Данс"] = grouped["Кредит данс"] + " - " + grouped["Нэр"].fillna("")
    grouped = grouped[["Данс", "Кредит - ₮"]]
    # Хөл дүн нэмэх
    total_row = pd.DataFrame([{
        "Данс": "Кредит - ₮",
        "Кредит - ₮": grouped["Кредит - ₮"].sum()
    }])
    grouped_with_total = pd.concat([grouped, total_row], ignore_index=True)
    st.subheader("Мөнгө болох борлуулалт")
    st.dataframe(grouped_with_total.style.format({"Кредит - ₮": "{:,.2f}"}), use_container_width=True)
else:
    st.warning("Кредит данс эсвэл Кредит - ₮ багана олдсонгүй.")
    
    
    
# Сонгох дансны жагсаалт
selected_accounts = ["100101", "100102", "120101", '310101', '340104']

# ...existing code...

if "Дебет данс" in df.columns and "Дебет - ₮" in df.columns:
    filtered_df = df[df["Дебет данс"].astype(str).isin(selected_accounts)]
    grouped = filtered_df.groupby("Дебет данс")["Дебет - ₮"].sum().reset_index()
    # Төрлийг ижил болгоно
    grouped["Дебет данс"] = grouped["Дебет данс"].astype(str)
    accounts_df["Код"] = accounts_df["Код"].astype(str)
    # Дансны нэрийг нэмэх
    grouped = grouped.merge(accounts_df[["Код", "Нэр"]], left_on="Дебет данс", right_on="Код", how="left")
    grouped["Данс"] = grouped["Дебет данс"] + " - " + grouped["Нэр"].fillna("")
    grouped = grouped[["Данс", "Дебет - ₮"]]
    # Хөл дүн нэмэх
    total_row = pd.DataFrame([{
        "Данс": "Дебет - ₮",
        "Дебет - ₮": grouped["Дебет - ₮"].sum()
    }])
    grouped_with_total = pd.concat([grouped, total_row], ignore_index=True)
    st.subheader("Борлуулалт дараах дансанд орсон")
    st.dataframe(grouped_with_total.style.format({"Дебет - ₮": "{:,.2f}"}), use_container_width=True)
else:
    st.warning("Дебет данс эсвэл Дебет - ₮ багана олдсонгүй.")
    
    
import pandas as pd
from pathlib import Path

# ЕЖ.xlsx файлын зам
BASE_DIR = Path(__file__).resolve().parent
ej_file = BASE_DIR.parent / "data" / "ЕЖ.xlsx"

# ЕЖ.xlsx-ээс дата унших
df_ej = pd.read_excel(ej_file)

# 100101 дансны кредит талын дүнг тооцоолох
if "Дүн" in df_ej.columns and "Кредит" in df_ej.columns:
    # Дебет баганаар бүлэглэж, дүнг гаргах
    debit_grouped = (
        df_ej[df_ej["Кредит"].astype(str) == "100101 - Касс дахь мөнгө /Дэлгүүр/"]
        .groupby("Дебет")["Дүн"].sum().reset_index()
    )
    # Хөл дүн нэмэх
    total_row = pd.DataFrame([{
        "Дебет": "Нийт",
        "Дүн": debit_grouped["Дүн"].sum()
    }])
    debit_grouped_with_total = pd.concat([debit_grouped, total_row], ignore_index=True)
    st.subheader("100101 дэлгүүрийн касс дансны кредит талд орсон гүйлгээг дебетээр бүлэглэсэн дүн")
    st.dataframe(debit_grouped_with_total.style.format({"Дүн": "{:,.0f}"}), use_container_width=True)
else:
    st.warning("ЕЖ.xlsx файлд 'Кредит' эсвэл 'Дүн' багана олдсонгүй.")
    
    
    
# 100102 дансны кредит талын дүнг тооцоолох
if "Дүн" in df_ej.columns and "Кредит" in df_ej.columns:
    # Дебет баганаар бүлэглэж, дүнг гаргах
    debit_grouped = (
        df_ej[df_ej["Кредит"].astype(str) == "100102 - Касс дахь мөнгө /Gold's/"]
        .groupby("Дебет")["Дүн"].sum().reset_index()
    )
    # Хөл дүн нэмэх
    total_row = pd.DataFrame([{
        "Дебет": "Нийт",
        "Дүн": debit_grouped["Дүн"].sum()
    }])
    debit_grouped_with_total = pd.concat([debit_grouped, total_row], ignore_index=True)
    st.subheader("100102 - Касс дахь мөнгө /Gold's/ дансны кредит талд орсон гүйлгээг дебетээр бүлэглэсэн дүн")
    st.dataframe(debit_grouped_with_total.style.format({"Дүн": "{:,.0f}"}), use_container_width=True)
else:
    st.warning("ЕЖ.xlsx файлд 'Кредит' эсвэл 'Дүн' багана олдсонгүй.")
    
    
if "Дүн" in df_ej.columns and "Кредит" in df_ej.columns and "Дебет" in df_ej.columns:
    # 120101 дансны кредит талын гүйлгээ
    df_120101 = df_ej[df_ej["Кредит"].astype(str) == "120101 - Дансны авлага"]

    # Дебет дансны эхлэлүүдийг олж, сонгох боломжтой болгох
    debit_starts = sorted(set(df_120101["Дебет"].astype(str).str[:2]))
    selected_starts = st.multiselect(
        "Дебет дансны эхлэлээр шүүх (нэг буюу хэд хэдэн эхлэл сонгоно уу):",
        options=debit_starts,
        default=[ "11"]
    )

    # Сонгосон эхлэлүүдээр шүүх
    if selected_starts:
        mask = df_120101["Дебет"].astype(str).str[:2].isin(selected_starts)
        df_120101 = df_120101[mask]

    # Дебетээр бүлэглэж, дүнг гаргах
    debit_grouped = df_120101.groupby("Дебет")["Дүн"].sum().reset_index()
    # Хөл дүн нэмэх
    total_row = pd.DataFrame([{
        "Дебет": "Нийт",
        "Дүн": debit_grouped["Дүн"].sum()
    }])
    debit_grouped_with_total = pd.concat([debit_grouped, total_row], ignore_index=True)
    st.subheader("120101 - Дансны авлага дансны кредит талд орсон гүйлгээг дебетээр бүлэглэсэн дүн")
    st.dataframe(debit_grouped_with_total.style.format({"Дүн": "{:,.0f}"}), use_container_width=True)
else:
    st.warning("ЕЖ.xlsx файлд 'Кредит', 'Дебет' эсвэл 'Дүн' багана олдсонгүй.")
    
    
    
    
# 310101 дансны кредит талын дүнг тооцоолох
if "Дүн" in df_ej.columns and "Кредит" in df_ej.columns and "Дебет" in df_ej.columns:
    # 310101 дансны кредит талын гүйлгээ
    df_310101 = df_ej[df_ej["Кредит"].astype(str) == "310101 - Дансны өглөг"]

    # Дебет дансны эхлэлүүдийг олж, сонгох боломжтой болгох
    debit_starts = sorted(set(df_310101["Дебет"].astype(str).str[:2]))
    selected_starts = st.multiselect(
        "Дебет дансны эхлэлээр шүүх (нэг буюу хэд хэдэн эхлэл сонгоно уу):",
        options=debit_starts,
        default=[ "11"]
    )

    # Сонгосон эхлэлүүдээр шүүх
    if selected_starts:
        mask = df_310101["Дебет"].astype(str).str[:2].isin(selected_starts)
        df_310101 = df_310101[mask]

    # Дебетээр бүлэглэж, дүнг гаргах
    debit_grouped = df_310101.groupby("Дебет")["Дүн"].sum().reset_index()
    # Хөл дүн нэмэх
    total_row = pd.DataFrame([{
        "Дебет": "Нийт",
        "Дүн": debit_grouped["Дүн"].sum()
    }])
    debit_grouped_with_total = pd.concat([debit_grouped, total_row], ignore_index=True)
    st.subheader("310101 - Дансны өглөг дансны кредит талд орсон гүйлгээг дебетээр бүлэглэсэн дүн")
    st.dataframe(debit_grouped_with_total.style.format({"Дүн": "{:,.0f}"}), use_container_width=True)
else:
    st.warning("ЕЖ.xlsx файлд 'Кредит', 'Дебет' эсвэл 'Дүн' багана олдсонгүй.")
    
    
    
    
# 340104 дансны кредит талын дүнг тооцоолох
if "Дүн" in df_ej.columns and "Дебет" in df_ej.columns and "Кредит" in df_ej.columns:
    # Дебет баганаар 340104-г шүүж, Кредит баганаар 310601, 510101-г шүүнэ
    filtered = df_ej[
        (df_ej["Дебет"].astype(str) == "340104 - Бусад урт хугацаат өр төлбөр") &
        (df_ej["Кредит"].astype(str).isin([
            "310601 - НӨАТ - ын өглөг",
            "510101 - Борлуулалтын орлого"
        ]))
    ]
    kredit_grouped = filtered.groupby("Кредит")["Дүн"].sum().reset_index()
    # Хөл дүн нэмэх
    total_row = pd.DataFrame([{
        "Кредит": "Нийт",
        "Дүн": kredit_grouped["Дүн"].sum()
    }])
    kredit_grouped_with_total = pd.concat([kredit_grouped, total_row], ignore_index=True)
    st.subheader("340104 - Бусад урт хугацаат өр төлбөр дансны кредит талд орсон гүйлгээнээс зөвхөн 310601, 510101 дансны дүн Anuxai Private Brand-н өглөгийг барагдуулсан")
    st.dataframe(kredit_grouped_with_total.style.format({"Дүн": "{:,.0f}"}), use_container_width=True)
else:
    st.warning("ЕЖ.xlsx файлд 'Кредит', 'Дебет' эсвэл 'Дүн' багана олдсонгүй.")