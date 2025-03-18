from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str

    class Config:
        env_file = ".env"
        case_sensitive = True
        extra = "ignore"


settings = Settings(_env_file=".env")
