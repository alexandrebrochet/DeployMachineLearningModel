from app.database.connection import engine
from app.database.models import Base


def main():
    Base.metadata.create_all(bind=engine)
    print("Tables PostgreSQL créées avec succès.")


if __name__ == "__main__":
    main()