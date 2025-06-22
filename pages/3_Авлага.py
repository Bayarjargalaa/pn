import pandas as pd
from pathlib import Path
import streamlit as st

# Файлын зам
BASE_DIR = Path(__file__).resolve().parent
file_path = BASE_DIR.parent / "data" / "Борлуулалтын авлага.xlsx"

# Excel файл унших
df = pd.read_excel(file_path)

# Харилцагч байхгүй мөрүүдэд "Харилцагчгүй" гэж онооно
df["Харилцагчийн нэр"] = df["Харилцагчийн нэр"].fillna("Харилцагчгүй")

# Харилцагчийн нэрээр бүлэглэж, Нийт дүнг тооцоолох
if "Харилцагчийн нэр" in df.columns and "Нийт дүн" in df.columns:
    grouped = df.groupby("Харилцагчийн нэр")["Нийт дүн"].sum().reset_index()
    # Хөл дүн нэмэх
    total_row = pd.DataFrame([{
        "Харилцагчийн нэр": "Нийт",
        "Нийт дүн": grouped["Нийт дүн"].sum()
    }])
    grouped_with_total = pd.concat([grouped, total_row], ignore_index=True)
    st.subheader("Харилцагчийн нэрээр бүлэглэсэн авлагын дүн (Харилцагчгүйг оролцуулсан)")
    st.dataframe(grouped_with_total.style.format({"Нийт дүн": "{:,.0f}"}), use_container_width=True)
else:
    st.warning("Харилцагчийн нэр эсвэл Нийт дүн багана олдсонгүй.")
    
    
    
import pandas as pd
from pathlib import Path
import streamlit as st

# Файлын зам
BASE_DIR = Path(__file__).resolve().parent
file_path = BASE_DIR.parent / "data" / "Борлуулалтын авлага.xlsx"

# Excel файл унших
df = pd.read_excel(file_path)

# Харилцагч байхгүй мөрүүдэд "Харилцагчгүй" гэж онооно
df["Харилцагчийн нэр"] = df["Харилцагчийн нэр"].fillna("Харилцагчгүй")

# --- Авлагын эхний үлдэгдэл.xlsx файлыг унших ---
ehnii_uldegdel_file = BASE_DIR.parent / "data" / "Авлагын эхний үлдэгдэл.xlsx"
df_ehnii = pd.read_excel(ehnii_uldegdel_file)

# Харилцагч байхгүй мөрүүдэд "Харилцагчгүй" гэж онооно
df_ehnii["Харилцагчийн нэр"] = df_ehnii["Харилцагчийн нэр"].fillna("Харилцагчгүй")

# Харилцагчийн нэрээр бүлэглэж, эхний үлдэгдлийг нэгтгэнэ
ehnii_grouped = df_ehnii.groupby("Харилцагчийн нэр")["Эхний үлдэгдэл"].sum().reset_index()

# Үндсэн df дээр эхний үлдэгдэл багана нэмэх (merge хийх)
df_merged = df.merge(ehnii_grouped, on="Харилцагчийн нэр", how="left")
df_merged["Эхний үлдэгдэл"] = df_merged["Эхний үлдэгдэл"].fillna(0)

# Харилцагчийн нэрээр бүлэглэж, нийт дүн болон эхний үлдэгдлийг нэгтгэнэ
if "Харилцагчийн нэр" in df_merged.columns and "Нийт дүн" in df_merged.columns:
    grouped = df_merged.groupby("Харилцагчийн нэр")[["Нийт дүн", "Эхний үлдэгдэл"]].sum().reset_index()
    # Хөл дүн нэмэх
    total_row = pd.DataFrame([{
        "Харилцагчийн нэр": "Нийт",
        "Эхний үлдэгдэл": grouped["Эхний үлдэгдэл"].sum(),
        "Нийт дүн": grouped["Нийт дүн"].sum(),
        
    }])
    grouped_with_total = pd.concat([grouped, total_row], ignore_index=True)
    st.subheader("Харилцагчийн нэрээр бүлэглэсэн авлага болон эхний үлдэгдэл")
    st.dataframe(grouped_with_total.style.format({"Нийт дүн": "{:,.0f}", "Эхний үлдэгдэл": "{:,.0f}"}), use_container_width=True)
else:
    st.warning("Харилцагчийн нэр эсвэл Нийт дүн багана олдсонгүй.")
    
    
    
# ...existing code...

# Харилцагчийн нэрээр бүлэглэж, нийт дүн болон эхний үлдэгдлийг нэгтгэнэ
if "Харилцагчийн нэр" in df_merged.columns and "Нийт дүн" in df_merged.columns:
    grouped = df_merged.groupby("Харилцагчийн нэр")[["Эхний үлдэгдэл", "Нийт дүн"]].sum().reset_index()
    # Хөл дүн нэмэх
    total_row = pd.DataFrame([{
        "Харилцагчийн нэр": "Нийт",
        "Эхний үлдэгдэл": grouped["Эхний үлдэгдэл"].sum(),
        "Нийт дүн": grouped["Нийт дүн"].sum()
    }])
    grouped_with_total = pd.concat([grouped, total_row], ignore_index=True)
    st.subheader("Харилцагчийн нэрээр бүлэглэсэн авлага болон эхний үлдэгдэл")
    st.dataframe(grouped_with_total[["Харилцагчийн нэр", "Эхний үлдэгдэл", "Нийт дүн"]].style.format({"Нийт дүн": "{:,.0f}", "Эхний үлдэгдэл": "{:,.0f}"}), use_container_width=True)
else:
    st.warning("Харилцагчийн нэр эсвэл Нийт дүн багана олдсонгүй.")
    
    
# ...existing code...

# Харилцагчийн нэрээр бүлэглэж, нийт дүн болон эхний үлдэгдлийг нэгтгэнэ
if "Харилцагчийн нэр" in df_merged.columns and "Нийт дүн" in df_merged.columns:
    grouped = df_merged.groupby("Харилцагчийн нэр")[["Эхний үлдэгдэл", "Нийт дүн"]].sum().reset_index()
    grouped = grouped.rename(columns={"Нийт дүн": "Борлуулалтын авлага"})
    # Хөл дүн нэмэх
    total_row = pd.DataFrame([{
        "Харилцагчийн нэр": "Нийт",
        "Эхний үлдэгдэл": grouped["Эхний үлдэгдэл"].sum(),
        "Борлуулалтын авлага": grouped["Борлуулалтын авлага"].sum()
    }])
    grouped_with_total = pd.concat([grouped, total_row], ignore_index=True)
    st.subheader("Харилцагчийн нэрээр бүлэглэсэн авлага болон эхний үлдэгдэл")
    st.dataframe(
        grouped_with_total[["Харилцагчийн нэр", "Эхний үлдэгдэл", "Борлуулалтын авлага"]]
        .style.format({"Борлуулалтын авлага": "{:,.0f}", "Эхний үлдэгдэл": "{:,.0f}"}),
        use_container_width=True
    )
else:
    st.warning("Харилцагчийн нэр эсвэл Нийт дүн багана олдсонгүй.")
    
    
    
    
    
    
# --- Авлагын баримтын жагсаалт.xlsx-ээс авлага хасагдсан тооцоолох ---
barimt_file = BASE_DIR.parent / "data" / "Авлагын баримтын жагсаалт.xlsx"
df_barimt = pd.read_excel(barimt_file)
df_barimt["Харилцагчийн нэр"] = df_barimt["Харилцагчийн нэр"].fillna("Харилцагчгүй")

# Харилцагчийн нэрээр бүлэглэж, Кредит -₮ баганын нийлбэрийг тооцоолно
if "Харилцагчийн нэр" in df_barimt.columns and "Кредит -₮" in df_barimt.columns:
    avlaga_hasagdsan = df_barimt.groupby("Харилцагчийн нэр")["Кредит -₮"].sum().reset_index()
    avlaga_hasagdsan = avlaga_hasagdsan.rename(columns={"Кредит -₮": "Авлага хасагдсан"})
    # Хөл дүн нэмэх
    total_row = pd.DataFrame([{
        "Харилцагчийн нэр": "Нийт",
        "Авлага хасагдсан": avlaga_hasagdsan["Авлага хасагдсан"].sum()
    }])
    avlaga_hasagdsan_with_total = pd.concat([avlaga_hasagdsan, total_row], ignore_index=True)
    st.subheader("Харилцагчийн нэрээр бүлэглэсэн авлага хасагдсан дүн")
    st.dataframe(avlaga_hasagdsan_with_total.style.format({"Авлага хасагдсан": "{:,.0f}"}), use_container_width=True)
else:
    st.warning("Харилцагчийн нэр эсвэл Кредит -₮ багана олдсонгүй.")

# ...existing code...

# "Нийт дүн" баганыг "Борлуулалтын авлага" болгож нэрлэх
grouped = df_merged.groupby("Харилцагчийн нэр")[["Эхний үлдэгдэл", "Нийт дүн"]].sum().reset_index()
grouped = grouped.rename(columns={"Нийт дүн": "Борлуулалтын авлага"})

# ...existing code...

# --- Эцсийн үлдэгдэл тооцоолох ---
# ehnii_grouped: "Харилцагчийн нэр", "Эхний үлдэгдэл"
# grouped: "Харилцагчийн нэр", "Борлуулалтын авлага"
# avlaga_hasagdsan: "Харилцагчийн нэр", "Авлага хасагдсан"

# Шалгах: баганууд зөв нэртэй эсэх
# print(ehnii_grouped.columns)
# print(grouped.columns)
# print(avlaga_hasagdsan.columns)

# merge хийхдээ баганы нэрийг зөв байлгах
df_final = pd.merge(ehnii_grouped, grouped, on="Харилцагчийн нэр", how="outer")
df_final = pd.merge(df_final, avlaga_hasagdsan, on="Харилцагчийн нэр", how="outer")
df_final = df_final.fillna(0)

# Багануудыг заавал зөв нэртэй байлгах
for col in ["Эхний үлдэгдэл", "Борлуулалтын авлага", "Авлага хасагдсан"]:
    if col not in df_final.columns:
        df_final[col] = 0

df_final["Эцсийн үлдэгдэл"] = (
    df_final["Эхний үлдэгдэл"] + df_final["Борлуулалтын авлага"] - df_final["Авлага хасагдсан"]
)

# Хөл дүн нэмэх
total_row = pd.DataFrame([{
    "Харилцагчийн нэр": "Нийт",
    "Эхний үлдэгдэл": df_final["Эхний үлдэгдэл"].sum(),
    "Борлуулалтын авлага": df_final["Борлуулалтын авлага"].sum(),
    "Авлага хасагдсан": df_final["Авлага хасагдсан"].sum(),
    "Эцсийн үлдэгдэл": df_final["Эцсийн үлдэгдэл"].sum()
}])
df_final_with_total = pd.concat([df_final, total_row], ignore_index=True)

# ...existing code...

st.subheader("Харилцагчийн нэрээр бүлэглэсэн эцсийн авлагын үлдэгдэл")
st.dataframe(
    df_final_with_total[
        ["Харилцагчийн нэр", "Эхний үлдэгдэл", "Борлуулалтын авлага", "Авлага хасагдсан", "Эцсийн үлдэгдэл"]
    ].style.format({
        "Эхний үлдэгдэл": lambda x: f"{x:,.0f}" if isinstance(x, (int, float)) else x,
        "Борлуулалтын авлага": lambda x: f"{x:,.0f}" if isinstance(x, (int, float)) else x,
        "Авлага хасагдсан": lambda x: f"{x:,.0f}" if isinstance(x, (int, float)) else x,
        "Эцсийн үлдэгдэл": lambda x: f"{x:,.0f}" if isinstance(x, (int, float)) else x,
    }),
    use_container_width=True
)