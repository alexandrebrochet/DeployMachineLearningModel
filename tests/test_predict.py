from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_predict_success():
    response = client.post(
        "/predict",
        json={
            "BuildingAge": 25,
            "PrimaryPropertyType": "Large Office",
            "NumberofBuildings": 1,
            "PropertyGFATotal": 120000
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert "predicted_energy_consumption" in data
    assert isinstance(data["predicted_energy_consumption"], float)
    assert data["unit"] == "kBtu"


def test_predict_missing_field():
    response = client.post(
        "/predict",
        json={
            "BuildingAge": 25,
            "PrimaryPropertyType": "Large Office",
            "NumberofBuildings": 1
        }
    )

    assert response.status_code == 422


def test_predict_invalid_age():
    response = client.post(
        "/predict",
        json={
            "BuildingAge": -10,
            "PrimaryPropertyType": "Large Office",
            "NumberofBuildings": 1,
            "PropertyGFATotal": 120000
        }
    )

    assert response.status_code == 422


def test_predict_invalid_surface():
    response = client.post(
        "/predict",
        json={
            "BuildingAge": 25,
            "PrimaryPropertyType": "Large Office",
            "NumberofBuildings": 1,
            "PropertyGFATotal": 0
        }
    )

    assert response.status_code == 422

from unittest.mock import patch


def test_predict_model_error():
    payload = {
        "BuildingAge": 25,
        "PrimaryPropertyType": "Large Office",
        "NumberofBuildings": 1,
        "PropertyGFATotal": 120000
    }

    with patch(
        "app.api.predict.predict_energy",
        side_effect=RuntimeError("Modèle indisponible")
    ):
        response = client.post("/predict", json=payload)

    assert response.status_code == 500
    assert response.json() == {
        "detail": "Erreur lors de la prédiction"
    }

def test_home():
    response = client.get("/")

    assert response.status_code == 200
    assert response.json()["version"] == "0.3.0"


def test_health():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}