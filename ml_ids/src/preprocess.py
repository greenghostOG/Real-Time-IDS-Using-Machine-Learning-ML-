def preprocess(df):
    cols = [c for c in df.columns if c not in ['label']]
    return df[cols]
