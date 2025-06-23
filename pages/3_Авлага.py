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
    st.subheader("Харилцагчийн нэрээр бүлэглэсэн борлуулалтаар үүссэн авлагын дүн (Харилцагчгүйг оролцуулсан)")
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
# st.subheader("эхний үлдэгдэл")
# st.dataframe(ehnii_grouped.style.format({"Нийт дүн": "{:,.0f}", "Эхний үлдэгдэл": "{:,.0f}"}), use_container_width=True)



# Үндсэн df дээр эхний үлдэгдэл багана нэмэх (merge хийх)
df_merged = df.merge(ehnii_grouped, on="Харилцагчийн нэр", how="left")
df_merged["Эхний үлдэгдэл"] = df_merged["Эхний үлдэгдэл"].fillna(0)

# Харилцагчийн нэрээр бүлэглэж, нийт дүн болон эхний үлдэгдлийг нэгтгэнэ
# ...existing code...

if "Харилцагчийн нэр" in df_merged.columns and "Нийт дүн" in df_merged.columns:
    grouped = df_merged.groupby("Харилцагчийн нэр").agg({
        "Нийт дүн": "sum",
        "Эхний үлдэгдэл": "first"  # эсвэл "max"
    }).reset_index()
    # Хөл дүн нэмэх
    total_row = pd.DataFrame([{
        "Харилцагчийн нэр": "Нийт",
        "Эхний үлдэгдэл": grouped["Эхний үлдэгдэл"].sum(),
        "Нийт дүн": grouped["Нийт дүн"].sum(),
    }])
    grouped_with_total = pd.concat([grouped, total_row], ignore_index=True)
    # st.subheader("Харилцагчийн нэрээр бүлэглэсэн авлага болон эхний үлдэгдэл")
    # st.dataframe(grouped_with_total.style.format({"Нийт дүн": "{:,.0f}", "Эхний үлдэгдэл": "{:,.0f}"}), use_container_width=True)
else:
    st.warning("Харилцагчийн нэр эсвэл Нийт дүн багана олдсонгүй.")

# ...existing code...
    
    
    
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
    # st.subheader("Харилцагчийн нэрээр бүлэглэсэн авлага болон эхний үлдэгдэл")
    # st.dataframe(grouped_with_total[["Харилцагчийн нэр", "Эхний үлдэгдэл", "Нийт дүн"]].style.format({"Нийт дүн": "{:,.0f}", "Эхний үлдэгдэл": "{:,.0f}"}), use_container_width=True)
else:
    st.warning("Харилцагчийн нэр эсвэл Нийт дүн багана олдсонгүй.")
    
    
# ...existing code...
# Харилцагчийн нэрээр бүлэглэж, нийт дүн болон эхний үлдэгдлийг нэгтгэнэ
if "Харилцагчийн нэр" in df_merged.columns and "Нийт дүн" in df_merged.columns:
    grouped = df_merged.groupby("Харилцагчийн нэр").agg({
        "Эхний үлдэгдэл": "first",  # эсвэл "max" гэж сольж болно
        "Нийт дүн": "sum"
    }).reset_index()
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
    
    
    


# --- Авлагын баримтын жагсаалт.xlsx файлыг унших ---
barimt_file = BASE_DIR.parent / "data" / "Авлагын баримтын жагсаалт.xlsx"
df_barimt = pd.read_excel(barimt_file)

# "Автомат клиринг" төрлийг хасах
if "Баримтын төрөл" in df_barimt.columns:
    df_barimt = df_barimt[df_barimt["Баримтын төрөл"] != "Автомат клиринг"]

# Харилцагч байхгүй мөрүүдэд "Харилцагчгүй" гэж онооно
df_barimt["Харилцагчийн нэр"] = df_barimt["Харилцагчийн нэр"].fillna("Харилцагчгүй")

# Хасагдсан дүнг харилцагчийн нэрээр нэгтгэх (жишээ нь "Кредит -₮" багана байгаа гэж үзэв)
if "Харилцагчийн нэр" in df_barimt.columns and "Кредит -₮" in df_barimt.columns:
    hasagdsan_grouped = df_barimt.groupby("Харилцагчийн нэр")["Кредит -₮"].sum().reset_index()
    hasagdsan_grouped = hasagdsan_grouped.rename(columns={"Кредит -₮": "Хасагдсан дүн"})
else:
    hasagdsan_grouped = pd.DataFrame(columns=["Харилцагчийн нэр", "Хасагдсан дүн"])

# Үндсэн df дээр хасагдсан дүн багана нэмэх (merge хийх)
df_merged = df_merged.merge(hasagdsan_grouped, on="Харилцагчийн нэр", how="left")
df_merged["Хасагдсан дүн"] = df_merged["Хасагдсан дүн"].fillna(0)

# Харилцагчийн нэрээр бүлэглэж, нийт дүн, эхний үлдэгдэл, хасагдсан дүнг нэгтгэнэ

if "Харилцагчийн нэр" in df_merged.columns and "Нийт дүн" in df_merged.columns:
    grouped = df_merged.groupby("Харилцагчийн нэр").agg({
        "Эхний үлдэгдэл": "first",
        "Нийт дүн": "sum",
        "Хасагдсан дүн": "first"  # эсвэл "max"
    }).reset_index()
    grouped = grouped.rename(columns={"Нийт дүн": "Борлуулалтын авлага"})
    # Хөл дүн нэмэх
    total_row = pd.DataFrame([{
        "Харилцагчийн нэр": "Нийт",
        "Эхний үлдэгдэл": grouped["Эхний үлдэгдэл"].sum(),
        "Борлуулалтын авлага": grouped["Борлуулалтын авлага"].sum(),
        "Хасагдсан дүн": grouped["Хасагдсан дүн"].sum()
    }])
    grouped_with_total = pd.concat([grouped, total_row], ignore_index=True)
    st.subheader("Харилцагчийн нэрээр бүлэглэсэн авлага, эхний үлдэгдэл, хасагдсан дүн")
    st.dataframe(
        grouped_with_total[["Харилцагчийн нэр", "Эхний үлдэгдэл", "Борлуулалтын авлага", "Хасагдсан дүн"]]
        .style.format({"Борлуулалтын авлага": "{:,.0f}", "Эхний үлдэгдэл": "{:,.0f}", "Хасагдсан дүн": "{:,.0f}"}),
        use_container_width=True
    )
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
df["Харилцагчийн нэр"] = df["Харилцагчийн нэр"].fillna("Харилцагчгүй")

# --- Авлагын эхний үлдэгдэл.xlsx файлыг унших ---
ehnii_uldegdel_file = BASE_DIR.parent / "data" / "Авлагын эхний үлдэгдэл.xlsx"
df_ehnii = pd.read_excel(ehnii_uldegdel_file)
df_ehnii["Харилцагчийн нэр"] = df_ehnii["Харилцагчийн нэр"].fillna("Харилцагчгүй")
ehnii_grouped = df_ehnii.groupby("Харилцагчийн нэр")["Эхний үлдэгдэл"].sum().reset_index()

# Үндсэн df дээр эхний үлдэгдэл багана нэмэх (merge хийх)
df_merged = df.merge(ehnii_grouped, on="Харилцагчийн нэр", how="left")
df_merged["Эхний үлдэгдэл"] = df_merged["Эхний үлдэгдэл"].fillna(0)

# --- Авлагын баримтын жагсаалт.xlsx файлыг унших ---
barimt_file = BASE_DIR.parent / "data" / "Авлагын баримтын жагсаалт.xlsx"
df_barimt = pd.read_excel(barimt_file)
df_barimt["Харилцагчийн нэр"] = df_barimt["Харилцагчийн нэр"].fillna("Харилцагчгүй")

# "Автомат клиринг" төрлийг хасах
if "Баримтын төрөл" in df_barimt.columns:
    df_barimt = df_barimt[df_barimt["Баримтын төрөл"] != "Автомат клиринг"]

# Хасагдсан дүнг зөвхөн "Авлага" тооцооны төрлөөр тооцох
if "Тооцооны төрөл" in df_barimt.columns:
    df_barimt = df_barimt[df_barimt["Тооцооны төрөл"] == "Авлага"]

# Хасагдсан дүнг харилцагчийн нэрээр нэгтгэх
if "Харилцагчийн нэр" in df_barimt.columns and "Кредит -₮" in df_barimt.columns:
    hasagdsan_grouped = df_barimt.groupby("Харилцагчийн нэр")["Кредит -₮"].sum().reset_index()
    hasagdsan_grouped = hasagdsan_grouped.rename(columns={"Кредит -₮": "Хасагдсан дүн"})
else:
    hasagdsan_grouped = pd.DataFrame(columns=["Харилцагчийн нэр", "Хасагдсан дүн"])

# Үндсэн df дээр хасагдсан дүн багана нэмэх (merge хийх)
df_merged = df_merged.merge(hasagdsan_grouped, on="Харилцагчийн нэр", how="left")
df_merged["Хасагдсан дүн"] = df_merged["Хасагдсан дүн"].fillna(0)

# Харилцагчийн нэрээр бүлэглэж, нийт дүн, эхний үлдэгдэл, хасагдсан дүнг нэгтгэнэ
if "Харилцагчийн нэр" in df_merged.columns and "Нийт дүн" in df_merged.columns:
    grouped = df_merged.groupby("Харилцагчийн нэр").agg({
        "Эхний үлдэгдэл": "first",
        "Нийт дүн": "sum",
        "Хасагдсан дүн": "first"
    }).reset_index()
    grouped = grouped.rename(columns={"Нийт дүн": "Борлуулалтын авлага"})
    # Эцсийн үлдэгдэл тооцоолох
    grouped["Эцсийн үлдэгдэл"] = grouped["Эхний үлдэгдэл"] + grouped["Борлуулалтын авлага"] - grouped["Хасагдсан дүн"]
    # Хөл дүн нэмэх
    total_row = pd.DataFrame([{
        "Харилцагчийн нэр": "Нийт",
        "Эхний үлдэгдэл": grouped["Эхний үлдэгдэл"].sum(),
        "Борлуулалтын авлага": grouped["Борлуулалтын авлага"].sum(),
        "Хасагдсан дүн": grouped["Хасагдсан дүн"].sum(),
        "Эцсийн үлдэгдэл": grouped["Эцсийн үлдэгдэл"].sum()
    }])
    grouped_with_total = pd.concat([grouped, total_row], ignore_index=True)
    st.subheader("Харилцагчийн нэрээр бүлэглэсэн авлага, эхний үлдэгдэл, хасагдсан дүн, эцсийн үлдэгдэл")
    st.dataframe(
        grouped_with_total[["Харилцагчийн нэр", "Эхний үлдэгдэл", "Борлуулалтын авлага", "Хасагдсан дүн", "Эцсийн үлдэгдэл"]]
        .style.format({
            "Борлуулалтын авлага": "{:,.0f}",
            "Эхний үлдэгдэл": "{:,.0f}",
            "Хасагдсан дүн": "{:,.0f}",
            "Эцсийн үлдэгдэл": "{:,.0f}"
        }),
        use_container_width=True
    )
else:
    st.warning("Харилцагчийн нэр эсвэл Нийт дүн багана олдсонгүй.")
    
    


# ...existing code...

# Эцсийн үлдэгдэл тооцоолох: Эхний үлдэгдэл + Борлуулалтын авлага - Хасагдсан дүн
if all(col in grouped_with_total.columns for col in ["Эхний үлдэгдэл", "Борлуулалтын авлага", "Хасагдсан дүн"]):
    grouped_with_total["Эцсийн үлдэгдэл"] = (
        grouped_with_total["Эхний үлдэгдэл"] +
        grouped_with_total["Борлуулалтын авлага"] -
        grouped_with_total["Хасагдсан дүн"]
    )
    st.subheader("Харилцагчийн нэрээр бүлэглэсэн эцсийн үлдэгдэл")
    st.dataframe(
        grouped_with_total[["Харилцагчийн нэр", "Эхний үлдэгдэл", "Борлуулалтын авлага", "Хасагдсан дүн", "Эцсийн үлдэгдэл"]]
        .style.format({
            "Борлуулалтын авлага": "{:,.0f}",
            "Эхний үлдэгдэл": "{:,.0f}",
            "Хасагдсан дүн": "{:,.0f}",
            "Эцсийн үлдэгдэл": "{:,.0f}"
        }),
        use_container_width=True
    )
else:
    st.warning("Эцсийн үлдэгдэл тооцоход шаардлагатай баганууд олдсонгүй.")


# --- Авлагын баримтын жагсаалт.xlsx файлыг унших ---
barimt_file = BASE_DIR.parent / "data" / "Авлагын баримтын жагсаалт.xlsx"
df_barimt = pd.read_excel(barimt_file)

# "Автомат клиринг" төрлийг хасах
if "Баримтын төрөл" in df_barimt.columns:
    df_barimt = df_barimt[df_barimt["Баримтын төрөл"] != "Автомат клиринг"]

# Харилцагч байхгүй мөрүүдэд "Харилцагчгүй" гэж онооно
df_barimt["Харилцагчийн нэр"] = df_barimt["Харилцагчийн нэр"].fillna("Харилцагчгүй")

# Хасагдсан дүнг Баримтын төрлөөр бүлэглэж харуулах
if "Баримтын төрөл" in df_barimt.columns and "Кредит -₮" in df_barimt.columns:
    hasagdsan_by_type = df_barimt.groupby("Баримтын төрөл")["Кредит -₮"].sum().reset_index()
    hasagdsan_by_type = hasagdsan_by_type.rename(columns={"Кредит -₮": "Хасагдсан дүн"})
    st.subheader("Хасагдсан дүнг баримтын төрлөөр бүлэглэн харуулах")
    st.dataframe(
        hasagdsan_by_type[["Баримтын төрөл", "Хасагдсан дүн"]].style.format({"Хасагдсан дүн": "{:,.0f}"}),
        use_container_width=True
    )
else:
    st.warning("Баримтын төрөл эсвэл Кредит -₮ багана олдсонгүй.")