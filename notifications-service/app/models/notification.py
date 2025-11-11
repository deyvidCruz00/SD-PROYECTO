from sqlalchemy import Column, String, DateTime, Boolean, Integer, Text
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()


class Notification(Base):
    """Modelo de notificación"""
    __tablename__ = "notifications"
    
    id = Column(String(36), primary_key=True, index=True)
    user_id = Column(String(36), index=True, nullable=False)
    type = Column(String(50), nullable=False)  # project_invitation, task_assigned, etc.
    title = Column(String(255), nullable=False)
    message = Column(Text, nullable=False)
    is_read = Column(Boolean, default=False, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    related_project_id = Column(String(36), nullable=True, index=True)
    related_user_id = Column(String(36), nullable=True)
    related_task_id = Column(String(36), nullable=True)
