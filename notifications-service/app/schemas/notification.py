from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class NotificationCreate(BaseModel):
    """Schema para crear una notificación"""
    user_id: str = Field(..., description="ID del usuario que recibe la notificación")
    type: str = Field(..., description="Tipo de notificación")
    title: str = Field(..., description="Título de la notificación")
    message: str = Field(..., description="Mensaje de la notificación")
    related_project_id: Optional[str] = None
    related_user_id: Optional[str] = None
    related_task_id: Optional[str] = None


class NotificationResponse(BaseModel):
    """Schema de respuesta de notificación"""
    id: str
    user_id: str
    type: str
    title: str
    message: str
    is_read: bool
    created_at: datetime
    updated_at: datetime
    related_project_id: Optional[str] = None
    related_user_id: Optional[str] = None
    related_task_id: Optional[str] = None
    
    class Config:
        from_attributes = True


class KafkaNotificationEvent(BaseModel):
    """Schema para eventos de Kafka"""
    event_type: str
    user_id: str
    notification_type: str
    title: str
    message: str
    timestamp: datetime
    related_project_id: Optional[str] = None
    related_user_id: Optional[str] = None
    related_task_id: Optional[str] = None
