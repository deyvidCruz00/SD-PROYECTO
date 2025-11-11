from kafka import KafkaConsumer
from kafka import KafkaProducer
import json
import logging
from app.config import settings

logger = logging.getLogger(__name__)


class KafkaProducerService:
    """Servicio para producir mensajes en Kafka"""
    
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        if not self._initialized:
            self.producer = KafkaProducer(
                bootstrap_servers=[settings.KAFKA_BROKER],
                value_serializer=lambda v: json.dumps(v).encode('utf-8'),
                acks='all',
                retries=3
            )
            self._initialized = True
    
    def send_message(self, topic: str, message: dict):
        """Envía un mensaje a un tema de Kafka"""
        try:
            future = self.producer.send(topic, value=message)
            future.get(timeout=10)
            logger.info(f"Mensaje enviado a {topic}: {message}")
        except Exception as e:
            logger.error(f"Error al enviar mensaje a {topic}: {str(e)}")
            raise
    
    def close(self):
        """Cierra la conexión del productor"""
        if self.producer:
            self.producer.close()


class KafkaConsumerService:
    """Servicio para consumir mensajes de Kafka"""
    
    def __init__(self, topic: str, group_id: str):
        self.topic = topic
        self.group_id = group_id
        self.consumer = None
    
    def start(self, callback):
        """Inicia el consumidor y procesa mensajes"""
        self.consumer = KafkaConsumer(
            self.topic,
            bootstrap_servers=[settings.KAFKA_BROKER],
            group_id=self.group_id,
            value_deserializer=lambda m: json.loads(m.decode('utf-8')),
            auto_offset_reset='earliest',
            enable_auto_commit=True
        )
        
        logger.info(f"Iniciado consumidor Kafka para topic: {self.topic}")
        
        try:
            for message in self.consumer:
                try:
                    callback(message.value)
                except Exception as e:
                    logger.error(f"Error procesando mensaje: {str(e)}")
        except KeyboardInterrupt:
            logger.info("Consumidor de Kafka detenido")
        finally:
            self.consumer.close()
    
    def close(self):
        """Cierra la conexión del consumidor"""
        if self.consumer:
            self.consumer.close()
