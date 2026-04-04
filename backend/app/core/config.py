import os

class Settings:
    SECRET_KEY: str = os.environ["SGE_SECRET_KEY"]  # sin default — falla si no está definida
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8 # 8 days

settings = Settings()
