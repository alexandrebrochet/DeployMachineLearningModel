
import os

import pytest
from dotenv import load_dotenv
from sqlalchemy import URL, create_engine, text
from sqlalchemy.orm import Session

from app.database.models import (
    PredictionInput,
    PredictionOutput,
)


TEST_DATABASE = "building_energy_test"

load_dotenv()


@pytest.fixture
def db_session():
    """Session de test avec annulation automatique des écritures."""

    url = URL.create(
        drivername="postgresql+psycopg",
        username=os.environ["DB_USER"],
        password=os.environ["DB_PASSWORD"],
        host=os.getenv("DB_HOST", "localhost"),
        port=int(os.getenv("DB_PORT", "5432")),
        database=TEST_DATABASE,
    )

    engine = create_engine(url, pool_pre_ping=True)

    try:
        # Vérification de sécurité avant toute écriture
        with engine.connect() as check_connection:
            database_name = check_connection.execute(
                text("SELECT current_database()")
            ).scalar_one()

            if database_name != TEST_DATABASE:
                raise RuntimeError(
                    "Base de test incorrecte : opération interdite"
                )

        connection = engine.connect()
        transaction = connection.begin()

        try:
            with Session(bind=connection) as session:
                yield session
        finally:
            transaction.rollback()
            connection.close()

    finally:
        engine.dispose()


def test_insert_prediction(db_session):
    """Vérifie l'enregistrement réel d'une prédiction."""

    entry = PredictionInput(
        building_age=25,
        primary_property_type="Large Office",
        number_of_buildings=1,
        property_gfa_total=120000,
    )

    db_session.add(entry)
    db_session.flush()

    assert entry.id is not None

    result = PredictionOutput(
        prediction_input_id=entry.id,
        predicted_energy_consumption=7055555.49,
        model_version="1.0",
    )

    db_session.add(result)
    db_session.flush()

    assert result.id is not None
    assert result.prediction_input_id == entry.id

    saved_input = db_session.get(
        PredictionInput,
        entry.id,
    )

    saved_output = db_session.get(
        PredictionOutput,
        result.id,
    )

    assert saved_input.building_age == 25
    assert saved_input.primary_property_type == "Large Office"

    assert (
        saved_output.predicted_energy_consumption
        == pytest.approx(7055555.49)
    )

    assert saved_output.model_version == "1.0"
