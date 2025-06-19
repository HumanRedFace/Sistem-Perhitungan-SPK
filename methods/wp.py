import pandas as pd
import numpy as np

def wp(df, cost_benefit: dict, weights: list):
    steps = []
    steps.append("Metode Weighted Product (WP)\n")
    data = df.copy()
    alternatives = data["Alternatif"].values
    criteria = data.columns[1:]
    matrix = data[criteria].astype(float)

    # Transform cost menjadi 1/nilai
    steps.append("Langkah 1: Transformasi nilai untuk kriteria bertipe cost (1/x)")
    for i, c in enumerate(criteria):
        if cost_benefit[c] == "cost":
            matrix[c] = 1 / matrix[c]

    steps.append(matrix.round(4).copy())

    # Normalisasi bobot
    steps.append("Langkah 2: Normalisasi bobot kriteria (w/sum(w))")
    weights = np.array(weights)
    weights = weights / weights.sum()
    steps.append(f"Bobot Ternormalisasi: {np.round(weights, 4)}")

    # Perhitungan skor
    steps.append("Langkah 3: Hitung nilai preferensi (Skor)\nRumus: Skor = ∏(x_ij^w_j)")
    scores = np.prod(matrix ** weights, axis=1)

    result = pd.DataFrame({
        "Alternatif": alternatives,
        "Skor": scores
    }).sort_values(by="Skor", ascending=False).reset_index(drop=True)
    result["Ranking"] = result.index + 1

    steps.append("Langkah 4: Hasil Akhir")
    steps.append(result.copy())

    return result, steps
