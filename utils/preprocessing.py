import pandas as pd

def handle_uploaded_file(uploaded_file):
    """
    Membaca file yang diupload user,
    bisa format CSV atau Excel, dan mengembalikan dataframe.
    """
    if uploaded_file.name.endswith('.csv'):
        df = pd.read_csv(uploaded_file)
    elif uploaded_file.name.endswith(('.xls', '.xlsx')):
        df = pd.read_excel(uploaded_file)
    else:
        raise ValueError("Format file tidak didukung. Gunakan CSV atau Excel.")
    return df

def normalize_data(df, cost_benefit):
    """
    Normalisasi data berdasarkan cost/benefit.
    df: DataFrame dengan kolom Alternatif dan kriteria.
    cost_benefit: dict {kriteria: 'cost' atau 'benefit'}.

    Output: DataFrame normalisasi kriteria tanpa kolom Alternatif.
    """
    df_norm = df.copy()
    criteria = df.columns.tolist()[1:]  # asumsi kolom pertama adalah Alternatif

    for c in criteria:
        if cost_benefit[c] == 'benefit':
            max_val = df[c].max()
            if max_val == 0:
                df_norm[c] = 0
            else:
                df_norm[c] = df[c] / max_val
        else:  # cost
            min_val = df[c].min()
            # Hindari pembagian dengan nol
            df_norm[c] = min_val / df[c].replace(0, 1e-9)

    return df_norm
