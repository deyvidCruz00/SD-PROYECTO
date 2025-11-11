from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Optional


class EmailRequest(BaseModel):
    """Schema para solicitar envío de email"""
    to_email: EmailStr = Field(..., description="Email destinatario")
    to_name: Optional[str] = None
    subject: str = Field(..., description="Asunto del email")
    body: str = Field(..., description="Cuerpo del email")
    template_name: Optional[str] = None  # Nombre de la plantilla si se usa
    template_data: Optional[dict] = None  # Datos para la plantilla
    event_type: Optional[str] = None
    related_user_id: Optional[str] = None
    related_project_id: Optional[str] = None


class EmailResponse(BaseModel):
    """Schema de respuesta de email"""
    id: str
    to_email: str
    to_name: Optional[str]
    subject: str
    status: str
    created_at: datetime
    sent_at: Optional[datetime]
    error_message: Optional[str]
    
    class Config:
        from_attributes = True


class KafkaEmailEvent(BaseModel):
    """Schema para eventos de Kafka"""
    event_type: str
    to_email: str
    to_name: Optional[str] = None
    subject: str
    body: str
    template_name: Optional[str] = None
    template_data: Optional[dict] = None
    timestamp: datetime
    related_user_id: Optional[str] = None
    related_project_id: Optional[str] = None


class EmailStats(BaseModel):
    """Estadísticas de emails"""
    total_sent: int
    total_failed: int
    total_pending: int
