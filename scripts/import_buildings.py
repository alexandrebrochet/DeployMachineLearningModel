
import csv
from pathlib import Path

from sqlalchemy import select, func, text

from app.database.connection import SessionLocal
from app.database.models import Building


# Base PostgreSQL autorisée pour l'importation
EXPECTED_DATABASE = "building_energy_db"

# Chemin du fichier CSV
CSV_PATH = (
    Path(__file__).resolve().parents[1]
    / "data"
    / "2016_Building_Energy_Benchmarking_2.csv"
)


def clean_value(value):
    """Convertit les valeurs vides en None."""
    if value is None:
        return None

    value = value.strip()

    return value if value else None


def optional_int(value):
    """Convertit une valeur facultative en entier."""
    value = clean_value(value)
    return int(value) if value is not None else None


def main():

    if not CSV_PATH.is_file():
        raise FileNotFoundError(
            f"Fichier CSV introuvable : {CSV_PATH}"
        )

    inserted = 0
    updated = 0

    with SessionLocal() as db:
        try:

            # Vérification de la base AVANT toute modification
            database_name = db.execute(
                text("SELECT current_database()")
            ).scalar_one()

            if database_name != EXPECTED_DATABASE:
                raise RuntimeError(
                    "Importation interdite : "
                    f"base '{database_name}' incorrecte. "
                    f"Base attendue : '{EXPECTED_DATABASE}'."
                )

            print(f"Base PostgreSQL vérifiée : {database_name}")

            with open(
                CSV_PATH,
                "r",
                encoding="utf-8-sig",
                newline=""
            ) as file:

                reader = csv.DictReader(file)

                required_columns = {
                    "OSEBuildingID",
                    "DataYear",
                    "PropertyName",
                    "YearBuilt",
                }

                if not required_columns.issubset(
                    set(reader.fieldnames or [])
                ):
                    raise ValueError(
                        "Le fichier CSV ne contient pas "
                        "toutes les colonnes obligatoires."
                    )

                for row in reader:

                    raw_data = {
                        key: clean_value(value)
                        for key, value in row.items()
                    }

                    ose_id = int(row["OSEBuildingID"])
                    data_year = int(row["DataYear"])

                    building = db.scalar(
                        select(Building).where(
                            Building.ose_building_id == ose_id,
                            Building.data_year == data_year,
                        )
                    )

                    year_built = optional_int(
                        row["YearBuilt"]
                    )

                    property_name = clean_value(
                        row["PropertyName"]
                    )

                    if building is None:

                        building = Building(
                            ose_building_id=ose_id,
                            data_year=data_year,
                            property_name=property_name,
                            year_built=year_built,
                            raw_data=raw_data,
                        )

                        db.add(building)
                        inserted += 1

                    else:

                        building.property_name = property_name
                        building.year_built = year_built
                        building.raw_data = raw_data

                        updated += 1

            # Validation de toutes les modifications
            db.commit()

            # Vérification du nombre total de bâtiments
            total = db.scalar(
                select(func.count()).select_from(Building)
            )

            print("\nImportation terminée.")
            print(f"Bâtiments insérés : {inserted}")
            print(f"Bâtiments mis à jour : {updated}")
            print(f"Total en base : {total}")

        except Exception:

            db.rollback()
            raise


if __name__ == "__main__":
    main()
