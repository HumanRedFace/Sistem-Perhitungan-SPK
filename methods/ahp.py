import pandas as pd
import numpy as np

def ahp(pairwise_matrix: pd.DataFrame, criteria: list):
    steps = []
    steps.append("Metode Analytic Hierarchy Process (AHP)\n")

    # Step 1: Hitung jumlah kolom
    col_sum = pairwise_matrix.sum()
    steps.append("Langkah 1: Jumlah Kolom pada Matriks Perbandingan Berpasangan")
    steps.append(col_sum.to_frame(name="Jumlah"))

    # Step 2: Normalisasi Matriks
    norm_matrix = pairwise_matrix / col_sum
    steps.append("Langkah 2: Normalisasi Matriks")
    steps.append(norm_matrix.round(4))

    # Step 3: Hitung rata-rata setiap baris = bobot kriteria
    weights = norm_matrix.mean(axis=1)
    weights_df = pd.DataFrame({
        "Kriteria": criteria,
        "Bobot": weights.round(4)
    })
    steps.append("Langkah 3: Bobot Kriteria (Rata-rata dari Matriks Normalisasi)")
    steps.append(weights_df)

    # Step 4: Konsistensi
    # Menghitung λ maks
    lambda_max = (pairwise_matrix @ weights).sum() / weights.sum()
    n = len(criteria)
    CI = (lambda_max - n) / (n - 1) if n > 1 else 0
    RI_dict = {1: 0.00, 2: 0.00, 3: 0.58, 4: 0.90, 5: 1.12, 6: 1.24, 7: 1.32, 8: 1.41, 9: 1.45, 10: 1.49}
    RI = RI_dict.get(n, 1.49)
    CR = CI / RI if RI != 0 else 0

    konsistensi_df = pd.DataFrame({
        "Lambda Maks": [lambda_max],
        "Consistency Index (CI)": [CI],
        "Random Index (RI)": [RI],
        "Consistency Ratio (CR)": [CR]
    })
    steps.append("Langkah 4: Perhitungan Konsistensi")
    steps.append(konsistensi_df)

    if CR < 0.1:
        steps.append("Hasil: Konsistensi DITERIMA karena CR < 0.1")
    else:
        steps.append("Hasil: Konsistensi TIDAK DITERIMA, harap periksa kembali nilai perbandingan.")

    return weights_df, steps
