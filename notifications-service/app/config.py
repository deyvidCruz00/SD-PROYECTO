from pydantic_settings import BaseSettings
from typing import Optional
import os


class Settings(BaseSettings):
    """Configuración de la aplicación"""
    SERVICE_PORT: int = int(os.getenv('PORT', '8002'))
    SERVICE_NAME: str = "notifications-service"
    
    # Kafka (disabled for Render deployment)
    KAFKA_ENABLED: bool = os.getenv('KAFKA_ENABLED', 'true').lower() == 'true'
    KAFKA_BROKER: str = "localhost:9092"
    KAFKA_NOTIFICATION_TOPIC: str = "notifications"
    
    # Database - PostgreSQL for Render
    DATABASE_URL: Optional[str] = os.getenv('DATABASE_URL')
    
    # Logging
    LOG_LEVEL: str = "INFO"
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
