class Settings:
    SECRET_KEY: str = "SuperSecretKeyForSGE2026!"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8 # 8 days

settings = Settings()
