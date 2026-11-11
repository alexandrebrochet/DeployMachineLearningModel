# Building Energy Prediction API

API REST de prédiction de la consommation énergétique des bâtiments, développée avec FastAPI, Scikit-learn et PostgreSQL dans le cadre du projet OpenClassrooms **Déployer un modèle de Machine Learning**.

## 1. Présentation

L'application permet d'estimer la consommation énergétique d'un bâtiment à partir de quatre caractéristiques :

- Âge du bâtiment
- Type principal de propriété
- Nombre de bâtiments
- Surface totale

Le modèle de Machine Learning retourne une estimation de consommation énergétique en kBtu.

Les paramètres des prédictions et leurs résultats sont enregistrés dans PostgreSQL.

## 2. Technologies utilisées

| Technologie | Utilisation |
|---|---|
| Python 3.13 | Langage de programmation |
| FastAPI | API REST |
| Pydantic | Validation des données |
| Scikit-learn | Modèle de Machine Learning |
| Joblib | Chargement du modèle |
| PostgreSQL 18 | Base de données |
| SQLAlchemy | ORM et transactions |
| Pytest | Tests automatisés |
| GitHub Actions | Intégration continue |
| Git | Gestion des versions |

## 3. Architecture

L'application est organisée en plusieurs composants :

- `app/main.py` : initialisation de FastAPI.
- `app/api/predict.py` : endpoint de prédiction.
- `app/models/schemas.py` : schémas Pydantic.
- `app/services/prediction_service.py` : chargement et exécution du modèle ML.
- `app/database/connection.py` : connexion PostgreSQL.
- `app/database/models.py` : modèles SQLAlchemy.

Les diagrammes UML et la description détaillée de l'architecture sont disponibles dans `documents/architecture.md`.

## 4. Installation

### Prérequis

- Python 3.13
- PostgreSQL 18
- Git

### Cloner le dépôt

```bash
git clone https://github.com/alexandrebrochet/DeployMachineLearningModel.git
cd DeployMachineLearningModel
```

### Créer un environnement virtuel

Sous Windows :

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Sous Linux :

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### Installer les dépendances

```bash
python -m pip install -r requirements.txt
```

## 5. Configuration PostgreSQL

Créer une base PostgreSQL et un utilisateur disposant des droits nécessaires.

Créer ensuite un fichier `.env` à la racine du projet :

```dotenv
DB_HOST=localhost
DB_PORT=5432
DB_NAME=building_energy_db
DB_USER=building_energy_user
DB_PASSWORD=remplacer_par_un_mot_de_passe
```

Le fichier `.env` doit rester local et ne doit jamais être ajouté au dépôt Git.

Les tables applicatives sont définies dans `app/database/models.py`.

Pour initialiser les tables :

```bash
python -c "from app.database.models import Base; from app.database.connection import engine; Base.metadata.create_all(bind=engine)"
```

La table `buildings` peut ensuite être alimentée avec le jeu de données du projet. Le script d'import et la disponibilité des données doivent être vérifiés avant une installation complète.

## 6. Démarrer l'API

```bash
uvicorn app.main:app --reload
```

L'API est accessible localement :

- Documentation Swagger : http://127.0.0.1:8000/docs
- Documentation OpenAPI : http://127.0.0.1:8000/openapi.json
- Santé de l'application : http://127.0.0.1:8000/health

## 7. Exemple de prédiction

Endpoint :

`POST /predict`

Corps JSON :

```json
{
  "BuildingAge": 25,
  "PrimaryPropertyType": "Large Office",
  "NumberofBuildings": 1,
  "PropertyGFATotal": 120000
}
```

Exemple de réponse :

```json
{
  "predicted_energy_consumption": 7055555.49,
  "unit": "kBtu"
}
```

La valeur dépend de la version du modèle utilisé.

## 8. Base de données

L'application utilise trois tables principales.

**buildings** : caractéristiques des bâtiments du jeu de données.

**prediction_inputs** : paramètres fournis lors des prédictions.

**prediction_outputs** : résultats du modèle, associés aux entrées.

Les entrées et les résultats sont enregistrés dans une transaction PostgreSQL.

## 9. Tests automatisés

Les tests sont développés avec Pytest.

Les tests unitaires vérifient les endpoints, la validation des données et la gestion des erreurs.

Les tests d'intégration vérifient les opérations SQLAlchemy sur une base PostgreSQL dédiée.

Commande :

```bash
python -m pytest -v --cov=app --cov-report=term-missing --cov-fail-under=85
```

La couverture locale mesurée lors de la validation est de **96,40 %**.

Les tests d'intégration nécessitent une base `building_energy_test` accessible avec les identifiants configurés.

## 10. Intégration continue

Le workflow `.github/workflows/ci.yml` est exécuté lors des pushs et des Pull Requests vers les branches configurées.

Il réalise les opérations suivantes :

1. Récupération du dépôt.
2. Installation de Python 3.13.
3. Installation des dépendances.
4. Démarrage de PostgreSQL 18 dans un conteneur temporaire.
5. Création des tables SQLAlchemy.
6. Exécution des tests Pytest.
7. Vérification d'une couverture minimale de 85 %.

## 11. Gestion des erreurs

| Situation | Code HTTP |
|---|---|
| Prédiction réussie | 200 |
| Données invalides | 422 |
| Erreur PostgreSQL | 503 |
| Erreur du modèle ML | 500 |

## 12. État du projet

Le projet comprend une API fonctionnelle, un modèle ML chargé avec Joblib, une base PostgreSQL locale, des tests automatisés et une CI GitHub Actions.

Le déploiement sur un serveur distant n'est pas inclus dans l'environnement actuel.

## 13. Documentation

Voir `documents/architecture.md` pour les diagrammes UML de classes et de séquence.