APP_NAME='ibrahem-mini-RAG'
APP_VERSION = '0.1'

FILE_ALLOWED_TYPE=['text/plain','application/pdf']
FILE_MAX_SIZE=10
FILE_DEFAULT_CHUNK_SIZE= 512000

#================================= MONGO DATABASE CONFIG =====================
#MONGO_URL= "mongodb://ibrahem:99474697@localhost:27007"
#MONGODB_DATABASE = "mini-rag"

#================================= POSTGRES DATABASE CONFIG ===================
POSTGRES_USERNAME="postgres"
POSTGRES_PASSWORD="minirag1234"
POSTGRES_HOST="localhost"
POSTGRES_PORT="5432"
POSTGRES_MAIN_DATABASE="minirag"


#================================= LLM CONFIG ===============================

GENERATION_BACKEND = "COHERE"
EMBEDDING_BACKEND = "COHERE"  


OPENAI_API_KEY = ""
OPENAI_API_URL = 

COHERE_API_KEY = ""

GENERATION_MODEL_ID_LITERAL = ["gemma2:9b-instruct-q5_0","gpt-4o-mini","gpt-4o"]
GENERATION_MODEL_ID = "gpt-3.5-turbo-0125"
EMBEDDING_MODEL_ID="embed-multilingual-light-v3.0"
EMBEDDING_SIZE = 384

INPUT_DEFAULT_MAX_CHARACTERS = 1024
GENERATION_DEFAULT_MAX_TOKENS = 200
GENERATION_DEFAULT_TEMPERATURE = 0.1


#================================= Vector DB CONFIG ===============================
VECTOR_DB_BACKEND_LITERAL = ["QDRANT", "PGVECTOR"]
VECTOR_DB_BACKEND = "PGVECTOR" # PGVECTOR, QDRANT
VECTOR_DB_PATH = "qdrant_db"
VECTOR_DB_METHOD = "cosine"

#================================= Template Configs ===============================
PRIMARY_LANG = "en"
DEFAULT_LANG = "en"

 #================================= WhatsApp Cloud API ===========================
WHATSAPP_VERIFY_TOKEN=""
WHATSAPP_API_TOKEN=
WHATSAPP_PHONE_NUMBER_ID=""
WHATSAPP_DEFAULT_PROJECT_ID=""