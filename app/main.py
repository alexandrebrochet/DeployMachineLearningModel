from fastapi import FastAPI
from app.api.predict import router as predict_router

app = FastAPI(
    title="Machine Learning API",
    description="API de prédiction de la consommation énergétique des bâtiments",
    version="0.3.0"
)

app.include_router(predict_router)


@app.get("/", tags=["General"])
def home():
    return {
        "message": "Bienvenue sur Machine Learning API",
        "version": app.version
    }


@app.get("/health", tags=["Health"])
def health():
    return {"status": "ok"}