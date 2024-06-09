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
    results = []
    for index, row in penyakit_gejala.iterrows():
        if row['Nama Gejala'].strip() in selected_gejala.keys():
            mb = row['MB'] * selected_gejala[row['Nama Gejala'].strip()]
            md = row['MD'] * selected_gejala[row['Nama Gejala'].strip()]
            cf = calculate_cf(mb, md)
            results.append((row['hama dan penyakit'], cf))
    
    if results:
        sorted_results = sorted(results, key=lambda x: x[1], reverse=True)
        for result in sorted_results:
            st.write(f"Hama/Penyakit: {result[0]}, Nilai Kepastian: {result[1]:.2f}")
    else:
        st.write("Tidak ada hama atau penyakit yang cocok dengan gejala yang dipilih.")

# Streamlit UI
st.balloons()
st.markdown("# Diagnosa Hama dan Penyakit")

st.write("Kami senang melihat Anda di sini. ✨ "
         "Aplikasi ini akan membantu Anda mendiagnosa hama dan penyakit berdasarkan gejala yang Anda inputkan.")

st.write("Silakan pilih nilai kepastian untuk setiap gejala:")

selected_gejala = {}
certainty_levels = {
    "Pasti Tidak": 0.2,
    "hampir Pasti Tidak": 0.3,
    "Kemungkinan Besar Tidak": 0.4,
    "Kemungkinan Tidak": 0.5,
    "Tidak Tahu": 0.6,
    "Mungkin": 0.7,
    "Kemungkinan Besar": 0.8,
    " Hampir Yakin": 0.9,
    "Sangat Yakin": 1.0
}

for gejala in gejala_list:
    choice = st.radio(f"{gejala}", list(certainty_levels.keys()))
    kepastian = certainty_levels[choice]
    if kepastian > 0:
        selected_gejala[gejala] = kepastian

if st.button("Submit"):
    st.write("Hasil Diagnosa:")
    diagnose(selected_gejala)

st.write("Terima kasih telah menggunakan aplikasi ini! :balloon:")
