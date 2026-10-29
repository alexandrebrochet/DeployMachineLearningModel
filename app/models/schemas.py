from pydantic import BaseModel, Field, ConfigDict


class BuildingInput(BaseModel):
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "BuildingAge": 25,
                "PrimaryPropertyType": "Large Office",
                "NumberofBuildings": 1,
                "PropertyGFATotal": 120000
            }
        }
    )

    BuildingAge: int = Field(ge=0, le=300)
    PrimaryPropertyType: str = Field(min_length=1)
    NumberofBuildings: int = Field(ge=1)
    PropertyGFATotal: float = Field(gt=0)


class PredictionOutput(BaseModel):
    predicted_energy_consumption: float
    unit: str = "kBtu"