import json
import numpy as np
import pandas as pd
import torch
from sklearn.model_selection import train_test_split

def load_data():
    with open('data/dane_clean.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    df = pd.DataFrame(data)

    # fill missing values
    df['rodzaj_zabudowy'] = df['rodzaj_zabudowy'].fillna('inne')

    # features used for training (dropped poziom and umeblowane — 82% nulls)
    features = ['miasto', 'powierzchnia', 'liczba_pokoi', 'rynek', 'rodzaj_zabudowy']
    target = 'cena_m2_pln'

    df = df[features + [target]].dropna()

    # remove outliers — realistic range for Polish apartments is 3000–50000 PLN/m²
    df = df[(df[target] >= 3000) & (df[target] <= 50000)]

    miasta = df['miasto'].values  # save city codes for stratification

    # one-hot encode categoricals — avoids implying false order between categories
    df = pd.get_dummies(df, columns=['miasto', 'rynek', 'rodzaj_zabudowy'])

    feature_cols = [c for c in df.columns if c != target]

    X = df[feature_cols].values.astype(np.float32)
    y = df[[target]].values.astype(np.float32)

    # normalize features so they're on a similar scale
    mean = X.mean(axis=0)
    std = X.std(axis=0)
    X = (X - mean) / std

    # normalize target the same way as features
    y_mean = y.mean()
    y_std = y.std()
    y = (y - y_mean) / y_std

    X_tensor = torch.tensor(X)
    y_tensor = torch.tensor(y)

    # stratify by city so each city is evenly represented in train and test
    X_train, X_test, y_train, y_test = train_test_split(X_tensor, y_tensor, test_size=0.2, random_state=42, stratify=miasta)

    print(f"Train: {len(X_train)} rekordow, Test: {len(X_test)} rekordow")
    print(f"Liczba features: {X.shape[1]}")

    return X_train, X_test, y_train, y_test, mean, std, y_mean, y_std

if __name__ == "__main__":
    X_train, X_test, y_train, y_test, mean, std, y_mean, y_std = load_data()
    print("X_train shape:", X_train.shape)
    print("y_train shape:", y_train.shape)
