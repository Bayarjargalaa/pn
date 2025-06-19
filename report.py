import streamlit as st
import pandas as pd

st.set_page_config(page_title="Сар бүрийн ашиг алдагдлын тайлан", layout="centered")
st.title("📊 Сар бүрийн ашиг алдагдлын тайлан")
df= pd.read_excel("ЕЖ.xlsx")

print(df.columns)

# 🧹 Бэлтгэх
df['Огноо'] = pd.to_datetime(df['сар, өдөр'])



# Данс болон дүнг нэг багана болгон нэгтгэх
all_debet_df = df[["Огноо", "Дебет", "Дүн"]].rename(columns={"Дебет": "Данс код"})
all_credit_df = df[["Огноо", "Кредит\n", "Дүн"]].rename(columns={"Кредит\n": "Данс код"})



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
# st.subheader("Сар бүрийн дебет дүн")
# st.dataframe(pivot)
# st.dataframe(pivot_debit.style.format("{:,.2f}"))

# 📈 Хүснэгт харуулах
# st.subheader("Сар бүрийн кредит дүн")
# st.dataframe(pivot)
# st.dataframe(pivot_credit.style.format("{:,.2f}"))

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
sales_entries = df[df["Кредит\n"].astype(str).str.startswith("5101")].copy()

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



