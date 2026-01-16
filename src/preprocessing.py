def encode_categories(df, liste=None):
    if liste is None:
        liste = ['service', 'proto', 'conn_state']
        
    for col in liste:
        df[col] = df[col].astype('category')
    return df
