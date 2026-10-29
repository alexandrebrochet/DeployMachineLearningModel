# Déployez votre modèle de Machine Learning 

## Présentation

Ce projet a pour objectif de développer et de déployer une API REST permettant d'exposer un modèle de Machine Learning.

Il est réalisé dans le cadre du parcours OpenClassrooms et vise à appliquer les bonnes pratiques de développement, de versionnage, de tests automatisés et de déploiement.

## Technologies

- Python
- FastAPI
- Pytest et pytest-cov
- PostgreSQL
- Git et GitHub
- GitHub Actions (CI/CD)

## Architecture du projet

```text
app/                Code source de l'application
  api/              Endpoints REST
  models/           Modèles de Machine Learning
  services/         Logique métier
  database/         Accès à PostgreSQL
tests/              Tests automatisés
scripts/            Scripts utilitaires
sql/                Scripts SQL
docs/               Documentation
.github/workflows/  Pipelines CI/CD
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

Activation sous Windows avec Git Bash :

```bash
source .venv/Scripts/activate
```

### 3. Installer les dépendances

```bash
pip install -r requirements.txt
```

### 4. Configuration

Copier `.env.example` vers `.env` et adapter les paramètres à son environnement.

Ne jamais publier le fichier `.env` contenant des secrets.

## Fonctionnalités prévues

- Exposition d'un modèle ML