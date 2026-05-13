from .BaseDataModel import BaseDataModel
from .db_schemes import ChatMessage
from sqlalchemy.future import select
from sqlalchemy import func, desc


class ChatModel(BaseDataModel):
    """
    موديل للتعامل مع جدول chat_messages في قاعدة البيانات.
    يوفر عمليات: حفظ رسالة، جلب آخر N رسالة، مسح سجل محادثة.
    """

    def __init__(self, db_client: object):
        super().__init__(db_client=db_client)
        self.db_client = db_client

    @classmethod
    async def create_instance(cls, db_client: object):
        instance = cls(db_client)
        return instance

    async def add_message(self, session_id: str, project_id: int, role: str, content: str):
        """حفظ رسالة جديدة في قاعدة البيانات"""
        async with self.db_client() as session:
            async with session.begin():
                message = ChatMessage(
                    session_id=session_id,
                    project_id=project_id,
                    role=role,
                    content=content
                )
                session.add(message)
            await session.commit()
            await session.refresh(message)
        return message

    async def get_recent_messages(self, session_id: str, project_id: int, limit: int = 6):
        """
        جلب آخر N رسالة لجلسة ومشروع محددين.
        الترتيب: من الأقدم إلى الأحدث (لأن الموديل يحتاج السياق بالترتيب الزمني).
        """
        async with self.db_client() as session:
            async with session.begin():
                # نجلب آخر `limit` رسالة مرتبة من الأحدث إلى الأقدم
                stmt = (
                    select(ChatMessage)
                    .where(
                        ChatMessage.session_id == session_id,
                        ChatMessage.project_id == project_id
                    )
                    .order_by(desc(ChatMessage.created_at))
                    .limit(limit)
                )
                result = await session.execute(stmt)
                messages = result.scalars().all()

            # نعكس الترتيب ليصبح من الأقدم إلى الأحدث
            return list(reversed(messages))

    async def clear_session(self, session_id: str, project_id: int):
        """مسح كل رسائل جلسة محددة"""
        from sqlalchemy import delete
        async with self.db_client() as session:
            async with session.begin():
                stmt = delete(ChatMessage).where(
                    ChatMessage.session_id == session_id,
                    ChatMessage.project_id == project_id
                )
                result = await session.execute(stmt)
                await session.commit()
            return result.rowcount

    async def get_session_message_count(self, session_id: str, project_id: int):
        """عدد الرسائل في جلسة محددة"""
        async with self.db_client() as session:
            count_sql = select(func.count(ChatMessage.message_id)).where(
                ChatMessage.session_id == session_id,
                ChatMessage.project_id == project_id
            )
            result = await session.execute(count_sql)
            return result.scalar()
