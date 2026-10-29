from pathlib import Path

import joblib
import pandas as pd


MODEL_PATH = (
    Path(__file__).resolve().parents[1]
    / "models"
    / "building_energy_model.joblib"
)

_model = None


def get_model():
    global _model

    if _model is None:
        _model = joblib.load(MODEL_PATH)

    return _model


def predict_energy(data: dict) -> float:
    model = get_model()

    input_data = pd.DataFrame([data])

    prediction = model.predict(input_data)

    return float(prediction[0])