from sqlalchemy import Column, String, DateTime, Boolean, Text, Integer
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()


class EmailLog(Base):
    """Modelo para registro de emails enviados"""
    __tablename__ = "email_logs"
    
    id = Column(String(36), primary_key=True, index=True)
    to_email = Column(String(255), nullable=False, index=True)
    to_name = Column(String(255), nullable=True)
    subject = Column(String(255), nullable=False)
    body = Column(Text, nullable=False)
    status = Column(String(20), default="pending")  # pending, sent, failed
    error_message = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    sent_at = Column(DateTime, nullable=True)
    event_type = Column(String(50), nullable=True)  # registration, project_invitation, etc.
    related_user_id = Column(String(36), nullable=True, index=True)
    related_project_id = Column(String(36), nullable=True)
