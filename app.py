import streamlit as st
import pandas as pd
from utils.visualization import plot_ranking
from utils.preprocessing import normalize_data
from methods.saw import saw
from methods.wp import wp
from methods.topsis import topsis

st.set_page_config(page_title="SPK Calculation", layout="wide")
st.title("Sistem Pendukung Keputusan (SPK)")

# Terapkan style CSS
with open("assets/style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

input_mode = st.radio("Input data via:", ("Upload file Excel/CSV", "Input manual data"))

# =============================== MODE UPLOAD ===================================
if input_mode == "Upload file Excel/CSV":
    uploaded_file = st.file_uploader("Upload file Excel dengan 2 sheet: DataAlternatif dan Kriteria", type=["xlsx"])

    with st.expander("Lihat contoh format Excel yang benar"):
        st.markdown("""
        File harus memiliki 2 sheet:
        - **DataAlternatif**: Kolom pertama = Alternatif, kolom lainnya = kriteria
        - **Kriteria**: Kolom = Kriteria | CostBenefit | Bobot

        Contoh CostBenefit: `cost`, `benefit`
        Total Bobot harus = 1.0
        """)

    if uploaded_file is not None:
        try:
            xls = pd.ExcelFile(uploaded_file)
            df = pd.read_excel(xls, sheet_name="DataAlternatif")
            df_kriteria = pd.read_excel(xls, sheet_name="Kriteria")

            st.markdown("### Data Alternatif")
            st.dataframe(df)

            st.markdown("### Data Kriteria")
            st.dataframe(df_kriteria)

            cost_benefit = dict(zip(df_kriteria["Kriteria"], df_kriteria["CostBenefit"].str.lower()))
            bobot_dict = dict(zip(df_kriteria["Kriteria"], df_kriteria["Bobot"]))

            criteria_names = df.columns[1:]
            bobot_list = [bobot_dict[name] for name in criteria_names]

            metode = st.selectbox("Pilih Metode SPK", ["SAW", "WP", "TOPSIS", "AHP"], key="select_metode_upload")
            if st.button("Hitung dan Tampilkan Hasil", key="btn_upload"):
                df_norm = normalize_data(df, cost_benefit)

                if metode == "SAW":
                    result, steps = saw(df_norm, cost_benefit, bobot_list)
                elif metode == "WP":
                    result, steps = wp(df_norm, cost_benefit, bobot_list)
                else:
                    result, steps = topsis(df, cost_benefit, bobot_list)

                st.markdown("### Tahapan Perhitungan")
                for step in steps:
                    if isinstance(step, pd.DataFrame):
                        st.dataframe(step)
                    else:
                        st.markdown(f"```\n{step}\n```")

                st.markdown("### Hasil Ranking")
                st.dataframe(result)
                st.plotly_chart(plot_ranking(result), use_container_width=True)

        except Exception as e:
            st.error(f"Format file tidak sesuai atau sheet tidak ditemukan.\n\nDetail error: {e}")
            st.stop()

# ============================= MODE MANUAL INPUT ================================
else:
    n_criteria = st.number_input("Jumlah kriteria", min_value=1, max_value=10, value=3, step=1)
    st.markdown("### Masukkan nama kriteria, tipe cost/benefit, dan bobot")

    criteria_data = []
    cols1 = st.columns([4, 3, 3])
    cols1[0].markdown("**Nama Kriteria**")
    cols1[1].markdown("**Cost / Benefit**")
    cols1[2].markdown("**Bobot (misal 0.2)**")

    for i in range(n_criteria):
        c_name = cols1[0].text_input(f"Nama kriteria #{i+1}", value=f"Kriteria{i+1}", key=f"krit{i}")
        c_cb = cols1[1].selectbox(f"Cost/Benefit #{i+1}", ["Benefit", "Cost"], index=0, key=f"cb{i}")
        c_weight = cols1[2].number_input(f"Bobot #{i+1}", min_value=0.0, max_value=1.0, value=round(1/n_criteria,2), step=0.01, format="%.2f", key=f"weight{i}")
        criteria_data.append({'name': c_name, 'cb': c_cb.lower(), 'weight': c_weight})

    total_weight = sum(row['weight'] for row in criteria_data)
    if total_weight > 1.0:
        st.error(f"Total bobot melebihi 1.00! Saat ini: {total_weight:.2f}. Silakan kurangi salah satu bobot.")
        st.stop()

    df_criteria = pd.DataFrame(criteria_data)
    st.markdown("#### Preview Kriteria yang sudah diinput:")
    st.dataframe(df_criteria)

    n_alternatives = st.number_input("Jumlah alternatif", min_value=1, max_value=20, value=3, step=1)
    st.markdown("### Masukkan nama alternatif dan nilai tiap kriteria")

    data = {"Alternatif": []}
    for c in df_criteria['name']:
        data[c] = []

    for i in range(n_alternatives):
        cols = st.columns(n_criteria + 1)
        alt_name = cols[0].text_input(f"Nama alternatif #{i+1}", value=f"Alt{i+1}", key=f"alt{i}")
        data["Alternatif"].append(alt_name)

        for j, c in enumerate(df_criteria['name']):
            is_cost = df_criteria.loc[df_criteria['name'] == c, 'cb'].values[0] == 'cost'
            input_label = f"Nilai {c} untuk alternatif #{i+1}"

            with cols[j+1]:
                if is_cost:
                    st.markdown("**Rp**", help="Karena kriteria ini bertipe cost.")
                val = st.number_input(
                    input_label,
                    key=f"val_{i}_{j}",
                    min_value=0.0,
                    format="%.0f",
                    value=0.0
                )
            data[c].append(val)

    df = pd.DataFrame(data)
    st.dataframe(df)

    metode = st.selectbox("Pilih Metode SPK", ["SAW", "WP", "TOPSIS", "AHP"], key="select_metode_manual")
    if st.button("Hitung dan Tampilkan Hasil", key="btn_manual"):
        cost_benefit = {row['name']: row['cb'] for row in criteria_data}
        bobot_dict = {row['name']: row['weight'] for row in criteria_data}
        criteria_names = df.columns[1:]
        bobot_list = [bobot_dict[name] for name in criteria_names]

        df_norm = normalize_data(df, cost_benefit)

        if metode == "SAW":
            result, steps = saw(df_norm, cost_benefit, bobot_list)
        elif metode == "WP":
            result, steps = wp(df_norm, cost_benefit, bobot_list)
        else:
            result, steps = topsis(df, cost_benefit, bobot_list)

        st.markdown("### Tahapan Perhitungan")
        for step in steps:
            if isinstance(step, pd.DataFrame):
                st.dataframe(step)
            else:
                st.markdown(f"```\n{step}\n```")

        st.markdown("### Hasil Ranking")
        st.dataframe(result)
        st.plotly_chart(plot_ranking(result), use_container_width=True)
