from enum import Enum
from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    # Database settings
    DB_HOST: str
    DB_USER: str
    DB_PASSWORD: str
    DB_NAME: str
    DB_PORT: int = 27017  # Default MongoDB port
    DB_URI: str
    # Pinecone settings
    PINECONE_API_KEY: str
    PINECONE_INDEX_NAME: str
    
    # OpenAI settings
    OPENAI_API_KEY: str
    
    # LangSmith settings
    LANGSMITH_ENDPOINT: str = "https://api.smith.langchain.com"
    LANGSMITH_API_KEY: str
    LANGSMITH_PROJECT: str
    LANGSMITH_TRACING: bool = True
    class Config:
        env_file = ".env"
        case_sensitive = True

class ModelType(str, Enum):
    gpt4o = 'gpt-4o'
    gpt4o_mini = 'gpt-4o-mini'
    embedding = 'text-embedding-ada-002'

@lru_cache()
def get_settings():
    return Settings()

settings = get_settings()