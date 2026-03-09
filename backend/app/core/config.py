class Settings:
    SECRET_KEY: str = "RiobambaEP_SGE_Contratacion_2026_Secreta!"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8 # 8 days

settings = Settings()
