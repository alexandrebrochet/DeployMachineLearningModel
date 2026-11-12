
import os
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy import create_engine, text, URL


# Charger les paramètres de connexion existants
load_dotenv(Path(__file__).resolve().parents[1] / ".env")

# Protection : imposer explicitement la base de test
TEST_DB_NAME = "building_energy_test"

if TEST_DB_NAME == os.getenv("DB_NAME"):
    print("Base de test configurée dans .env")
else:
    print("Connexion à une base de test distincte")


database_url = URL.create(
    drivername="postgresql+psycopg",
    username=os.environ["DB_USER"],
    password=os.environ["DB_PASSWORD"],
    host=os.getenv("DB_HOST", "localhost"),
    port=int(os.getenv("DB_PORT", "5432")),
    database=TEST_DB_NAME,
)

engine = create_engine(database_url, pool_pre_ping=True)

try:
    with engine.connect() as connection:
        database_name = connection.execute(
            text("SELECT current_database()")
        ).scalar_one()

        connected_user = connection.execute(
            text("SELECT current_user")
        ).scalar_one()

        if database_name != TEST_DB_NAME:
            raise RuntimeError(
                "Sécurité : connexion à une base inattendue"
            )

        print("Connexion PostgreSQL réussie")
        print(f"Base : {database_name}")
        print(f"Utilisateur : {connected_user}")

finally:
    engine.dispose()
