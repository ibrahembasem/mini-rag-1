from enum import Enum

class ResponseSignal(Enum):

    FILE_VALIDATE_SUCCESS = "file validate successfully"
    FILE_TYPE_NOT_SUPPORTED = "file type not supported"
    FILE_SIZE_EXCEEDED = "file size exceeded"
    FILE_UPOLAD_SUCCESS = "file upload success"
    FILE_UPOLAD_FAILED = "file upload failed"
    PROCESSING_FAILED = "processin failed"
    PROCESSING_SUCCESS = "processing success"