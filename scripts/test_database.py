from sqlalchemy import text

from app.database.connection import engine


def main():
    with engine.connect() as connection:
        result = connection.execute(
            text("SELECT current_database(), current_user, version()")
        )

        row = result.fetchone()

        print("Connexion PostgreSQL : OK")
        print("Base de données :", row[0])
        print("Utilisateur :", row[1])
        print("Version :", row[2].split(",")[0])


if __name__ == "__main__":
    main()