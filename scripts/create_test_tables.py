
import os
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy import create_engine, text, URL

from app.database.models import Base


load_dotenv(Path(__file__).resolve().parents[1] / ".env")

TEST_DB_NAME = "building_energy_test"

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
        current_database = connection.execute(
            text("SELECT current_database()")
        ).scalar_one()

        if current_database != TEST_DB_NAME:
            raise RuntimeError(
                "Sécurité : base PostgreSQL incorrecte"
            )

    # Création uniquement des tables manquantes
    Base.metadata.create_all(bind=engine)

    print("Tables de test créées avec succès.")

    with engine.connect() as connection:
        tables = connection.execute(
            text("""
                SELECT tablename
                FROM pg_tables
                WHERE schemaname = 'public'
                ORDER BY tablename
            """)
        ).scalars().all()

        for table in tables:
            print(f"- {table}")

finally:
    engine.dispose()
