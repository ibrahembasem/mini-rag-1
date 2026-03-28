from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, Any, Dict
from bson import ObjectId

class DataChunk(BaseModel):
    # نستخدم Any هنا لأن Pydantic V2 لا يدعم ObjectId تلقائياً
    id: Optional[Any] = Field(None, alias="_id") 
    chunk_text: str = Field(..., min_length=1)
    chunk_metadata: Dict = {}
    chunk_order: int = Field(..., gt=0)
    chunk_project_id: Any # أو استخدم ObjectId إذا كنت تفضل ولكن Any أضمن للتشغيل حالياً

    # هذا الجزء هو الحل للخطأ الذي ظهر لك
    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        populate_by_name=True
    )