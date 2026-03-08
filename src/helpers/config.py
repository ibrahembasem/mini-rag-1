from pydantic_settings import BaseSettings, SettingsConfigDict

class Setting(BaseSettings):

    APP_NAME : str
    APP_VERSION : str
    OPENAI_API_KEY: str
    
    FILE_ALLOWED_TYPE: list
    FILE_MAX_SIZE: int
    FILE_DEFAULT_CHUNK_SIZE : int

    model_config = SettingsConfigDict(env_file=".env")


def get_setting():
    return Setting()

