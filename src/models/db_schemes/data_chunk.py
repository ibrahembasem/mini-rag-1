from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, Any, Dict
from bson import ObjectId

class DataChunk(BaseModel):
    id: Optional[Any] = Field(None, alias="_id") 
    chunk_text: str = Field(..., min_length=1)
    chunk_metadata: Dict = {}
    chunk_order: int = Field(..., gt=0)
    chunk_project_id: Any 

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        populate_by_name=True
    )

    @classmethod
    def get_indexess(cls):

          return [
            {
                "key":[
                    ("chunk_project_id", 1)
                ],
                "name":"chunk_project_id_index_1",
                "unique":False
            }
        ]