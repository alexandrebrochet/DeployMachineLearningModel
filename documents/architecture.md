
# Architecture du projet

## Diagramme de classes UML

```mermaid
classDiagram
    class Building {
        +int id
        +int ose_building_id
        +int data_year
        +str property_name
        +int year_built
        +JSONB raw_data
    }

    class PredictionInput {
        +int id
        +int building_id
        +int building_age
        +str primary_property_type
        +int number_of_buildings
        +float property_gfa_total
        +datetime created_at
    }

    class PredictionOutput {
        +int id
        +int prediction_input_id
        +float predicted_energy_consumption
        +str model_version
        +datetime created_at
    }

    Building "0..1" --> "0..*" PredictionInput : building_id
    PredictionInput "1" --> "0..1" PredictionOutput : prediction_input_id
```

## Description des composants

### API FastAPI

L'API expose les routes `/`, `/health` et `/predict`.

La route `/predict` valide les données avec Pydantic,
enregistre les paramètres dans PostgreSQL, exécute
le modèle de prédiction et enregistre le résultat.

### Modèle Machine Learning

Le modèle Scikit-learn est chargé depuis un fichier
Joblib par le service de prédiction.

### Base de données PostgreSQL

La base contient trois tables principales :

- `buildings` : données des bâtiments.
- `prediction_inputs` : paramètres des prédictions.
- `prediction_outputs` : résultats des prédictions.

SQLAlchemy assure la correspondance entre les classes
Python et les tables PostgreSQL.

### Tests automatisés

Pytest vérifie les routes, la validation des données,
la gestion des erreurs et les opérations PostgreSQL.

GitHub Actions exécute les tests unitaires et
d'intégration avec une base PostgreSQL temporaire.
Le seuil minimal de couverture est fixé à 85 %.


## Diagramme de séquence — Prédiction énergétique

```mermaid
sequenceDiagram
    autonumber
    actor Client
    participant API as FastAPI
    participant DB as PostgreSQL
    participant ML as Service ML

    Client->>API: POST /predict (JSON)
    API->>API: Validation Pydantic
    API->>DB: INSERT prediction_inputs
    DB-->>API: ID de la prédiction
    API->>ML: predict_energy(données)
    ML-->>API: Consommation estimée
    API->>DB: INSERT prediction_outputs
    API->>DB: COMMIT
    DB-->>API: Transaction validée
    API-->>Client: HTTP 200 + résultat (kBtu)
```

### Gestion des erreurs

- Données invalides : HTTP 422.
- Erreur PostgreSQL : rollback et HTTP 503.
- Erreur du modèle ML : rollback et HTTP 500.

Les entrées et les résultats sont enregistrés
dans une même transaction PostgreSQL.