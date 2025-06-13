import streamlit as st
import pandas as pd

st.set_page_config(page_title="Сар бүрийн ашиг алдагдлын тайлан", layout="centered")
st.title("📊 Сар бүрийн ашиг алдагдлын тайлан")
df= pd.read_excel("ЕЖ.xlsx")
# 📂 Гүйлгээний файл байршуулах
# uploaded_file = st.file_uploader("Ерөнхий журналын Excel файл оруулна уу", type=["xlsx"])



# 🧹 Бэлтгэх
df['Огноо'] = pd.to_datetime(df['сар, өдөр'])



# Данс болон дүнг нэг багана болгон нэгтгэх
debet_df = df[["Огноо", "Дебет", "Дүн"]].rename(columns={"Дебет": "Данс код"})
# credit_df = df[["Огноо", "Кредит", "Дүн"]].rename(columns={"Кредит": "Данс код"})

# Данс код + Огноогоор нэгтгэхэд бэлдэх
all_df = pd.concat([debet_df,], ignore_index=True)

# Сарын формат гаргах (хүсвэл)
all_df["Сар"] = all_df["Огноо"].dt.to_period("M")

# Нийлбэрийг гаргах
pivot = all_df.groupby(["Сар", "Данс код"])["Дүн"].sum().reset_index()


# # 🎯 Дансны кодоос ангилал тодорхойлох
# def classify(account_code):
#     if account_code.startswith("5101"):
#         return "Орлого"
#     elif account_code.startswith("6101"):
#         return "Өртөг"
#     elif account_code.startswith("70") or account_code.startswith("71"):
#         return "Үйл ажиллагааны зардал"
#     else:
#         return "Бусад"

# df['Ангилал'] = df['Данс код'].apply(classify)

# # 💵 Дүн тооцох
# df['Дүн'] = df.apply(lambda x: x['Кредит'] if x['Ангилал'] == "Орлого" else x['Дебет'], axis=1)

# # 📊 Pivot Table үүсгэх
# pivot = df.groupby(['Сар', 'Ангилал'])['Дүн'].sum().unstack(fill_value=0)
# pivot['Цэвэр ашиг'] = pivot.get('Орлого', 0) - pivot.get('Өртөг', 0) - pivot.get('Үйл ажиллагааны зардал', 0) - pivot.get('Санхүүгийн зардал', 0)
print(pivot)

# 📈 Хүснэгт харуулах
st.subheader("Сар бүрийн ашиг алдагдлын хүснэгт")
st.dataframe(pivot)

# 📉 График
# st.line_chart(pivot['Цэвэр ашиг'])
