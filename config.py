from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    TOKEN: str
    HOST: str
    PORT: int
    USER: str
    PASS: str
    DATABASE_NAME: str
    DATABASE_LINK: str
    GPT_API_TOKEN: str
    ADMINS: list

    class Config:
        env_file = ".env"
    
settings = Settings()