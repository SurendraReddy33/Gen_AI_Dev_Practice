
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    MONGO_URI: str = "mongodb+srv://surendrareddygandra3:onTwB6qFMES4HF24@genai-cluster.cb98ycb.mongodb.net/"
    MONGO_DB: str = "smart_parking_db"
    JWT_SECRET: str = "u7^X3!f9zA@2M@nQw4%tS8rP1L$dC6hB"
    JWT_ALG: str = "HS256"
    JWT_EXPIRES_MIN: int = 60 * 24  # 1 day
    SMTP_HOST: str = "localhost"
    SMTP_PORT: int = 1025
    SMTP_USER: str = "gsrgsreddy3@gmail.com"
    SMTP_PASS: str = "vejwwtmsyrbnorss"
    SMTP_FROM: str = "gsrgsreddy3@gmai.com"
    RESET_TOKEN_TTL_MIN: int = 30

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

settings = Settings()
