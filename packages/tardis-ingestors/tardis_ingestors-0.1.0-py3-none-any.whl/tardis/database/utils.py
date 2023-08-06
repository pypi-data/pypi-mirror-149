import os


def try_load_dotenv():
    try:
        from dotenv import load_dotenv

        load_dotenv()
    finally:
        pass


def get_db_credentials() -> dict[str, str]:
    try_load_dotenv()
    return {
        "user": os.getenv("PSQL_USER"),
        "password": os.getenv("PSQL_PASSWORD"),
        "host": os.getenv("PSQL_HOST"),
        "port": os.getenv("PSQL_PORT"),
        "database": os.getenv("PSQL_DATABASE"),
    }
