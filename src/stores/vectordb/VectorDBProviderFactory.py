from .providers import QdrantDBProvider , PGVectorProvider
from .VectorDBEnums import VecotrDBEnums
from controllers.BaseController import BaseController
from sqlalchemy.orm import sessionmaker

class VectorDBProviderFactory:
    def __init__(self, config, db_client: sessionmaker = None):
        self.db_client = db_client
        self.config = config
        self.base_controller = BaseController()

    def create(self, provider: str):
        if provider == VecotrDBEnums.QDRANT.value:
            qdrant_db_client = self.base_controller.get_database_path(db_name=self.config.VECTOR_DB_PATH)
            
            return QdrantDBProvider(
                db_client = qdrant_db_client,
                distance_method= self.config.VECTOR_DB_DISTANCE_METHOD
            )
        
        if provider == VecotrDBEnums.PGVECTOR.value:
            return PGVectorProvider(
                db_client=self.db_client,
                distance_method=self.config.VECTOR_DB_DISTANCE_METHOD,
                default_vector_size=self.config.EMBEDDING_SIZE,
                index_threshold=self.config.VECTOR_DB_PGVEC_INDEX_THRESHOLD,
            )

        
        return None

