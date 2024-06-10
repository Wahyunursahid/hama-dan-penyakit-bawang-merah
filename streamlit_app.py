import streamlit as st
import pandas as pd

# Baca data dari file Excel
file_path = 'UAS-PAKAR.xlsx'
df_penyakit = pd.read_excel(file_path, sheet_name='penyakit')
df_gejala = pd.read_excel(file_path, sheet_name='gejala')
df_hubungan = pd.read_excel(file_path, sheet_name='hubungan')

# Tampilkan nama kolom untuk memastikan nama kolom yang benar
st.write("Kolom pada dataframe gejala:", df_gejala.columns.tolist())

# Buat dictionary untuk menyimpan data CF
cf_data = {}

# Proses data penyakit
penyakit_dict = dict(zip(df_penyakit['id_penyakit'], df_penyakit['hama dan penyakit']))

# Proses data gejala
# Periksa nama kolom yang benar dan sesuaikan jika perlu
gejala_dict = dict(zip(df_gejala['id gejala'], df_gejala['gejala']))

# Proses data hubungan hama penyakit dengan gejala
for index, row in df_hubungan.iterrows():
    penyakit_id = row['jenis hama dan penyakit']
    gejala_ids = row['gejala'].split(',')
    
    if penyakit_id not in cf_data:
        cf_data[penyakit_id] = {}
    
    for gejala_id in gejala_ids:
        cf_data[penyakit_id][gejala_id] = 0  # Nilai CF default 0, nanti akan dihitung berdasarkan input pengguna

# Fungsi untuk menghitung Certainty Factor
def calculate_cf(symptoms):
    results = {}
    for disease, symptoms_cf in cf_data.items():
        combined_cf = 0
        for symptom, user_cf in symptoms.items():
            if symptom in symptoms_cf:
                combined_cf = combined_cf + user_cf * (1 - combined_cf)
        results[disease] = combined_cf
    return results

# Fungsi untuk konversi nilai CF dari deskripsi
def convert_cf(description):
    cf_values = {
        'Pasti': 1.0,
        'Hampir Pasti': 0.9,
        'Kemungkinan Besar': 0.8,
        'Mungkin': 0.7,
        'Tidak Tahu': 0.6,
        'Kemungkinan Tidak': 0.5,
        'Kemungkinan Besar Tidak': 0.4,
        'Hampir Pasti Tidak': 0.3,
        'Pasti Tidak': 0.2
    }
    return cf_values.get(description, 0.0)

# Streamlit UI
st.title('Diagnosa Hama dan Penyakit Tanaman Bawang Merah')
st.write('Pilih gejala yang terdeteksi pada tanaman bawang merah:')

input_symptoms = {}

for gejala_id, gejala_desc in gejala_dict.items():
    selected_cf = st.radio(f"{gejala_desc} ({gejala_id})", 
                           ['Tidak Tahu', 'Pasti Tidak', 'Hampir Pasti Tidak', 'Kemungkinan Besar Tidak', 'Kemungkinan Tidak', 'Mungkin', 'Kemungkinan Besar', 'Hampir Pasti', 'Pasti'])
    input_symptoms[gejala_id] = convert_cf(selected_cf)

# Hitung CF berdasarkan gejala input
if st.button('Diagnosa'):
    diagnosis = calculate_cf(input_symptoms)
    
    st.write("Hasil Diagnosa:")
    for disease_id, cf in diagnosis.items():
        disease_name = penyakit_dict[disease_id]
        st.write(f"Penyakit/Hama: {disease_name}, Certainty Factor: {cf:.2f}")
