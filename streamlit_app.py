import streamlit as st
import pandas as pd

# Load the Excel file
file_path = '/mnt/data/UAS-PAKAR.xlsx'
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

# Ensure there are no NaN values in 'Nama Penyakit'
penyakit_gejala['Nama Penyakit'] = penyakit_gejala['Nama Penyakit'].fillna('Unknown')

# Define function to calculate Certainty Factor
def calculate_cf(mb, md):
    return mb - md

# Define diagnosis function
def diagnose(selected_gejala):
    results = {penyakit: 0 for penyakit in tabel1['hama dan penyakit'].tolist()}
    
    for index, row in penyakit_gejala.iterrows():
        if row['Nama Gejala'].strip() in selected_gejala.keys():
            mb = row['MB'] * selected_gejala[row['Nama Gejala'].strip()]
            md = row['MD'] * selected_gejala[row['Nama Gejala'].strip()]
            cf = calculate_cf(mb, md)
            if row['Nama Penyakit'] in results:
                results[row['Nama Penyakit']] += cf
            else:
                results['Unknown'] += cf

    total_cf = sum(results.values()) if sum(results.values()) != 0 else 1  # To prevent division by zero
    sorted_results = sorted(results.items(), key=lambda x: x[1], reverse=True)
    
    for result in sorted_results:
        percentage = (result[1] / total_cf) * 100
        st.write(f"Hama/Penyakit: {result[0]}, Persentase Kepastian: {percentage:.2f}%")

# Streamlit UI
st.title("Sistem Diagnosa Hama dan Penyakit")

st.write("Masukan Skala Keyakinan Pada Gejala Anda:")
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

selected_gejala = {}
for gejala in gejala_list:
    choice = st.selectbox(f"{gejala}:", options=list(certainty_levels.keys()), index=4)  # Default to "Tidak Tahu"
    selected_gejala[gejala] = certainty_levels[choice]

if st.button("Diagnosa Sekarang"):
    st.write("Hasil Diagnosa:")
    diagnose(selected_gejala)

st.write("Terima kasih telah menggunakan aplikasi ini!")
