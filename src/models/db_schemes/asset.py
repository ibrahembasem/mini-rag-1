from pydantic import BaseModel, Field, field_validator, ConfigDict
from typing import Optional, Any
from bson import ObjectId 
from datetime import datetime,timezone


class Asset(BaseModel):
    id: Optional[Any] = Field(None, alias="_id") 
    asset_project_id : ObjectId
    asset_type: str = Field(...,min_length=1)
    asset_name: str = Field(...,min_length=1)
    asset_size: int = Field(ge=0, default=None)
    asset_config: dict = Field(ge=0, default=None)
    asset_push_at:datetime = Field(default=datetime.utcnow)


    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        populate_by_name=True 
    )

    @classmethod
    def get_indexes(cls):

        return [
            {
                "key":[
                    ("asset_project_id", 1)
                ],
                "name":"asset_id_index_1",
                "unique":False
            },
             {
                "key":[
                    ("asset_project_id", 1),
                    ("asset_name",1)
                ],
                "name":"asset_project_id_index_1",
                "unique":True
            }
        ]
