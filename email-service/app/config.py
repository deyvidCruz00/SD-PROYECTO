from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Configuración de la aplicación"""
    SERVICE_PORT: int = 8003
    SERVICE_NAME: str = "email-service"
    
    # Kafka
    KAFKA_BROKER: str = "localhost:9092"
    KAFKA_EMAIL_TOPIC: str = "emails"
    
    # Database
    DATABASE_URL: Optional[str] = None
    
    # SMTP Configuration
    SMTP_HOST: str = "smtp.gmail.com"
    SMTP_PORT: int = 587
    SMTP_USER: str = ""
    SMTP_PASSWORD: str = ""
    SMTP_FROM_EMAIL: str = "noreply@colaboraapp.com"
    SMTP_FROM_NAME: str = "Colabora App"
    
    # Logging
    LOG_LEVEL: str = "INFO"
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
