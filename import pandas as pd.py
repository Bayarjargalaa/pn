import pandas as pd
import os

output_filename = "filtered_data1.xlsx"





file_path = "2023,03,18-2025,5,31.xlsx"
columns_to_select = [0, 1, 2, 4, 7, 8, 11,]
df_filtered = pd.read_excel(file_path, usecols=columns_to_select, skiprows=6)
df_filtered.to_excel(output_filename, index=False)
print(df_filtered.head())

df_filtered = df_filtered.rename(columns={
    'Unnamed: 4': 'Гүйлгээний утга',
    'Unnamed: 7': 'Дүн', 
    'Кредит\n': 'Кредит',
})

# # Бүрэн замыг хэвлэх
full_path = os.path.abspath(output_filename)
print("Файл хадгалагдсан зам:", full_path)
# Бүлэглэж, 'Дүн' баганын нийлбэрийг тооцох
grouped = df_filtered.groupby(['Дебет', 'Кредит',  ])['Дүн'].sum().reset_index()



grouped.to_excel("grouped_data_debit.xlsx", index=False)
print("Бүлэглэсэн өгөгдөл хадгалагдсан:", os.path.abspath("grouped_data_debit.xlsx"))
print(df_filtered.head())
# df=pd.read_excel(file_path, skiprows=6)
# print(df.columns)
