from aiogram import Router
from aiogram.types import Message
import psycopg2
from sqlalchemy import Column, String, Integer, create_engine, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

from config import settings


DatabaseGPTRequestsRouter = Router()


try:
    conn = psycopg2.connect(
        host=settings.HOST,
        database=settings.DATABASE_NAME,
        user=settings.USER,
        password=settings.PASS
    )
    cursor = conn.cursor()
    conn.autocommit = True
    cursor.execute(f"CREATE DATABASE {settings.DATABASE_NAME}")
    cursor.close()
    conn.close()
except: pass

base_of_users = declarative_base()
engine_of_users = create_engine(settings.DATABASE_LINK, echo=True)
Session = sessionmaker(bind=engine_of_users)
session_of_gpt_requests = Session()
    
class GPTRequests(base_of_users):
    __tablename__ = f"gpt_requests"
    request_id = Column(Integer, primary_key = True)
    user_id = Column(String, nullable = False)
    request_text = Column(String, nullable = False)
    
base_of_users.metadata.create_all(engine_of_users)


async def add_request(message: Message) -> None:
    user_id = str(message.from_user.id)
    request_text = message.text
    new_request = GPTRequests(user_id = user_id, request_text = request_text)
    session_of_gpt_requests.add(new_request)
    session_of_gpt_requests.commit()
    return