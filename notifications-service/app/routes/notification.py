from fastapi import APIRouter, Depends, Query, HTTPException
from typing import List
from app.schemas.notification import NotificationResponse, NotificationCreate
from app.services.notification_service import NotificationService

router = APIRouter(prefix="/api/v1/notifications", tags=["notifications"])

# Instancia del servicio
notification_service = NotificationService()


@router.get("", response_model=List[NotificationResponse])
async def get_notifications(
    user_id: str = Query(..., description="ID del usuario"),
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100)
):
    """Obtiene las notificaciones de un usuario con paginación"""
    return notification_service.get_user_notifications(user_id, skip, limit)


@router.get("/unread/count")
async def get_unread_count(user_id: str = Query(..., description="ID del usuario")):
    """Obtiene el conteo de notificaciones no leídas"""
    return {
        "user_id": user_id,
        "unread_count": notification_service.get_unread_count(user_id)
    }


@router.post("", response_model=NotificationResponse)
async def create_notification(notification: NotificationCreate):
    """Crea una nueva notificación"""
    return notification_service.create_notification(notification)


@router.put("/{notification_id}/read", response_model=NotificationResponse)
async def mark_as_read(notification_id: str):
    """Marca una notificación como leída"""
    result = notification_service.mark_as_read(notification_id)
    if not result:
        raise HTTPException(status_code=404, detail="Notificación no encontrada")
    return result


@router.put("/user/{user_id}/read-all")
async def mark_all_as_read(user_id: str):
    """Marca todas las notificaciones de un usuario como leídas"""
    count = notification_service.mark_all_as_read(user_id)
    return {"user_id": user_id, "marked_as_read": count}


@router.delete("/{notification_id}")
async def delete_notification(notification_id: str):
    """Elimina una notificación"""
    if not notification_service.delete_notification(notification_id):
        raise HTTPException(status_code=404, detail="Notificación no encontrada")
    return {"message": "Notificación eliminada"}


@router.get("/health", tags=["health"])
async def health_check():
    """Verificación de salud del servicio"""
    return {
        "status": "healthy",
        "service": "notifications-service"
    }
