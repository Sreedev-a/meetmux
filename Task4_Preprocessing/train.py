import yaml
import joblib

from sklearn.model_selection import train_test_split

from src.data_loader import load_data
from src.preprocess import build_preprocessor

with open("config/config.yaml", "r") as f:
    config = yaml.safe_load(f)

print(config["data"]["path"])

import os
print(os.path.exists(config["data"]["path"]))

df = load_data(config["data"]["path"])

X = df.drop("target", axis=1)
y = df["target"]

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=config["model"]["test_size"],
    random_state=42
)

preprocessor = build_preprocessor(X_train)

preprocessor.fit(X_train)

joblib.dump(preprocessor, "models/preprocessor.pkl")

print("Preprocessor trained and saved successfully.")