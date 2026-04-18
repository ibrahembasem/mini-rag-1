from fastapi import FastAPI
from routes import base, data, nlp
from helpers.config import get_setting
from stores.llm.LLMProviderFactory import LLMProviderFactory
from stores.vectordb.VectorDBProviderFactory import VectorDBProviderFactory
from stores.llm.templates.template_parser import TemplateParser
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
app = FastAPI()

async def startup_span():
    setting = get_setting()

    postgres_conn = f"postgresql+asyncpg://{setting.POSTGRES_USERNAME}:{setting.POSTGRES_PASSWORD}@{setting.POSTGRES_HOST}:{setting.POSTGRES_PORT}/{setting.POSTGRES_MAIN_DATABASE}"
    
    app.db_engine = create_async_engine(postgres_conn)
    app.db_client = sessionmaker(
        app.db_engine, class_= AsyncSession, expire_on_commit=False
    )



    #app.mongo_conn = AsyncIOMotorClient(setting.MONGO_URL)
    #app.db_client = app.mongo_conn[setting.MONGODB_DATABASE]

    llm_provider_factory = LLMProviderFactory(setting)
    vectordb_provider_factory = VectorDBProviderFactory(config =setting, db_client=app.db_client)

    # generating client
    app.generation_client = llm_provider_factory.create(provider = setting.GENERATION_BACEND)
    app.generation_client.set_generation_model(model_id= setting.GENERATION_MODEL_ID)
    
    # embedding client 
    app.embedding_client = llm_provider_factory.create(provider=setting.EMBEDDING_BACKEND)
    app.embedding_client.set_embedding_model(model_id=setting.EMBEDDING_MODEL_ID,
                                             embedding_size=setting.EMBEDDING_SIZE)
    

    # vector db client
    app.vectordb_client = vectordb_provider_factory.create(
        provider= setting.VECTOR_DB_BACKEND
    )

    await app.vectordb_client.connect()

    app.template_parser = TemplateParser(
        language=setting.PRIMARY_LANG,
        default_language=setting.DEFAULT_LANG,
    )




async def shutdown_span():
    #app.mongo_conn.close()
    await app.db_engine.dispose()
    await app.vectordb_client.disconnect()


#app.router.lifespan.on_startup.append(startup_span)
#app.router.lifespan.on_startup.append(shutdown_span)

app.on_event("startup")(startup_span)
app.on_event("shutdown")(shutdown_span)




app.include_router(base.base_router)
app.include_router(data.data_router)
app.include_router(nlp.nlp_router)
