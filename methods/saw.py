import pandas as pd

def saw(df_norm: pd.DataFrame, cost_benefit: dict, weights: list):
    steps = []
    criteria = df_norm.columns[1:]
    steps.append("Metode Simple Additive Weighting (SAW)\n")
    steps.append("Langkah 1: Matriks Normalisasi")
    steps.append(df_norm.copy())

    steps.append("Langkah 2: Hitung Skor Preferensi\nRumus: Skor = Σ(w_j * x_ij)")
    skor = []
    for idx, row in df_norm.iterrows():
        total = 0
        detail = []
        for i, c in enumerate(criteria):
            w = weights[i]
            val = row[c]
            total += w * val
            detail.append(f"{w:.3f}×{val:.3f}")
        skor.append(total)
        steps.append(f"{row['Alternatif']}: " + " + ".join(detail) + f" = {total:.4f}")

    df_result = pd.DataFrame({
        "Alternatif": df_norm["Alternatif"],
        "Skor": skor
    }).sort_values(by="Skor", ascending=False).reset_index(drop=True)
    df_result["Ranking"] = df_result.index + 1

    steps.append("Langkah 3: Hasil Akhir")
    steps.append(df_result.copy())

    return df_result, steps
