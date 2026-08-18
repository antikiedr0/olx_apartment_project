import json
import torch
import numpy as np
import pandas as pd
from model import Model

def predict(powierzchnia, liczba_pokoi, miasto, rynek, rodzaj_zabudowy, umeblowane=False):
    # load full dataset to get the same column structure as during training
    with open('data/dane_clean.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    df = pd.DataFrame(data)
    df['rodzaj_zabudowy'] = df['rodzaj_zabudowy'].fillna('inne')
    df['umeblowane'] = (df['umeblowane'] == 'tak').astype(int)

    features = ['miasto', 'powierzchnia', 'liczba_pokoi', 'rynek', 'rodzaj_zabudowy', 'umeblowane']
    target = 'cena_m2_pln'

    df = df[features + [target]].dropna(subset=[c for c in features if c != 'umeblowane'] + [target])
    df = df[(df[target] >= 3000) & (df[target] <= 50000)]
    df = pd.get_dummies(df, columns=['miasto', 'rynek', 'rodzaj_zabudowy'])

    feature_cols = [c for c in df.columns if c != target]

    # build single-row DataFrame for the input
    input_df = pd.DataFrame([{
        'powierzchnia': powierzchnia,
        'liczba_pokoi': liczba_pokoi,
        'miasto': miasto,
        'rynek': rynek,
        'rodzaj_zabudowy': rodzaj_zabudowy,
        'umeblowane': int(umeblowane),
    }])
    input_df = pd.get_dummies(input_df, columns=['miasto', 'rynek', 'rodzaj_zabudowy'])

    # align columns with training data — missing one-hot columns become 0
    input_df = input_df.reindex(columns=feature_cols, fill_value=0)

    X = input_df.values.astype(np.float32)

    # normalize with training stats
    mean = df[feature_cols].values.astype(np.float32).mean(axis=0)
    std = df[feature_cols].values.astype(np.float32).std(axis=0)
    X = (X - mean) / std

    y_mean = df[target].values.astype(np.float32).mean()
    y_std = df[target].values.astype(np.float32).std()

    model = Model()
    model.load_state_dict(torch.load('model/model.pth'))
    model.eval()

    tensor = torch.tensor(X)
    with torch.no_grad():
        pred_norm = model(tensor)

    cena_m2 = pred_norm.item() * y_std + y_mean
    cena_calkowita = cena_m2 * powierzchnia
    print(f"Przewidywana cena za m²: {cena_m2:.0f} PLN/m²")
    print(f"Przewidywana cena calkowita: {cena_calkowita:.0f} PLN")
    return cena_m2


if __name__ == "__main__":
    predict(
        powierzchnia=100,
        liczba_pokoi=4,
        miasto='bydgoszcz',
        rynek='wtorny',
        rodzaj_zabudowy='apartament',
        umeblowane=True,
    )
