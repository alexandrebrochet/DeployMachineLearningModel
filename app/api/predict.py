
import logging

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from app.database.connection import get_db
from app.database.models import (
    PredictionInput as PredictionInputDB,
    PredictionOutput as PredictionOutputDB,
)
from app.models.schemas import (
    BuildingInput,
    PredictionOutput as PredictionOutputSchema,
)
from app.services.prediction_service import predict_energy


logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/predict",
    tags=["Machine Learning"],
)


@router.post("", response_model=PredictionOutputSchema)
def predict(
    data: BuildingInput,
    db: Session = Depends(get_db),
):
    try:
        # 1. Enregistrer les caractéristiques reçues
        entry = PredictionInputDB(
            building_age=data.BuildingAge,
            primary_property_type=data.PrimaryPropertyType,
            number_of_buildings=data.NumberofBuildings,
            property_gfa_total=data.PropertyGFATotal,
        )

        db.add(entry)
        db.flush()

        # 2. Relire les données enregistrées
        db.refresh(entry)

        model_input = {
            "BuildingAge": entry.building_age,
            "PrimaryPropertyType": entry.primary_property_type,
            "NumberofBuildings": entry.number_of_buildings,
            "PropertyGFATotal": entry.property_gfa_total,
        }

        # 3. Effectuer la prédiction
        prediction = predict_energy(model_input)

        # 4. Enregistrer le résultat
        result = PredictionOutputDB(
            prediction_input_id=entry.id,
            predicted_energy_consumption=prediction,
            model_version="1.0",
        )

        db.add(result)

        # 5. Valider la transaction
        db.commit()

        return PredictionOutputSchema(
            predicted_energy_consumption=prediction,
            unit="kBtu",
        )

    except SQLAlchemyError:
        db.rollback()
        logger.exception("Erreur PostgreSQL pendant la prédiction")
        raise HTTPException(
            status_code=503,
            detail="Service de stockage temporairement indisponible",
        )

    except Exception:
        db.rollback()
        logger.exception("Erreur pendant la prédiction")
        raise HTTPException(
            status_code=500,
            detail="Erreur lors de la prédiction",
        )
