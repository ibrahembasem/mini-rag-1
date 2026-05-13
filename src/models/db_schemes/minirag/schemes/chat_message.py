from .minirag_base import SQLAlchemyBase
from sqlalchemy import Column, Integer, DateTime, func, String, Text, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy import Index
import uuid


class ChatMessage(SQLAlchemyBase):
    """
    جدول لتخزين رسائل المحادثة (الذاكرة الدائمة).
    كل رسالة مرتبطة بـ session_id (معرّف الجلسة).
    - في Streamlit: يكون session_id عبارة عن UUID عشوائي.
    - في واتساب: يكون session_id هو رقم هاتف المستخدم.
    """
    __tablename__ = "chat_messages"

    message_id = Column(Integer, primary_key=True, autoincrement=True)
    message_uuid = Column(UUID(as_uuid=True), default=uuid.uuid4, unique=True, nullable=False)

    # معرّف الجلسة: يربط الرسائل ببعضها (UUID للويب، رقم هاتف للواتساب)
    session_id = Column(String(100), nullable=False, index=True)

    # معرّف المشروع
    project_id = Column(Integer, ForeignKey("projects.project_id"), nullable=False)

    # دور المرسل: "user" أو "assistant"
    role = Column(String(20), nullable=False)

    # محتوى الرسالة
    content = Column(Text, nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # العلاقات
    project = relationship("Project", back_populates="chat_messages")

    __table_args__ = (
        Index('ix_chat_session_project', session_id, project_id),
    )
