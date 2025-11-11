import logging
import uuid
from datetime import datetime
from typing import List, Optional
from app.models.notification import Notification
from app.schemas.notification import NotificationCreate, NotificationResponse, KafkaNotificationEvent

logger = logging.getLogger(__name__)


class NotificationService:
    """Servicio de negocio para notificaciones"""
    
    def __init__(self):
        # En una aplicación real, aquí usarías una base de datos
        self.notifications: dict = {}
    
    def create_notification(self, notification_create: NotificationCreate) -> NotificationResponse:
        """Crea una nueva notificación"""
        notification_id = str(uuid.uuid4())
        
        notification = {
            "id": notification_id,
            "user_id": notification_create.user_id,
            "type": notification_create.type,
            "title": notification_create.title,
            "message": notification_create.message,
            "is_read": False,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow(),
            "related_project_id": notification_create.related_project_id,
            "related_user_id": notification_create.related_user_id,
            "related_task_id": notification_create.related_task_id
        }
        
        self.notifications[notification_id] = notification
        logger.info(f"Notificación creada: {notification_id}")
        
        return NotificationResponse(**notification)
    
    def get_user_notifications(self, user_id: str, skip: int = 0, limit: int = 10) -> List[NotificationResponse]:
        """Obtiene las notificaciones de un usuario"""
        user_notifications = [
            n for n in self.notifications.values() 
            if n["user_id"] == user_id
        ]
        return [
            NotificationResponse(**n) 
            for n in user_notifications[skip:skip + limit]
        ]
    
    def get_unread_count(self, user_id: str) -> int:
        """Obtiene el conteo de notificaciones no leídas"""
        return sum(
            1 for n in self.notifications.values()
            if n["user_id"] == user_id and not n["is_read"]
        )
    
    def mark_as_read(self, notification_id: str) -> Optional[NotificationResponse]:
        """Marca una notificación como leída"""
        if notification_id in self.notifications:
            self.notifications[notification_id]["is_read"] = True
            self.notifications[notification_id]["updated_at"] = datetime.utcnow()
            return NotificationResponse(**self.notifications[notification_id])
        return None
    
    def mark_all_as_read(self, user_id: str) -> int:
        """Marca todas las notificaciones de un usuario como leídas"""
        count = 0
        for notification in self.notifications.values():
            if notification["user_id"] == user_id and not notification["is_read"]:
                notification["is_read"] = True
                notification["updated_at"] = datetime.utcnow()
                count += 1
        return count
    
    def delete_notification(self, notification_id: str) -> bool:
        """Elimina una notificación"""
        if notification_id in self.notifications:
            del self.notifications[notification_id]
            logger.info(f"Notificación eliminada: {notification_id}")
            return True
        return False
    
    def process_kafka_event(self, event: dict) -> NotificationResponse:
        """Procesa un evento de Kafka y crea una notificación"""
        try:
            kafka_event = KafkaNotificationEvent(**event)
            
            notification_create = NotificationCreate(
                user_id=kafka_event.user_id,
                type=kafka_event.notification_type,
                title=kafka_event.title,
                message=kafka_event.message,
                related_project_id=kafka_event.related_project_id,
                related_user_id=kafka_event.related_user_id,
                related_task_id=kafka_event.related_task_id
            )
            
            return self.create_notification(notification_create)
        except Exception as e:
            logger.error(f"Error procesando evento de Kafka: {str(e)}")
            raise
