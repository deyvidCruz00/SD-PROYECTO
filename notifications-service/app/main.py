from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging
from app.config import settings
from app.routes import notification
from app.kafka.producer import KafkaConsumerService
import threading

# Configurar logging
logging.basicConfig(level=settings.LOG_LEVEL)
logger = logging.getLogger(__name__)

# Crear aplicación FastAPI
app = FastAPI(
    title="Notifications Service",
    description="Servicio de notificaciones para el sistema de proyectos colaborativos",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir rutas
app.include_router(notification.router)


# Variables globales para Kafka
kafka_consumer = None
kafka_consumer_thread = None


def start_kafka_consumer():
    """Inicia el consumidor de Kafka en un hilo separado"""
    global kafka_consumer, kafka_consumer_thread
    
    try:
        from app.services.notification_service import NotificationService
        
        notification_service = NotificationService()
        kafka_consumer = KafkaConsumerService(
            topic=settings.KAFKA_NOTIFICATION_TOPIC,
            group_id="notifications-service-group"
        )
        
        def process_message(message):
            logger.info(f"Procesando mensaje de Kafka: {message}")
            notification_service.process_kafka_event(message)
        
        kafka_consumer_thread = threading.Thread(
            target=kafka_consumer.start,
            args=(process_message,),
            daemon=True
        )
        kafka_consumer_thread.start()
        logger.info("Consumidor de Kafka iniciado")
    except Exception as e:
        logger.error(f"Error al iniciar consumidor de Kafka: {str(e)}")


@app.on_event("startup")
async def startup_event():
    """Evento al iniciar la aplicación"""
    logger.info(f"Iniciando {settings.SERVICE_NAME}...")
    start_kafka_consumer()


@app.on_event("shutdown")
async def shutdown_event():
    """Evento al cerrar la aplicación"""
    logger.info(f"Cerrando {settings.SERVICE_NAME}...")
    if kafka_consumer:
        kafka_consumer.close()


@app.get("/", tags=["info"])
async def read_root():
    """Endpoint raíz"""
    return {
        "service": settings.SERVICE_NAME,
        "version": "1.0.0",
        "status": "running"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=settings.SERVICE_PORT)
