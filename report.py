
import os
from pathlib import Path
import pandas as pd
import streamlit as st


# 📌 Одоогийн Python скрипт байрлаж буй хавтас
BASE_DIR = Path(__file__).resolve().parent

# 📌 data хавтас дахь файлын зам
file_path = BASE_DIR.parent / 'PN'/ "data" / "ЕЖ.xlsx"
print(f"Файл байрлах зам: {file_path}")

st.set_page_config(page_title="Сар бүрийн ашиг алдагдлын тайлан", layout="centered")

df= pd.read_excel(file_path)

print(df.columns)

# 🧹 Бэлтгэх
df['Огноо'] = pd.to_datetime(df['сар, өдөр'])



# Данс болон дүнг нэг багана болгон нэгтгэх
all_debet_df = df[["Огноо", "Дебет", "Дүн"]].rename(columns={"Дебет": "Данс код"})
all_credit_df = df[["Огноо", "Кредит", "Дүн"]].rename(columns={"Кредит": "Данс код"})



# Сарын формат гаргах (хүсвэл)
all_debet_df["Сар"] = all_debet_df["Огноо"].dt.to_period("M")
all_credit_df["Сар"] = all_credit_df["Огноо"].dt.to_period("M")

# Нийлбэрийг гаргах
# pivot = all_df.groupby(["Данс код"])["Дүн"].sum().reset_index()
pivot_debit = all_debet_df.pivot_table(
    index="Данс код", 
    columns="Сар", 
    values="Дүн", 
    aggfunc="sum", 
    fill_value=0
)
numeric_cols = pivot_debit.select_dtypes(include=['number']).columns
pivot_debit[numeric_cols] = pivot_debit[numeric_cols].astype(float)

pivot_credit = all_credit_df.pivot_table(
    index="Данс код", 
    columns="Сар", 
    values="Дүн", 
    aggfunc="sum", 
    fill_value=0
)
numeric_cols = pivot_credit.select_dtypes(include=['number']).columns
pivot_credit[numeric_cols] = pivot_credit[numeric_cols].astype(float)




# 📈 Хүснэгт харуулах
st.subheader("Сар бүрийн дебет дүн")
st.dataframe(pivot_debit.style.format("{:,.2f}"))

# 📈 Хүснэгт харуулах
st.subheader("Сар бүрийн кредит дүн")
st.dataframe(pivot_credit.style.format("{:,.2f}"))



# ...existing code...

# Сар бүрийн кредит дүн
st.subheader("Сар бүрийн кредит дүн")

# Багана бүрийн нийлбэр (сар бүрийн нийт кредит дүн)
col_total = pd.DataFrame(pivot_credit.sum(axis=0)).T
col_total.index = ['Баганын хөл дүн']

# Мөр бүрийн нийлбэр (данс бүрийн нийт кредит дүн)
pivot_credit_with_row_total = pivot_credit.copy()
pivot_credit_with_row_total['Мөрийн хөл дүн'] = pivot_credit_with_row_total.sum(axis=1)

# Баганын хөл дүнг нэмэх
pivot_credit_with_total = pd.concat([pivot_credit_with_row_total, col_total], axis=0)

# Хэрвээ "Мөрийн хөл дүн" багана баганын нийлбэрт байхгүй бол 0 гэж үзнэ
if 'Мөрийн хөл дүн' not in col_total.columns:
    pivot_credit_with_total.loc['Баганын хөл дүн', 'Мөрийн хөл дүн'] = col_total.sum(axis=1).values[0]

st.dataframe(pivot_credit_with_total.style.format("{:,.2f}"), use_container_width=True)
# ...existing code...



rows_5101  = pivot_credit.loc[pivot_credit.index.astype(str).str.startswith('5101')]
rows_6101  = pivot_debit.loc[pivot_debit.index.astype(str).str.startswith('6101')]
# rows_1501  = pivot_debit.loc[pivot_debit.index.astype(str).str.startswith('1501')]
rows_70  = pivot_debit.loc[pivot_debit.index.astype(str).str.startswith('70')]
rows_71  = pivot_debit.loc[pivot_debit.index.astype(str).str.startswith('71')]
rows_87  = pivot_debit.loc[pivot_debit.index.astype(str).str.startswith('87')]
rows_88  = pivot_debit.loc[pivot_debit.index.astype(str).str.startswith('88')]
rows_91  = pivot_debit.loc[pivot_debit.index.astype(str).str.startswith('91')]

merged_rows = pd.concat([rows_5101, rows_6101,  ], axis=0)

# Сар багануудаар ялган, ялгасны дараа хоорондын зөрүүг тооцох
gross_profit = rows_5101.sum(numeric_only=True) - rows_6101.sum(numeric_only=True)
merged_rows.loc['Бохир ашиг'] = gross_profit

row_70_total = pd.DataFrame(rows_70.sum(numeric_only=True)).T
row_70_total.index = ['70_Зардлын_нийт']
merged_rows = pd.concat([merged_rows, row_70_total], axis=0)

row_71_total = pd.DataFrame(rows_71.sum(numeric_only=True)).T
row_71_total.index = ['71_Зардлын_нийт']
merged_rows = pd.concat([merged_rows, row_71_total], axis=0)

row_87_total = pd.DataFrame(rows_87.sum(numeric_only=True)).T
row_87_total.index = ['87_Зардлын_нийт']
merged_rows = pd.concat([merged_rows, row_87_total], axis=0)

row_88_total = pd.DataFrame(rows_88.sum(numeric_only=True)).T
row_88_total.index = ['88_Зардлын_нийт']
merged_rows = pd.concat([merged_rows, row_88_total], axis=0)

row_91_total = pd.DataFrame(rows_91.sum(numeric_only=True)).T
row_91_total.index = ['91_Зардлын_нийт']
merged_rows = pd.concat([merged_rows, row_91_total], axis=0)

rows_all_expense = pivot_debit.loc[
    pivot_debit.index.astype(str).str.startswith(('70', '71', '87', '88', '91'))
]



row_total_expense = pd.DataFrame(rows_all_expense.sum(numeric_only=True)).T
row_total_expense.index = ['Нийт зардал (70+71+87+88+91)']

net_profit = gross_profit - row_total_expense.loc['Нийт зардал (70+71+87+88+91)']
net_profit = pd.DataFrame(net_profit).T 
net_profit.index = ['Цэвэр ашиг /-/ бол алдагдал']
# merged_rows.loc['Цэвэр ашиг'] = net_profit

merged_rows = pd.concat([merged_rows, row_total_expense], axis=0)

merged_rows = pd.concat([merged_rows, net_profit], axis=0)
st.subheader("📊 Сар бүрийн ашиг алдагдлын тайлан")
st.dataframe(merged_rows.style.format("{:,.2f}"), use_container_width=True)

# 📉 График
# st.line_chart(pivot['Цэвэр ашиг'])


st.subheader("Сар бүрийн зардлын тайлан (70, 71, 87, 88, 91)")
st.dataframe(rows_all_expense.style.format("{:,.2f}"), use_container_width=True)



# selected_month = st.selectbox("Сар сонгох:", numeric_cols)
# # 📌 Сонгосон сарын мэдээллийг харуулах
# st.dataframe(
#     rows_all_expense[[selected_month]].style.format("{:,.2f}"),
#     use_container_width=True
# )

df.columns = df.columns.astype(str)
selected_month = st.selectbox(
    "Сар сонгох:", 
    numeric_cols,
    key="sar_songolt"
)

# 👉 Сонгосон сарын нэг баганын датафрейм
selected_data = rows_all_expense[[selected_month]].copy()

# 👉 Нийт зардал (нийт нийлбэр)
total = selected_data[selected_month].sum()

# 👉 Хувь тооцох багана
selected_data["Хувь (%)"] = (selected_data[selected_month] / total * 100)

# 👉 Streamlit-д форматлаж харуулах
st.dataframe(
    selected_data.style.format({
        selected_month: "{:,.2f}",
        "Хувь (%)": "{:.2f}%"
    }),
    use_container_width=True
)
import pandas as pd
import streamlit as st

# 📌 5101 дүнг Кредит талд агуулсан гүйлгээнүүдийг шүүх
sales_entries = df[df["Кредит"].astype(str).str.startswith("5101")].copy()

# 🗓️ Огноог datetime болгож, сараар бүлэглэхэд ашиглах багана үүсгэх
sales_entries["Огноо"] = pd.to_datetime(sales_entries["Огноо"], errors='coerce')
sales_entries["Сар"] = sales_entries["Огноо"].dt.to_period("M")

# 📊 Сараар, Дебет дансаар бүлэглэж дүнг нэгтгэх
monthly_sales = sales_entries.groupby(["Сар", "Дебет"])["Дүн"].sum().reset_index()

# 📌 Pivot хүснэгт үүсгэх: мөр - Дебет данс, багана - Сар
pivot_monthly_sales = monthly_sales.pivot(index="Дебет", columns="Сар", values="Дүн").fillna(0)

# ➕ Нийт мөр нэмэх: Сар тус бүрийн нийлбэрийг тооцоолно
total_row = pivot_monthly_sales.sum(numeric_only=True)
total_row.name = "Нийт"

# ⬇️ Нийт мөрийг pivot хүснэгтэд нэмэх
pivot_monthly_sales = pd.concat([pivot_monthly_sales, total_row.to_frame().T])

# 📈 Streamlit дээр харуулах
st.subheader("📊 Борлуулалтын орлого (5101) сар бүр харьцсан дансуудаар (Нийт дүнтэй)")
st.dataframe(pivot_monthly_sales.style.format("{:,.2f}"), use_container_width=True)



# 1. Касс /Дэлгүүр/ дебет талд орсон гүйлгээнүүдийг авах
cash_in = df[df["Дебет"] == "100101 - Касс дахь мөнгө /Дэлгүүр/"].copy()

# 2. Огноо-г datetime болгож, сараар бүлэглэх
cash_in["Огноо"] = pd.to_datetime(cash_in["Огноо"], errors='coerce')
cash_in["Сар"] = cash_in["Огноо"].dt.to_period("M")

# 3. Сар, Кредит дансаар бүлэглэн дүнг нэгтгэх
credit_grouped = cash_in.groupby(["Сар", "Кредит"])["Дүн"].sum().reset_index()

# 4. Pivot table: мөр - Кредит данс, багана - Сар
pivot_cash_in_by_credit = credit_grouped.pivot(index="Кредит", columns="Сар", values="Дүн").fillna(0)


total_row_cash_in = pivot_cash_in_by_credit.sum(numeric_only=True)
total_row_cash_in.name = "Нийт"
pivot_cash_in_by_credit = pd.concat([pivot_cash_in_by_credit, total_row_cash_in.to_frame().T])

# 5. Streamlit дээр харуулах
st.subheader("💰 100101 - Касс /Дэлгүүр/ дансны Дебет орлогын гүйлгээ (Сар, Кредит дансаар)")
st.dataframe(pivot_cash_in_by_credit.style.format("{:,.2f}"), use_container_width=True)




# 1. Касс /Дэлгүүр/ данс Кредит талд орсон гүйлгээнүүдийг шүүнэ
cash_out = df[df["Кредит"] == "100101 - Касс дахь мөнгө /Дэлгүүр/"].copy()

# 2. Огноог datetime болгож, "Сар" багана үүсгэх
cash_out["Огноо"] = pd.to_datetime(cash_out["Огноо"], errors='coerce')
cash_out["Сар"] = cash_out["Огноо"].dt.to_period("M")

# 3. Сараар болон Дебет дансаар бүлэглэн дүнг нэгтгэх
debit_grouped = cash_out.groupby(["Сар", "Дебет"])["Дүн"].sum().reset_index()

# 4. Pivot table: мөр - Дебет данс, багана - Сар
pivot_debit_cash_out = debit_grouped.pivot(index="Дебет", columns="Сар", values="Дүн").fillna(0)

total_row_cash = pivot_debit_cash_out.sum(numeric_only=True)
total_row_cash.name = "Нийт"
pivot_debit_cash_out = pd.concat([pivot_debit_cash_out, total_row_cash.to_frame().T])
# 5. Streamlit дээр харуулах
st.subheader("💸 100101 - Касс /Дэлгүүр/ дансны Кредит гүйлгээтэй харьцсан Дебет дансууд (Сараар)")
st.dataframe(pivot_debit_cash_out.style.format("{:,.2f}"), use_container_width=True)


# 🔶 1. 100102 - Касс /Gold's/ дансны Дебет орлогын гүйлгээ

cash_in_102 = df[df["Дебет"] == "100102 - Касс дахь мөнгө /Gold's/"].copy()

cash_in_102["Огноо"] = pd.to_datetime(cash_in_102["Огноо"], errors='coerce')
cash_in_102["Сар"] = cash_in_102["Огноо"].dt.to_period("M")

credit_grouped_102 = cash_in_102.groupby(["Сар", "Кредит"])["Дүн"].sum().reset_index()

pivot_cash_in_102 = credit_grouped_102.pivot(index="Кредит", columns="Сар", values="Дүн").fillna(0)

total_row_in_102 = pivot_cash_in_102.sum(numeric_only=True)
total_row_in_102.name = "Нийт"
pivot_cash_in_102 = pd.concat([pivot_cash_in_102, total_row_in_102.to_frame().T])

st.subheader("💰 100102 - Касс /Gold's/ Дебет орлогын гүйлгээ (Сар, Кредит дансаар)")
st.dataframe(pivot_cash_in_102.style.format("{:,.2f}"), use_container_width=True)


# 🔶 2. 100102 - Касс /Gold's/ дансны Кредит гарлага гүйлгээ

cash_out_102 = df[df["Кредит"] == "100102 - Касс дахь мөнгө /Gold's/"].copy()

cash_out_102["Огноо"] = pd.to_datetime(cash_out_102["Огноо"], errors='coerce')
cash_out_102["Сар"] = cash_out_102["Огноо"].dt.to_period("M")

debit_grouped_102 = cash_out_102.groupby(["Сар", "Дебет"])["Дүн"].sum().reset_index()

pivot_cash_out_102 = debit_grouped_102.pivot(index="Дебет", columns="Сар", values="Дүн").fillna(0)

total_row_out_102 = pivot_cash_out_102.sum(numeric_only=True)
total_row_out_102.name = "Нийт"
pivot_cash_out_102 = pd.concat([pivot_cash_out_102, total_row_out_102.to_frame().T])

st.subheader("💸 100102 - Касс /Gold's/ Кредит гарлага гүйлгээ (Сар, Дебет дансаар)")
st.dataframe(pivot_cash_out_102.style.format("{:,.2f}"), use_container_width=True)


# 🔶 1. Дебет талд орсон гүйлгээ (Авлага нэмэгдсэн)
avlaga_debit = df[df["Дебет"] == "120101 - Дансны авлага"].copy()
avlaga_debit["Огноо"] = pd.to_datetime(avlaga_debit["Огноо"], errors='coerce')
avlaga_debit["Сар"] = avlaga_debit["Огноо"].dt.to_period("M")

debit_grouped = avlaga_debit.groupby(["Сар", "Кредит"])["Дүн"].sum().reset_index()
pivot_debit_avlaga = debit_grouped.pivot(index="Кредит", columns="Сар", values="Дүн").fillna(0)

# Нийт мөр
total_row_debit = pivot_debit_avlaga.sum(numeric_only=True)
total_row_debit.name = "Нийт"
pivot_debit_avlaga = pd.concat([pivot_debit_avlaga, total_row_debit.to_frame().T])

st.subheader("📥 120101 - Дансны авлага (Дебет орсон гүйлгээ, Сар бүр Кредит дансаар)")
st.dataframe(pivot_debit_avlaga.style.format("{:,.2f}"), use_container_width=True)


# 🔶 2. Кредит талд орсон гүйлгээ (Авлага буурсан)
avlaga_credit = df[df["Кредит"] == "120101 - Дансны авлага"].copy()
avlaga_credit["Огноо"] = pd.to_datetime(avlaga_credit["Огноо"], errors='coerce')
avlaga_credit["Сар"] = avlaga_credit["Огноо"].dt.to_period("M")

credit_grouped = avlaga_credit.groupby(["Сар", "Дебет"])["Дүн"].sum().reset_index()
pivot_credit_avlaga = credit_grouped.pivot(index="Дебет", columns="Сар", values="Дүн").fillna(0)

# Нийт мөр
total_row_credit = pivot_credit_avlaga.sum(numeric_only=True)
total_row_credit.name = "Нийт"
pivot_credit_avlaga = pd.concat([pivot_credit_avlaga, total_row_credit.to_frame().T])

st.subheader("📤 120101 - Дансны авлага (Кредит орсон гүйлгээ, Сар бүр Дебет дансаар)")
st.dataframe(pivot_credit_avlaga.style.format("{:,.2f}"), use_container_width=True)


import pandas as pd
import streamlit as st

# 🟩 1. Дебет талд орсон гүйлгээ (авлага нэмэгдсэн)
emp_receivable_debit = df[df["Дебет"] == "120601 - Ажиллагчдаас авах авлага"].copy()
emp_receivable_debit["Огноо"] = pd.to_datetime(emp_receivable_debit["Огноо"], errors='coerce')
emp_receivable_debit["Сар"] = emp_receivable_debit["Огноо"].dt.to_period("M")

debit_grouped = emp_receivable_debit.groupby(["Сар", "Кредит"])["Дүн"].sum().reset_index()
pivot_debit_emp = debit_grouped.pivot(index="Кредит", columns="Сар", values="Дүн").fillna(0)

# 👉 Нийт мөр
total_row_debit = pivot_debit_emp.sum(numeric_only=True)
total_row_debit.name = "Нийт"
pivot_debit_emp = pd.concat([pivot_debit_emp, total_row_debit.to_frame().T])

st.subheader("📥 120601 - Ажиллагчдаас авах авлага (Дебет, Сар бүр Кредит дансаар)")
st.dataframe(pivot_debit_emp.style.format("{:,.2f}"), use_container_width=True)


# 🟥 2. Кредит талд орсон гүйлгээ (авлага буурсан)
emp_receivable_credit = df[df["Кредит"] == "120601 - Ажиллагчдаас авах авлага"].copy()
emp_receivable_credit["Огноо"] = pd.to_datetime(emp_receivable_credit["Огноо"], errors='coerce')
emp_receivable_credit["Сар"] = emp_receivable_credit["Огноо"].dt.to_period("M")

credit_grouped = emp_receivable_credit.groupby(["Сар", "Дебет"])["Дүн"].sum().reset_index()
pivot_credit_emp = credit_grouped.pivot(index="Дебет", columns="Сар", values="Дүн").fillna(0)

# 👉 Нийт мөр
total_row_credit = pivot_credit_emp.sum(numeric_only=True)
total_row_credit.name = "Нийт"
pivot_credit_emp = pd.concat([pivot_credit_emp, total_row_credit.to_frame().T])

st.subheader("📤 120601 - Ажиллагчдаас авах авлага (Кредит, Сар бүр Дебет дансаар)")
st.dataframe(pivot_credit_emp.style.format("{:,.2f}"), use_container_width=True)


import pandas as pd
import streamlit as st

# 📌 1. Дебет талд орсон гүйлгээ — өглөг буурсан
debit_df = df[df["Дебет"] == "310101 - Дансны өглөг"].copy()
debit_df["Огноо"] = pd.to_datetime(debit_df["Огноо"], errors="coerce")
debit_df["Сар"] = debit_df["Огноо"].dt.to_period("M")

grouped_debit = debit_df.groupby(["Сар", "Кредит"])["Дүн"].sum().reset_index()
pivot_debit = grouped_debit.pivot(index="Кредит", columns="Сар", values="Дүн").fillna(0)

total_row_debit = pivot_debit.sum(numeric_only=True)
total_row_debit.name = "Нийт"
pivot_debit = pd.concat([pivot_debit, total_row_debit.to_frame().T])

st.subheader("📉 310101 - Дансны өглөгийн бууралт (Дебет гүйлгээ, Сар бүр Кредит дансаар)")
st.dataframe(pivot_debit.style.format("{:,.2f}"), use_container_width=True)


# 📌 2. Кредит талд орсон гүйлгээ — өглөг нэмэгдсэн
credit_df = df[df["Кредит"] == "310101 - Дансны өглөг"].copy()
credit_df["Огноо"] = pd.to_datetime(credit_df["Огноо"], errors="coerce")
credit_df["Сар"] = credit_df["Огноо"].dt.to_period("M")

grouped_credit = credit_df.groupby(["Сар", "Дебет"])["Дүн"].sum().reset_index()
pivot_credit = grouped_credit.pivot(index="Дебет", columns="Сар", values="Дүн").fillna(0)

total_row_credit = pivot_credit.sum(numeric_only=True)
total_row_credit.name = "Нийт"
pivot_credit = pd.concat([pivot_credit, total_row_credit.to_frame().T])

st.subheader("📈 310101 - Дансны өглөгийн өсөлт (Кредит гүйлгээ, Сар бүр Дебет дансаар)")
st.dataframe(pivot_credit.style.format("{:,.2f}"), use_container_width=True)


import pandas as pd
import streamlit as st

# 📌 1. Дебет талд орсон гүйлгээ — өглөг буурсан (төлсөн)
debit_df = df[df["Дебет"] == "311301 - НХАТ - ын өглөг"].copy()
debit_df["Огноо"] = pd.to_datetime(debit_df["Огноо"], errors="coerce")
debit_df["Сар"] = debit_df["Огноо"].dt.to_period("M")

grouped_debit = debit_df.groupby(["Сар", "Кредит"])["Дүн"].sum().reset_index()
pivot_debit = grouped_debit.pivot(index="Кредит", columns="Сар", values="Дүн").fillna(0)

total_row_debit = pivot_debit.sum(numeric_only=True)
total_row_debit.name = "Нийт"
pivot_debit = pd.concat([pivot_debit, total_row_debit.to_frame().T])

st.subheader("📉 311301 - НХАТ-ын өглөгийн бууралт (Дебет гүйлгээ, Сар бүр Кредит дансаар)")
st.dataframe(pivot_debit.style.format("{:,.2f}"), use_container_width=True)


# 📌 2. Кредит талд орсон гүйлгээ — өглөг нэмэгдсэн
credit_df = df[df["Кредит"] == "311301 - НХАТ - ын өглөг"].copy()
credit_df["Огноо"] = pd.to_datetime(credit_df["Огноо"], errors="coerce")
credit_df["Сар"] = credit_df["Огноо"].dt.to_period("M")

grouped_credit = credit_df.groupby(["Сар", "Дебет"])["Дүн"].sum().reset_index()
pivot_credit = grouped_credit.pivot(index="Дебет", columns="Сар", values="Дүн").fillna(0)

total_row_credit = pivot_credit.sum(numeric_only=True)
total_row_credit.name = "Нийт"
pivot_credit = pd.concat([pivot_credit, total_row_credit.to_frame().T])

st.subheader("📈 311301 - НХАТ-ын өглөгийн өсөлт (Кредит гүйлгээ, Сар бүр Дебет дансаар)")
st.dataframe(pivot_credit.style.format("{:,.2f}"), use_container_width=True)


import pandas as pd
import streamlit as st

# 📌 1. Дебет талд орсон гүйлгээ (өр төлсөн дүн)
debit_df = df[df["Дебет"] == "340104 - Бусад урт хугацаат өр төлбөр"].copy()
debit_df["Огноо"] = pd.to_datetime(debit_df["Огноо"], errors="coerce")
debit_df["Сар"] = debit_df["Огноо"].dt.to_period("M")

grouped_debit = debit_df.groupby(["Сар", "Кредит"])["Дүн"].sum().reset_index()
pivot_debit = grouped_debit.pivot(index="Кредит", columns="Сар", values="Дүн").fillna(0)

total_row_debit = pivot_debit.sum(numeric_only=True)
total_row_debit.name = "Нийт"
pivot_debit = pd.concat([pivot_debit, total_row_debit.to_frame().T])

st.subheader("📉 340104 - Урт хугацаат өр төлбөрийн бууралт (Дебет гүйлгээ, Кредит дансаар)")
st.dataframe(pivot_debit.style.format("{:,.2f}"), use_container_width=True)


# 📌 2. Кредит талд орсон гүйлгээ (өр үүссэн дүн)
credit_df = df[df["Кредит"] == "340104 - Бусад урт хугацаат өр төлбөр"].copy()
credit_df["Огноо"] = pd.to_datetime(credit_df["Огноо"], errors="coerce")
credit_df["Сар"] = credit_df["Огноо"].dt.to_period("M")

grouped_credit = credit_df.groupby(["Сар", "Дебет"])["Дүн"].sum().reset_index()
pivot_credit = grouped_credit.pivot(index="Дебет", columns="Сар", values="Дүн").fillna(0)

total_row_credit = pivot_credit.sum(numeric_only=True)
total_row_credit.name = "Нийт"
pivot_credit = pd.concat([pivot_credit, total_row_credit.to_frame().T])

st.subheader("📈 340104 - Урт хугацаат өр үүсэлт (Кредит гүйлгээ, Дебет дансаар)")
st.dataframe(pivot_credit.style.format("{:,.2f}"), use_container_width=True)

