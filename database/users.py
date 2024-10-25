from aiogram import Router
from aiogram.types import CallbackQuery
import psycopg2
from sqlalchemy import Column, String, create_engine, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session


from config import settings


DatabaseUsersRouter = Router()


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
session_of_users = Session()
    
class Users(base_of_users):
    __tablename__ = "users"
    user_id = Column(String, primary_key = True)
    username = Column(String, nullable = False)
    name = Column(String, nullable = False)
    last_name = Column(String, nullable = True)
    date = Column(Date, nullable = False)
    phone_number = Column(String, nullable=True)

base_of_users.metadata.create_all(engine_of_users)


async def start_info(callback: CallbackQuery) -> None:
    user_id = str(callback.from_user.id)
    username = str(callback.from_user.username)
    name = str(callback.from_user.first_name)
    last_name = str(callback.from_user.last_name)
    date = str(callback.message.date)
    user = session_of_users.query(Users).filter_by(user_id = user_id).first()
    if not user:
        new_user = Users(user_id = user_id, username = username, name = name, last_name = last_name, date = date)
        session_of_users.add(new_user)
        session_of_users.commit()
    return
