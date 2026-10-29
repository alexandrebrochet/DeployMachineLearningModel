from fastapi import APIRouter, HTTPException

from app.models.schemas import BuildingInput, PredictionOutput
from app.services.prediction_service import predict_energy

router = APIRouter(
    prefix="/predict",
    tags=["Machine Learning"]
)


@router.post("", response_model=PredictionOutput)
def predict(data: BuildingInput):
    try:
        prediction = predict_energy(data.model_dump())

        return PredictionOutput(
            predicted_energy_consumption=prediction,
            unit="kBtu"
        )

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Erreur lors de la prédiction"
        )