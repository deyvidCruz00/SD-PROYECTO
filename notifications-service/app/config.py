from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Configuración de la aplicación"""
    SERVICE_PORT: int = 8002
    SERVICE_NAME: str = "notifications-service"
    
    # Kafka
    KAFKA_BROKER: str = "localhost:9092"
    KAFKA_NOTIFICATION_TOPIC: str = "notifications"
    
    # Database
    DATABASE_URL: Optional[str] = None
    
    # Logging
    LOG_LEVEL: str = "INFO"
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
