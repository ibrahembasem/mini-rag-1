from pydantic import BaseModel, Field, field_validator, ConfigDict
from typing import Optional, Any
# من الأفضل استيرادها هكذا لضمان التوافق
from bson import ObjectId 

class Project(BaseModel):
    # نستخدم Any أو حلاً مخصصاً لأن Pydantic V2 صارم مع ObjectId
    id: Optional[Any] = Field(None, alias="_id") 
    project_id: str = Field(..., min_length=1)

    # 1. تصحيح الإملاء هنا (إضافة حرف t)
    @field_validator('project_id')
    @classmethod
    def validate_project_id(cls, value):
        if not value.isalnum():
            raise ValueError("project_id must be alphanumeric")
        return value
    
    # 2. الطريقة الحديثة لتعريف الـ Config في V2
    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        populate_by_name=True # لتسمح باستخدام id بدلاً من _id
    )