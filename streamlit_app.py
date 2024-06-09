import streamlit as st
import pandas as pd

# Load the Excel file
file_path = 'UAS-PAKAR.xlsx'
xls = pd.ExcelFile(file_path)

# Load sheets
tabel1 = pd.read_excel(xls, sheet_name='tabel1')
tabel2 = pd.read_excel(xls, sheet_name='tabel2')
tabel3 = pd.read_excel(xls, sheet_name='tabel3')
tabel4 = pd.read_excel(xls, sheet_name='tabel4')
tabel5 = pd.read_excel(xls, sheet_name='tabel5')

# Prepare data
gejala_list = tabel2['gejala'].tolist()

# Clean column names by stripping extra spaces
tabel3.columns = tabel3.columns.str.strip()

# Perform the merge operation using the cleaned column names
penyakit_gejala = pd.merge(tabel3, tabel1, left_on='Nama Penyakit', right_on='hama dan penyakit', how='left')
penyakit_gejala['MB'] = penyakit_gejala['MB'].str.replace(',', '.').astype(float)
penyakit_gejala['MD'] = penyakit_gejala['MD'].str.replace(',', '.').astype(float)

# Define function to calculate Certainty Factor
def calculate_cf(mb, md):
    return mb - md

# Define diagnosis function
def diagnose(selected_gejala):
    results = {penyakit: 0 for penyakit in tabel1['hama dan penyakit'].tolist()}
    total_cf = 0
    for index, row in penyakit_gejala.iterrows():
        if row['Nama Gejala'].strip() in selected_gejala.keys():
            mb = row['MB'] * selected_gejala[row['Nama Gejala'].strip()]
            md = row['MD'] * selected_gejala[row['Nama Gejala'].strip()]
            cf = calculate_cf(mb, md)
            results[row['Nama Penyakit']] += cf
            total_cf += cf
    
    if results:
        sorted_results = sorted(results.items(), key=lambda x: x[1], reverse=True)
        total_cf = sum(results.values()) if sum(results.values()) != 0 else 1  # To prevent division by zero
        for result in sorted_results:
            percentage = (result[1] / total_cf) * 100
            st.write(f"Hama/Penyakit: {result[0]}, Persentase Kepastian: {percentage:.2f}%")
    else:
        st.write("Tidak ada hama atau penyakit yang cocok dengan gejala yang dipilih.")

# Streamlit UI
st.markdown("# Diagnosa Hama dan Penyakit")

st.write("Kami senang melihat Anda di sini. ✨ "
         "Aplikasi ini akan membantu Anda mendiagnosa hama dan penyakit berdasarkan gejala yang Anda inputkan.")

st.write("Silakan pilih nilai kepastian untuk setiap gejala:")

selected_gejala = {}
certainty_levels = {
    "Pasti Tidak": 0.2,
    "Hampir Pasti Tidak": 0.3,
    "Kemungkinan Besar Tidak": 0.4,
    "Kemungkinan Tidak": 0.5,
    "Tidak Tahu": 0.6,
    "Mungkin": 0.7,
    "Kemungkinan Besar": 0.8,
    "Hampir Yakin": 0.9,
    "Sangat Yakin": 1.0
}

gejala_values = {}
for gejala in gejala_list:
    gejala_values[gejala] = st.radio(f"{gejala}", list(certainty_levels.keys()), index=0)

if st.button("Submit"):
    for gejala in gejala_list:
        choice = gejala_values[gejala]
        kepastian = certainty_levels[choice]
        if kepastian > 0:
            selected_gejala[gejala] = kepastian

    st.write("Hasil Diagnosa:")
    diagnose(selected_gejala)

st.write("Terima kasih telah menggunakan aplikasi ini!")
