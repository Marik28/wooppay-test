from pathlib import Path

from pydantic import BaseSettings

base_dir: Path = Path(__file__).parent.parent


class Settings(BaseSettings):
    base_dir: Path = base_dir

    postgres_host: str = "localhost"
    postgres_port: int = 5432
    postgres_user: str = "postgres"
    postgres_password: str = "postgres"
    postgres_db: str = "wooppay_test"
    db_url: str = None


settings = Settings(_env_file=base_dir / ".env")

# fixme
if settings.db_url is None:
    settings.db_url = f"postgresql://{settings.postgres_user}" \
                      f":{settings.postgres_password}" \
                      f"@{settings.postgres_host}" \
                      f":{settings.postgres_port}" \
                      f"/{settings.postgres_db}"
