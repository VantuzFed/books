from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    PROJECT_NAME: str = "Books API"
    DEBUG: bool = True

    # MariaDB connection settings
    DB_HOST: str = "localhost"
    DB_PORT: int = 3306
    DB_USER: str = "books_user"
    DB_PASSWORD: str = "books_password"
    DB_NAME: str = "books_db"

    @property
    def database_url(self) -> str:
        return (
            f"mysql+aiomysql://{self.DB_USER}:{self.DB_PASSWORD}"
            f"@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}?charset=utf8mb4"
        )

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()
