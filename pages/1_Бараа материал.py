
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

# 📊 Хүснэгтээр харуулах
st.subheader("Барааны эхний үлдэгдэл 2023.03.17-ны байдлаар")
st.dataframe(df_c1, use_container_width=True)




# Excel унших
file_path = BASE_DIR.parent / "data" / "бараа_тоо_ширхэгээр.xlsx"
df_transaction=pd.read_excel(file_path, sheet_name='Sheet', skiprows=4, nrows=39000)

# 'Татан авалт'-тай мөрүүдийг шүүх
tatan_avalt = df_transaction[df_transaction['Баримтын төрөл'] == 'Татан авалт']
tatan_avalt_grouped = tatan_avalt.groupby('Байршил')[['Орлого тоо', 'Орлого дүн']].sum().reset_index()    


st.subheader("Барааны татан авалтын нийт тоо ширхэг, өртөг дүн")
st.dataframe(tatan_avalt_grouped.style.format({"Орлого тоо": "{:,.2f}", "Орлого дүн":"{:,.2f}"}), use_container_width=True)




# Орлогын тоо > 0 буюу агуулахад орсон гүйлгээнүүдийг авна
outgoing_df = df_transaction[df_transaction["Орлого тоо"] > 0].copy()

# Баримтын төрөл ба агуулах (байршил) багануудаар бүлэглэж, дүнг нэгтгэх
agg_summary = outgoing_df.groupby(["Байршил", "Баримтын төрөл"])["Орлого тоо"].sum().reset_index()

# Харуулах
st.subheader("🏷️ Агуулах тус бүрт орсон баримтын төрлүүд")
st.dataframe(agg_summary.style.format({"Орлого тоо": "{:,.2f}"}), use_container_width=True)






# Зарлагын тоо > 0 буюу агуулахаас гарсан гүйлгээнүүдийг авна
outgoing_df = df_transaction[df_transaction["Зарлага тоо"] > 0].copy()

# Баримтын төрөл ба агуулах (байршил) багануудаар бүлэглэж, дүнг нэгтгэх
agg_summary = outgoing_df.groupby(["Байршил", "Баримтын төрөл"])["Зарлага тоо"].sum().reset_index()

# Харуулах
st.subheader("🏷️ Агуулах тус бүрээс гарсан баримтын төрлүүд")
st.dataframe(agg_summary.style.format({"Зарлага тоо": "{:2,.2f}"}), use_container_width=True)




# 1. "Бараа материал хөдөлгөөн" баримтуудыг шүүх
bm_movement_df = df_transaction[df_transaction["Баримтын төрөл"] == "Бараа материал хөдөлгөөн"].copy()

# 2. Баримт бүр хэдэн мөртэйг тоолно
barimt_counts = bm_movement_df.groupby("Баримт").size()

# 3. 2-с дээш мөртэй баримтуудын дугаарыг авна
multi_line_nos = barimt_counts[barimt_counts > 1].index

# 4. Эдгээр баримтуудыг датафреймээс шүүнэ
multi_row_df = bm_movement_df[bm_movement_df["Баримт"].isin(multi_line_nos)].copy()

# 5. Баримтаар нэгтгэж нийт орлого, зарлага гаргана
summary = multi_row_df.groupby("Баримт")[["Орлого тоо", "Зарлага тоо"]].sum().reset_index()

# 6. Гаралтын болон оролтын агуулахыг ялгаж авна
zar = multi_row_df[multi_row_df["Зарлага тоо"] > 0].groupby("Баримт").agg({
    "Байршил": "first",
    "Зарлага тоо": "sum"
}).reset_index().rename(columns={"Байршил": "Гаралтын агуулах"})

orl = multi_row_df[multi_row_df["Орлого тоо"] > 0].groupby("Баримт").agg({
    "Байршил": "first"
}).reset_index().rename(columns={"Байршил": "Оролтын агуулах"})

# 7. Нэгтгэж холбох
merged = pd.merge(zar, orl, on="Баримт", how="inner")

# 8. Гаралтын болон оролтын агуулах + нийт шилжүүлсэн тоо-г бүлэглэнэ
summary_by_location = merged.groupby(["Гаралтын агуулах", "Оролтын агуулах"])["Зарлага тоо"].sum().reset_index(name="Нийт шилжүүлсэн тоо")

# 9. Харуулах
st.subheader("🏷️ Агуулах хоорондын хөдөлгөөний шилжүүлэг")
st.dataframe(summary_by_location.style.format({"Нийт шилжүүлсэн тоо": "{:,.2f}"}), use_container_width=True)







# Орлого ба зарлагын агуулахыг ялгана
zar = df_transaction[df_transaction["Зарлага тоо"] > 0][["Баримтын төрөл", "Байршил", "Зарлага тоо"]].rename(
    columns={"Байршил": "Агуулах", "Зарлага тоо": "Тоо"})
zar["Төрөл"] = "Зарлага"

orl = df_transaction[df_transaction["Орлого тоо"] > 0][["Баримтын төрөл", "Байршил", "Орлого тоо"]].rename(
    columns={"Байршил": "Агуулах", "Орлого тоо": "Тоо"})
orl["Төрөл"] = "Орлого"

# Нэгдүүлж нэг датафрейм болгох
movement_combined = pd.concat([zar, orl], ignore_index=True)
pivot_df = movement_combined.pivot_table(
    index=["Агуулах"],         # Агуулах бүрийн хувьд
    columns=["Төрөл", "Баримтын төрөл"],  # Орлого/Зарлага + Баримтын төрөл
    values="Тоо",
    aggfunc="sum",
    fill_value=0
)

# Дизайн сайжруулалт
pivot_df.columns = [' | '.join(col).strip() for col in pivot_df.columns.values]
pivot_df = pivot_df.reset_index()
st.subheader("📊 Агуулах хоорондын Орлого/Зарлага, Баримтын төрлөөр")
st.dataframe(pivot_df, use_container_width=True)








# 1. Тоон багана (бүгдийг автоматаар олох)
numeric_cols = pivot_df.select_dtypes(include='number').columns

# 2. Нийт дүнг тооцоолох (тоон багануудаар)
totals = pivot_df[numeric_cols].sum()

# 3. Хөл дүнг нэг мөр болгон үүсгэх
total_row = pd.DataFrame([["Нийт", ""] + totals.tolist()], columns=["Агуулах", "Барааны нэр"] + numeric_cols.tolist())

# 4. Хөл дүнг датафреймд нэмж нэгтгэх
pivot_with_total = pd.concat([pivot_df, total_row], ignore_index=True)

# 5. Хүснэгтийг харуулах
st.subheader("📦 Агуулах + Барааны нэр + Хөл дүн")
st.dataframe(pivot_with_total, use_container_width=True)













# 'Татан авалт'-тай мөрүүдийг шүүх
tatan_avalt = df_transaction[df_transaction['Баримтын төрөл'] == 'Бараа материал хөдөлгөөн']
tatan_avalt_grouped = tatan_avalt.groupby('Байршил')[['Зарлага тоо', 'Зарлага дүн']].sum().reset_index()    


st.subheader("Барааны хөдөлгөөний зарлагын нийт тоо ширхэг, дүн")
st.dataframe(tatan_avalt_grouped.style.format({"Зарлага тоо": "{:,.2f}", "Зарлага дүн":"{:,.2f}"}), use_container_width=True)




# ...existing code...

# --- Байршил тус бүрийн барааны эцсийн үлдэгдэл (тооллогын орлого, зарлага оруулахгүй) ---

# 1. Эхний үлдэгдэл (агуулахын) - Байршил тус бүрээр (зөвхөн "Агуулах", "PN Store")
df_ankh = df_c1.rename(columns={"Нэр": "Барааны нэр"})[["Барааны нэр", "Агуулах", "PN Store"]].copy()
ankh_warehouse = df_ankh[["Барааны нэр", "Агуулах"]].copy().rename(columns={"Агуулах": "Эхний үлдэгдэл"})
ankh_warehouse["Байршил"] = "Агуулах"
ankh_store = df_ankh[["Барааны нэр", "PN Store"]].copy().rename(columns={"PN Store": "Эхний үлдэгдэл"})
ankh_store["Байршил"] = "PN Store"
df_ankh_all = pd.concat([ankh_warehouse, ankh_store], ignore_index=True)

# 2. Гүйлгээний бүх байршил, барааны нэрийн хослолыг олно
all_locations = df_transaction[["Байршил", "Барааны нэр"]].drop_duplicates()
# Эхний үлдэгдэлтэй байршлуудыг нэмнэ
all_locations = pd.concat([
    all_locations,
    df_ankh_all[["Байршил", "Барааны нэр"]]
]).drop_duplicates().reset_index(drop=True)

# 3. Орлого, зарлагыг тооцоолно (тооллогын орлого/зарлага оруулахгүй)
orl = df_transaction[
    (df_transaction["Орлого тоо"] > 0) &
    (df_transaction["Баримтын төрөл"] != "Тооллогын орлого")
].groupby(["Байршил", "Барааны нэр"])["Орлого тоо"].sum().reset_index()

zar = df_transaction[
    (df_transaction["Зарлага тоо"] > 0) &
    (df_transaction["Баримтын төрөл"] != "Тооллогын зарлага")
].groupby(["Байршил", "Барааны нэр"])["Зарлага тоо"].sum().reset_index()

# 4. Бүх байршил, барааны нэрийн хослол дээр эхний үлдэгдэл, орлого, зарлага-г нэгтгэнэ
df_balance = all_locations.merge(df_ankh_all, on=["Байршил", "Барааны нэр"], how="left")
df_balance = df_balance.merge(orl, on=["Байршил", "Барааны нэр"], how="left")
df_balance = df_balance.merge(zar, on=["Байршил", "Барааны нэр"], how="left")
df_balance = df_balance.fillna(0)

# 5. Эцсийн үлдэгдэл тооцоолох
df_balance["Эцсийн үлдэгдэл"] = (
    df_balance["Эхний үлдэгдэл"] + df_balance["Орлого тоо"] - df_balance["Зарлага тоо"]
)

# 6. Байршил, барааны нэрээр бүлэглэж, дүнг нэгтгэнэ (замбараагүй давхардлыг цэгцэлнэ)
df_balance_grouped = (
    df_balance.groupby(["Байршил", "Барааны нэр"], as_index=False)["Эцсийн үлдэгдэл"]
    .sum()
    .sort_values(["Байршил", "Барааны нэр"])
    .reset_index(drop=True)
)

# 7. Харуулах
st.subheader("📦Эцсийн үлдэгдэл  Байршил, бараагаар бүлэглэсэн  (тооллогын орлого/зарлага оруулахгүй)")
st.dataframe(df_balance_grouped, use_container_width=True)
# ...existing code...



# ...existing code...

# "Бараа материал хөдөлгөөн" төрлийн шилжүүлэг баримтуудыг авна
bm_movement = df_transaction[df_transaction["Баримтын төрөл"] == "Бараа материал хөдөлгөөн"].copy()

# "Агуулах"-аас "PN Store" руу шилжсэн бараануудыг шүүнэ
out_df = bm_movement[
    (bm_movement["Байршил"] == "Агуулах") & (bm_movement["Зарлага тоо"] > 0)
]
in_df = bm_movement[
    (bm_movement["Байршил"] == "PN Store") & (bm_movement["Орлого тоо"] > 0)
]

# Баримтын дугаараар холбож, барааны нэрээр бүлэглэн нийт шилжүүлсэн тоог гаргана
merged = pd.merge(
    out_df[["Баримт", "Барааны нэр", "Зарлага тоо"]],
    in_df[["Баримт", "Барааны нэр", "Орлого тоо"]],
    on=["Баримт", "Барааны нэр"],
    how="inner"
)

# Барааны нэрээр бүлэглэж нийт шилжүүлсэн тоог нэгтгэнэ
summary = merged.groupby("Барааны нэр")[["Зарлага тоо", "Орлого тоо"]].sum().reset_index()

# Хөл дүн (нийт дүн) тооцоолох
total_row = pd.DataFrame([{
    "Барааны нэр": "Нийт",
    "Зарлага тоо": summary["Зарлага тоо"].sum(),
    "Орлого тоо": summary["Орлого тоо"].sum()
}])

summary_with_total = pd.concat([summary, total_row], ignore_index=True)

# Харуулах
st.subheader("🏷️ 'Агуулах'-аас 'PN Store' руу 'Бараа материал хөдөлгөөн' төрлөөр шилжсэн бараа (нэг мөрөөр, хөл дүнтэй)")
st.dataframe(summary_with_total, use_container_width=True)
# ...existing code...



# ...existing code...

# --- "Бараа материал зарлага" төрлийн бүх байршлын шинжилгээ ---

# 1. "Бараа материал зарлага" төрлийн бүх мөрийг авна
bm_zarlaga = df_transaction[
    (df_transaction["Баримтын төрөл"] == "Бараа материал зарлага") &
    (df_transaction["Зарлага тоо"] > 0)
]

# 2. Байршил, барааны нэрээр бүлэглэж нийт зарлагыг гаргана
bm_zarlaga_grouped = bm_zarlaga.groupby(["Байршил", "Барааны нэр"])["Зарлага тоо"].sum().reset_index()

# 3. Нийт дүнг тооцоолох
total_row = pd.DataFrame([{
    "Байршил": "Нийт",
    "Барааны нэр": "",
    "Зарлага тоо": bm_zarlaga_grouped["Зарлага тоо"].sum()
}])

bm_zarlaga_with_total = pd.concat([bm_zarlaga_grouped, total_row], ignore_index=True)

# 4. Харуулах
st.subheader("📦 Бүх байршлын 'Бараа материал зарлага' төрлийн нийт зарлага")
st.dataframe(bm_zarlaga_with_total, use_container_width=True)
#


# ...existing code...

# --- "Бараа материал зарлага" төрлийн бүх байршлын шинжилгээ ---

# 1. "Бараа материал зарлага" төрлийн бүх мөрийг авна
# "Бараа материалын төрөл нэгтгэл" гэсэн баримтыг оруулахгүй!
bm_zarlaga = df_transaction[
    (df_transaction["Баримтын төрөл"] == "Бараа материал зарлага") &
    (df_transaction["Зарлага тоо"] > 0) &
    (df_transaction["Гүйлгээний утга"] != "Бараа материалын төрөл нэгтгэл")
]

# 2. Байршил, барааны нэрээр бүлэглэж нийт зарлагыг гаргана
bm_zarlaga_grouped = bm_zarlaga.groupby(["Байршил", "Барааны нэр"])["Зарлага тоо"].sum().reset_index()

# 3. Нийт дүнг тооцоолох
total_row = pd.DataFrame([{
    "Байршил": "Нийт",
    "Барааны нэр": "",
    "Зарлага тоо": bm_zarlaga_grouped["Зарлага тоо"].sum()
}])

bm_zarlaga_with_total = pd.concat([bm_zarlaga_grouped, total_row], ignore_index=True)

# 4. Харуулах
st.subheader("📦 Бүх байршлын 'Бараа материал зарлага' (нэгтгэлгүй) төрлийн нийт зарлага")
st.dataframe(bm_zarlaga_with_total, use_container_width=True)
# ...existing



# ...existing code...

# --- "Бараа материал зарлага" төрлийн бүх байршлын шинжилгээ, гүйлгээний утгаар бүлэглэх ---

# 1. "Бараа материал зарлага" төрлийн бүх мөрийг авна
bm_zarlaga = df_transaction[
    (df_transaction["Баримтын төрөл"] == "Бараа материал зарлага") &
    (df_transaction["Зарлага тоо"] > 0) &
    (df_transaction["Гүйлгээний утга"] != "Бараа материалын төрөл нэгтгэл")
]

# 2. Байршил, гүйлгээний утга, барааны нэрээр бүлэглэж нийт зарлагыг гаргана
bm_zarlaga_grouped = bm_zarlaga.groupby(
    ["Байршил", "Гүйлгээний утга", "Барааны нэр"]
)["Зарлага тоо"].sum().reset_index()

# 3. Нийт дүнг тооцоолох
total_row = pd.DataFrame([{
    "Байршил": "Нийт",
    "Гүйлгээний утга": "",
    "Барааны нэр": "",
    "Зарлага тоо": bm_zarlaga_grouped["Зарлага тоо"].sum()
}])

bm_zarlaga_with_total = pd.concat([bm_zarlaga_grouped, total_row], ignore_index=True)

# 4. Харуулах
st.subheader("📦 Бүх байршлын 'Бараа материал зарлага' (нэгтгэлгүй) төрлийн нийт зарлага - гүйлгээний утгаар бүлэглэсэн")
st.dataframe(bm_zarlaga_with_total, use_container_width=True)
# ...existing code...