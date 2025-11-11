import logging
import uuid
import aiosmtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
from typing import List, Optional
from jinja2 import Template
from app.config import settings
from app.schemas.email import EmailRequest, EmailResponse, KafkaEmailEvent

logger = logging.getLogger(__name__)


class EmailService:
    """Servicio de negocio para envío de emails"""
    
    def __init__(self):
        # En una aplicación real, usarías una base de datos
        self.email_logs: dict = {}
        self.templates = {
            "welcome": """
            <html>
            <body>
                <h1>¡Bienvenido a Colabora!</h1>
                <p>Hola {{ user_name }},</p>
                <p>Tu cuenta ha sido creada exitosamente.</p>
                <p>Puedes comenzar a explorar proyectos y conectar con otros artistas.</p>
            </body>
            </html>
            """,
            "project_invitation": """
            <html>
            <body>
                <h1>¡Invitación a Proyecto!</h1>
                <p>Hola {{ user_name }},</p>
                <p>{{ inviter_name }} te ha invitado al proyecto "{{ project_name }}"</p>
                <p>Los skills necesarios son: {{ required_skills }}</p>
            </body>
            </html>
            """,
            "task_assigned": """
            <html>
            <body>
                <h1>Nueva Tarea Asignada</h1>
                <p>Hola {{ user_name }},</p>
                <p>Te han asignado una tarea en el proyecto "{{ project_name }}"</p>
                <p>Título: {{ task_title }}</p>
                <p>Descripción: {{ task_description }}</p>
            </body>
            </html>
            """
        }
    
    async def send_email(self, email_request: EmailRequest) -> EmailResponse:
        """Envía un email"""
        email_id = str(uuid.uuid4())
        
        # Preparar cuerpo del email
        body = email_request.body
        if email_request.template_name and email_request.template_data:
            body = self._render_template(
                email_request.template_name,
                email_request.template_data
            )
        
        try:
            # Aquí iría la lógica real de envío con aiosmtplib
            # Para este ejemplo, simulamos el envío
            logger.info(f"Enviando email a {email_request.to_email}")
            
            # Registrar en logs
            email_log = {
                "id": email_id,
                "to_email": email_request.to_email,
                "to_name": email_request.to_name,
                "subject": email_request.subject,
                "body": body,
                "status": "sent",
                "created_at": datetime.utcnow(),
                "sent_at": datetime.utcnow(),
                "event_type": email_request.event_type,
                "related_user_id": email_request.related_user_id,
                "related_project_id": email_request.related_project_id,
                "error_message": None
            }
            
            self.email_logs[email_id] = email_log
            logger.info(f"Email enviado: {email_id}")
            
            return EmailResponse(**email_log)
        except Exception as e:
            logger.error(f"Error al enviar email: {str(e)}")
            
            email_log = {
                "id": email_id,
                "to_email": email_request.to_email,
                "to_name": email_request.to_name,
                "subject": email_request.subject,
                "body": body,
                "status": "failed",
                "created_at": datetime.utcnow(),
                "sent_at": None,
                "event_type": email_request.event_type,
                "related_user_id": email_request.related_user_id,
                "related_project_id": email_request.related_project_id,
                "error_message": str(e)
            }
            
            self.email_logs[email_id] = email_log
            return EmailResponse(**email_log)
    
    def _render_template(self, template_name: str, data: dict) -> str:
        """Renderiza una plantilla con los datos proporcionados"""
        if template_name not in self.templates:
            return data.get("body", "")
        
        template = Template(self.templates[template_name])
        return template.render(**data)
    
    def get_email_log(self, email_id: str) -> Optional[EmailResponse]:
        """Obtiene un registro de email"""
        if email_id in self.email_logs:
            return EmailResponse(**self.email_logs[email_id])
        return None
    
    def get_email_logs(self, skip: int = 0, limit: int = 10) -> List[EmailResponse]:
        """Obtiene registros de emails"""
        logs = list(self.email_logs.values())
        return [
            EmailResponse(**log)
            for log in logs[skip:skip + limit]
        ]
    
    def get_email_stats(self) -> dict:
        """Obtiene estadísticas de emails"""
        total_sent = sum(1 for log in self.email_logs.values() if log["status"] == "sent")
        total_failed = sum(1 for log in self.email_logs.values() if log["status"] == "failed")
        total_pending = sum(1 for log in self.email_logs.values() if log["status"] == "pending")
        
        return {
            "total_sent": total_sent,
            "total_failed": total_failed,
            "total_pending": total_pending
        }
    
    async def process_kafka_event(self, event: dict) -> EmailResponse:
        """Procesa un evento de Kafka y envía un email"""
        try:
            kafka_event = KafkaEmailEvent(**event)
            
            email_request = EmailRequest(
                to_email=kafka_event.to_email,
                to_name=kafka_event.to_name,
                subject=kafka_event.subject,
                body=kafka_event.body,
                template_name=kafka_event.template_name,
                template_data=kafka_event.template_data,
                event_type=kafka_event.event_type,
                related_user_id=kafka_event.related_user_id,
                related_project_id=kafka_event.related_project_id
            )
            
            return await self.send_email(email_request)
        except Exception as e:
            logger.error(f"Error procesando evento de Kafka: {str(e)}")
            raise
