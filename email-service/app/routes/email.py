from fastapi import APIRouter, HTTPException, Query
from typing import List
from app.schemas.email import EmailRequest, EmailResponse
from app.services.email_service import EmailService

router = APIRouter(prefix="/api/v1/emails", tags=["emails"])

# Instancia del servicio
email_service = EmailService()


@router.post("/send", response_model=EmailResponse)
async def send_email(email_request: EmailRequest):
    """Envía un email"""
    return await email_service.send_email(email_request)


@router.get("/logs", response_model=List[EmailResponse])
async def get_email_logs(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100)
):
    """Obtiene registros de emails enviados"""
    return email_service.get_email_logs(skip, limit)


@router.get("/logs/{email_id}", response_model=EmailResponse)
async def get_email_log(email_id: str):
    """Obtiene un registro específico de email"""
    result = email_service.get_email_log(email_id)
    if not result:
        raise HTTPException(status_code=404, detail="Email no encontrado")
    return result


@router.get("/stats")
async def get_email_stats():
    """Obtiene estadísticas de emails"""
    return email_service.get_email_stats()


@router.get("/health", tags=["health"])
async def health_check():
    """Verificación de salud del servicio"""
    return {
        "status": "healthy",
        "service": "email-service"
    }
