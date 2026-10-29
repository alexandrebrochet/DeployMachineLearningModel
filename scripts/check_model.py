from pathlib import Path
import joblib

MODEL_PATH = (
    Path(__file__).resolve().parents[1]
    / "app"
    / "models"
    / "building_energy_model.joblib"
)

model = joblib.load(MODEL_PATH)

print("Modèle chargé :", type(model).__name__)
print("Variables attendues :", model.feature_names_in_.tolist())