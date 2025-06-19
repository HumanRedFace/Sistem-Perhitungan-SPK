def normalize_data(df, cost_benefit):
    df_norm = df.copy()
    for col in df.columns[1:]:
        if col not in cost_benefit:
            continue
        if cost_benefit[col] == 'benefit':
            max_val = df[col].max()
            df_norm[col] = df[col] / max_val if max_val != 0 else 0
        elif cost_benefit[col] == 'cost':
            min_val = df[col].min()
            df_norm[col] = min_val / df[col]
    return df_norm
