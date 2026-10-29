from fastapi import FastAPI

app = FastAPI(
    title="Machine Learning API",
    description="API REST pour exposer un modèle de Machine Learning",
    version="0.2.0"
)


@app.get("/", tags=["General"])
def home():
    return {
        "message": "Bienvenue sur Machine Learning API",
        "version": app.version
    }


@app.get("/health", tags=["Health"])
def health():
    return {
        "status": "ok"
    }