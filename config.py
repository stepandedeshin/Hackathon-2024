from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    TOKEN: str
    HOST: str
    PORT: int
    USER: str
    PASS: str
    DATABASE_NAME: str
    
    class Config:
        env_file = ".env"
    
settings = Settings()