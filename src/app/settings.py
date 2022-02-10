from pathlib import Path

from pydantic import BaseSettings

base_dir: Path = Path(__file__).parent.parent


class Settings(BaseSettings):
    base_dir: Path = base_dir

    postgres_host: str
    postgres_port: int
    postgres_user: str
    postgres_password: str
    postgres_db: str
    db_url: str = None

    debug: bool
    app_host: str
    app_port: int

    username_min_len: int
    username_max_len: int

    password_min_len: int
    password_max_len: int


settings = Settings(_env_file=base_dir / ".env")

# fixme
if settings.db_url is None:
    settings.db_url = f"postgresql://{settings.postgres_user}" \
                      f":{settings.postgres_password}" \
                      f"@{settings.postgres_host}" \
                      f":{settings.postgres_port}" \
                      f"/{settings.postgres_db}"
