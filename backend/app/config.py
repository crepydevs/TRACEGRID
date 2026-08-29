from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str
    NEO4J_URI: str
    NEO4J_USER: str
    NEO4J_PASSWORD: str
    REDIS_URL: str
    TOR_SOCKS_PROXY: str = ""

    class Config:
        env_file = ".env"


settings = Settings()
