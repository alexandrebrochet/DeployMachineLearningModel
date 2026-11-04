# Déployez votre modèle de Machine Learning

## Présentation

Ce projet a pour objectif de développer et de déployer une API REST permettant d'exposer un modèle de Machine Learning.

Il est réalisé dans le cadre du parcours OpenClassrooms et vise à appliquer les bonnes pratiques de développement, de versionnage, de tests automatisés, de gestion des données et de déploiement.

Le cas d'utilisation concerne **la prédiction de la consommation énergétique des bâtiments de Seattle** à partir de leurs caractéristiques.

Le modèle est entraîné en amont, exporté avec Joblib, puis intégré à une application FastAPI.

## Technologies

- Python 3.13
- FastAPI et Pydantic
- Pandas, Scikit-learn et Joblib
- Pytest et pytest-cov
- PostgreSQL et SQLAlchemy (à intégrer)
- Git et GitHub
- GitHub Actions pour l'intégration continue

## Architecture du projet

```text
app/
  api/                 Endpoints REST
  models/              Modèle ML et schémas Pydantic
  services/            Logique de prédiction
  database/            Accès à PostgreSQL (prévu)
tests/                 Tests automatisés
scripts/               Scripts utilitaires
sql/                   Scripts SQL (prévus)
docs/                  Documentation
.github/
  workflows/
    ci.yml             Pipeline d'intégration continue
requirements.txt       Dépendances Python
README.md              Documentation du projet
```

## Installation

### 1. Cloner le dépôt

```bash
git clone https://github.com/alexandrebrochet/DeployMachineLearningModel.git
cd DeployMachineLearningModel
```

### 2. Créer un environnement virtuel

```bash
python -m venv .venv
```

Activation sous Windows PowerShell :

```powershell
.\.venv\Scripts\Activate.ps1
```

Activation sous Windows avec Git Bash :

```bash
source .venv/Scripts/activate
```

### 3. Installer les dépendances

```bash
python -m pip install -r requirements.txt
```

### 4. Configuration

Le projet prévoit l'utilisation de variables d'environnement pour les paramètres de configuration et les accès aux services externes.

Lorsque le fichier `.env.example` est disponible, le copier vers `.env` et adapter les paramètres à son environnement.

Ne jamais publier le fichier `.env` contenant des secrets.

## Modèle de Machine Learning

Le modèle prédit la consommation énergétique d'un bâtiment, exprimée en **kBtu**.

Il utilise quatre variables :

| Variable | Description |
|---|---|
| `BuildingAge` | Âge du bâtiment |
| `PrimaryPropertyType` | Type principal de bâtiment |
| `NumberofBuildings` | Nombre de bâtiments |
| `PropertyGFATotal` | Surface totale du bâtiment |

Le modèle est un pipeline Scikit-learn comprenant un prétraitement des variables et une régression linéaire.

Il est enregistré au format Joblib dans :

```text
app/models/building_energy_model.joblib
```

## API REST

L'application est développée avec FastAPI.

### Démarrer l'API

```bash
uvicorn app.main:app --reload
```

L'API est accessible localement à l'adresse :

`http://127.0.0.1:8000`

La documentation interactive Swagger est disponible sur :

`http://127.0.0.1:8000/docs`

### Endpoints disponibles

| Méthode | Endpoint | Description |
|---|---|---|
| GET | `/` | Informations générales sur l'API |
| GET | `/health` | Vérification de disponibilité |
| POST | `/predict` | Prédiction de consommation énergétique |

### Exemple de prédiction

Requête `POST /predict` :

```json
{
  "BuildingAge": 25,
  "PrimaryPropertyType": "Large Office",
  "NumberofBuildings": 1,
  "PropertyGFATotal": 120000
}
```

La réponse contient la consommation énergétique prédite ainsi que son unité :

```json
{
  "predicted_energy_consumption": 123456.78,
  "unit": "kBtu"
}
```

La valeur numérique ci-dessus est illustrative.

Les données entrantes sont validées avec Pydantic avant d'être transmises au modèle.

## Tests automatisés

Les tests sont développés avec Pytest.

Ils vérifient notamment :

- Le bon fonctionnement des prédictions.
- La validation des données d'entrée.
- Le rejet des valeurs invalides.
- Le comportement de l'API en cas d'erreur.
- La disponibilité des endpoints généraux.

### Exécuter les tests

```bash
python -m pytest -v
```

### Mesurer la couverture

```bash
python -m pytest -v --cov=app --cov-report=term-missing --cov-fail-under=85
```

Le seuil minimal de couverture est fixé à **85 %**.

Lors de la validation locale de l'étape CI, une couverture de **100 %** a été obtenue.

## Intégration continue avec GitHub Actions

L'intégration continue est configurée dans :

```text
.github/workflows/ci.yml
```

Le workflow est déclenché automatiquement lors :

- D'un `push` sur `main`.
- D'un `push` sur une branche `feature/**`.
- D'une Pull Request vers `main`.

### Étapes du workflow

1. Récupération du code source.
2. Installation de Python 3.13 sur un runner Ubuntu.
3. Installation des dépendances.
4. Exécution des tests Pytest.
5. Vérification du seuil minimal de couverture de 85 %.

Les tests sont exécutés sur l'infrastructure GitHub, sans déploiement sur un serveur de production.

### Protection de la branche principale

La branche `main` est protégée par une règle GitHub.

Les modifications doivent passer par une Pull Request et satisfaire le contrôle obligatoire `Tests Python`.

Les suppressions de branche et les push forcés sont également interdits par la règle configurée.

## Environnements

| Environnement | Utilisation | État |
|---|---|---|
| Développement | Développement local avec Python et FastAPI | Opérationnel |
| Test | Exécution automatisée des tests sur GitHub Actions | Opérationnel |
| Production | Hébergement de l'API et connexion à PostgreSQL | À mettre en place |

Les environnements de développement et de test sont séparés.

Le déploiement en production sera configuré dans une étape ultérieure.

## Gestion des secrets

Les informations sensibles ne doivent pas être enregistrées dans le dépôt Git.

Les bonnes pratiques retenues sont :

- Utiliser des variables d'environnement.
- Exclure les fichiers `.env` du versionnage.
- Utiliser GitHub Secrets pour les identifiants nécessaires aux workflows.
- Séparer les paramètres de développement, de test et de production.
- Ne jamais écrire de mots de passe dans le code source ou les journaux.

La configuration des secrets PostgreSQL et de production sera effectuée lors de l'intégration de ces services.

## Standards de développement

### Gestion des branches

Les nouvelles fonctionnalités sont développées sur des branches dédiées.

Exemples :

```text
main
feature/ml-prediction
feature/github-actions
docs/ci-cd
```

Les modifications sont intégrées à `main` au moyen de Pull Requests.

### Conventions de commits

Les messages de commit doivent décrire clairement les modifications.

Exemples :

```text
feat: add prediction endpoint
test: add API validation tests
fix: correct model loading
ci: configure automated tests
docs: update project documentation
```

### Qualité du code

Les règles retenues sont :

- Séparer les endpoints, les schémas et la logique métier.
- Valider les entrées de l'API.
- Écrire des tests pour les fonctionnalités ajoutées.
- Maintenir une couverture minimale de 85 %.
- Vérifier les contrôles GitHub Actions avant fusion.
- Éviter de stocker des informations sensibles dans Git.

## Suivi des expériences de Machine Learning

Le modèle utilisé par l'API provient d'une phase préalable d'entraînement et d'évaluation.

Pour assurer la reproductibilité des expériences, les informations suivantes doivent être documentées :

- Source et version du jeu de données.
- Variables utilisées pour l'entraînement.
- Prétraitements appliqués.
- Algorithmes évalués.
- Paramètres d'entraînement.
- Métriques de performance.
- Version des bibliothèques.
- Version du modèle exporté.

Le modèle actuellement intégré utilise une régression linéaire avec prétraitement Scikit-learn.

Les métriques détaillées de l'expérience initiale devront être reportées depuis le notebook d'entraînement, sans inventer de résultats.

## Fonctionnalités réalisées

- Export et intégration du modèle ML.
- API REST FastAPI.
- Validation des entrées avec Pydantic.
- Endpoint de prédiction.
- Tests automatisés.
- Mesure de couverture.
- Intégration continue avec GitHub Actions.
- Protection de la branche `main`.

## Fonctionnalités à développer

- Base de données PostgreSQL.
- Modèles relationnels avec SQLAlchemy.
- Importation du jeu de données complet.
- Enregistrement des entrées et sorties des prédictions.
- Traçabilité des prédictions.
- Tests d'intégration avec PostgreSQL.
- Configuration de l'environnement de production.
- Déploiement de l'API.