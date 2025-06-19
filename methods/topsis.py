import pandas as pd
import numpy as np

def topsis(df, cost_benefit: dict, weights: list):
    """
    Metode TOPSIS
    - df: DataFrame asli (bukan dinormalisasi)
    - cost_benefit: dict nama_kriteria: cost/benefit
    - weights: list sesuai urutan kolom kriteria
    """
    steps = []
    data = df.copy()
    alternatives = data["Alternatif"]
    criteria = data.columns[1:]
    matrix = data[criteria].astype(float)

    weights = np.array(weights)
    weights = weights / weights.sum()

    # Normalisasi
    norm_matrix = matrix / np.sqrt((matrix**2).sum())
    steps.append("Matrix Normalisasi:")
    steps.append(pd.DataFrame(norm_matrix, columns=criteria))

    # Matriks tertimbang
    weighted_matrix = norm_matrix * weights
    steps.append("Matrix Tertimbang:")
    steps.append(pd.DataFrame(weighted_matrix, columns=criteria))

    # Ideal positif dan negatif
    ideal_positive = []
    ideal_negative = []
    for i, c in enumerate(criteria):
        if cost_benefit[c] == "benefit":
            ideal_positive.append(weighted_matrix[c].max())
            ideal_negative.append(weighted_matrix[c].min())
        else:
            ideal_positive.append(weighted_matrix[c].min())
            ideal_negative.append(weighted_matrix[c].max())

    # Hitung jarak
    dist_pos = np.sqrt(np.sum((weighted_matrix - ideal_positive) ** 2, axis=1))
    dist_neg = np.sqrt(np.sum((weighted_matrix - ideal_negative) ** 2, axis=1))

    # Skor preferensi
    scores = dist_neg / (dist_pos + dist_neg)

    df_result = pd.DataFrame({
        "Alternatif": alternatives,
        "Skor": scores
    }).sort_values(by="Skor", ascending=False).reset_index(drop=True)
    df_result["Ranking"] = df_result.index + 1

    steps.append("Jarak Ideal Positif & Negatif:")
    steps.append(pd.DataFrame({
        "Jarak Positif": dist_pos,
        "Jarak Negatif": dist_neg
    }))

    steps.append("Hasil Skor dan Ranking:")
    steps.append(df_result.copy())

    return df_result, steps
