from enum import Enum

class ResponseSignal(Enum):

    FILE_VALIDATE_SUCCESS = "file validate successfully"
    FILE_TYPE_NOT_SUPPORTED = "file type not supported"
    FILE_SIZE_EXCEEDED = "file size exceeded"
    FILE_UPOLAD_SUCCESS = "file upload success"
    FILE_UPOLAD_FAILED = "file upload failed"
    PROCESSING_FAILED = "processin failed"
    PROCESSING_SUCCESS = "processing success"
    NO_FILES_ERROR = "not found files"
    FILE_ID_ERROR =  "no file found with this id"
    PROJECT_NOT_FOUND_ERROR = "project not found"
    INSERT_INTO_VECTORDB_ERROR = "insert into vectordb error"
    INSERT_INTO_VECTORDB_SUCCESS = "insert into vectordb success"
    VECTORDB_COLLECTION_RETRIVED = "vectordb collection retrieved"
    VECTORDB_SEARCH_ERROR = "Vectordb search error"
    VECTORDB_SEARCH_SUCCESS = "Vectordb search success"