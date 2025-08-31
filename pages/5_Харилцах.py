import pandas as pd
from pathlib import Path
import streamlit as st
import glob

# Фолдерын зам
BASE_DIR = Path(__file__).resolve().parent
folder_path = BASE_DIR.parent / "data" / "харилцах"

# Бүх Excel файлыг авах (.xls болон .xlsx)
excel_files = glob.glob(str(folder_path / "*.xls")) + glob.glob(str(folder_path / "*.xlsx"))

# ...existing code...

df_list = []
for file in excel_files:
    try:
        df = pd.read_excel(file)
        # Зөвхөн эхний мөрийг хасах (сүүлийн 2 мөрийг оруулна)
        if len(df) > 1:
            df = df.iloc[1:].reset_index(drop=True)
        else:
            df = pd.DataFrame()  # 1 эсвэл түүнээс цөөн мөртэй бол хоосон болгоно
        if not df.empty:
            df["Файл нэр"] = Path(file).name
            df_list.append(df)
    except Exception as e:
        st.warning(f"{file} уншихад алдаа гарлаа: {e}")

if df_list:
    all_df = pd.concat(df_list, ignore_index=True)
    st.subheader("Харилцах фолдер дахь бүх Excel файлын нэгтгэсэн мэдээлэл (эхний мөргүй)")
    st.dataframe(all_df, use_container_width=True)
else:
    st.warning("Харилцах фолдерт Excel файлууд олдсонгүй.")