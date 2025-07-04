from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str
    ENVIRONMENT: str = "development"
    DOMAIN: str = "localhost"

    class Config:
        env_file = ".env"
        case_sensitive = True
        extra = "ignore"


settings = Settings(_env_file=".env")
