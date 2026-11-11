
from unittest.mock import MagicMock, patch

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.exc import SQLAlchemyError

from app.main import app
from app.database.connection import get_db


client = TestClient(app)

VALID_PAYLOAD = {
    "BuildingAge": 25,
    "PrimaryPropertyType": "Large Office",
    "NumberofBuildings": 1,
    "PropertyGFATotal": 120000,
}


@pytest.fixture(autouse=True)
def mock_database():
    """Isole tous les tests de la vraie base PostgreSQL."""
    db = MagicMock()

    def override_get_db():
        yield db

    app.dependency_overrides[get_db] = override_get_db

    try:
        yield db
    finally:
        app.dependency_overrides.clear()


def test_predict_success(mock_database):
    response = client.post("/predict", json=VALID_PAYLOAD)

    assert response.status_code == 200

    data = response.json()

    assert "predicted_energy_consumption" in data
    assert isinstance(
        data["predicted_energy_consumption"], float
    )
    assert data["unit"] == "kBtu"

    mock_database.add.assert_called()
    assert mock_database.add.call_count == 2
    mock_database.flush.assert_called_once()
    mock_database.refresh.assert_called_once()
    mock_database.commit.assert_called_once()


def test_predict_missing_field(mock_database):
    payload = VALID_PAYLOAD.copy()
    del payload["PropertyGFATotal"]

    response = client.post("/predict", json=payload)

    assert response.status_code == 422
    mock_database.add.assert_not_called()


def test_predict_invalid_age(mock_database):
    payload = VALID_PAYLOAD.copy()
    payload["BuildingAge"] = -10

    response = client.post("/predict", json=payload)

    assert response.status_code == 422
    mock_database.add.assert_not_called()


def test_predict_invalid_surface(mock_database):
    payload = VALID_PAYLOAD.copy()
    payload["PropertyGFATotal"] = 0

    response = client.post("/predict", json=payload)

    assert response.status_code == 422
    mock_database.add.assert_not_called()


def test_predict_model_error(mock_database):
    with patch(
        "app.api.predict.predict_energy",
        side_effect=RuntimeError("Modèle indisponible"),
    ):
        response = client.post(
            "/predict",
            json=VALID_PAYLOAD,
        )

    assert response.status_code == 500
    assert response.json() == {
        "detail": "Erreur lors de la prédiction"
    }

    mock_database.rollback.assert_called_once()
    mock_database.commit.assert_not_called()


def test_database_error(mock_database):
    """Une erreur SQLAlchemy doit retourner HTTP 503."""
    mock_database.flush.side_effect = SQLAlchemyError(
        "Base indisponible"
    )

    response = client.post(
        "/predict",
        json=VALID_PAYLOAD,
    )

    assert response.status_code == 503
    assert response.json() == {
        "detail": "Service de stockage temporairement indisponible"
    }

    mock_database.rollback.assert_called_once()
    mock_database.commit.assert_not_called()


def test_database_commit_error(mock_database):
    """Un échec du commit doit provoquer un rollback."""
    mock_database.commit.side_effect = SQLAlchemyError(
        "Erreur de transaction"
    )

    response = client.post(
        "/predict",
        json=VALID_PAYLOAD,
    )

    assert response.status_code == 503
    mock_database.rollback.assert_called_once()


def test_prediction_values_saved(mock_database):
    """Vérifie les objets transmis à SQLAlchemy."""
    with patch(
        "app.api.predict.predict_energy",
        return_value=7055555.49,
    ) as mocked_prediction:
        response = client.post(
            "/predict",
            json=VALID_PAYLOAD,
        )

    assert response.status_code == 200

    entry = mock_database.add.call_args_list[0].args[0]
    result = mock_database.add.call_args_list[1].args[0]

    assert entry.building_age == 25
    assert entry.primary_property_type == "Large Office"
    assert entry.number_of_buildings == 1
    assert entry.property_gfa_total == 120000

    mocked_prediction.assert_called_once_with(
        {
            "BuildingAge": 25,
            "PrimaryPropertyType": "Large Office",
            "NumberofBuildings": 1,
            "PropertyGFATotal": 120000,
        }
    )

    assert result.predicted_energy_consumption == 7055555.49
    assert result.model_version == "1.0"
    mock_database.commit.assert_called_once()


def test_home():
    response = client.get("/")

    assert response.status_code == 200
    assert response.json()["version"] == "0.3.0"


def test_health():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
