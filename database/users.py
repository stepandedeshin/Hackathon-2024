import psycopg2
from aiogram import Router
from aiogram.types import Message
from sqlalchemy import Column, Date, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, sessionmaker

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


async def start_info(message: Message) -> None:
    '''
    Adds an information about user after using "/start"
    new user object contains user_id, username, name, last_name, date of first activation
    '''
    user_id = str(message.from_user.id)
    username = str(message.from_user.username)
    name = str(message.from_user.first_name)
    last_name = str(message.from_user.last_name)
    date = str(message.date)
    user = session_of_users.query(Users).filter_by(user_id = user_id).first()
    if not user:
        new_user = Users(user_id = user_id, username = username, name = name, last_name = last_name, date = date)
        session_of_users.add(new_user)
        session_of_users.commit()
    return


async def add_phone_number(message: Message) -> None:
    '''
    Adds an information about phone number if user exists in table "users"
    requires user_id to find user data in table "users" and adds shared phone number or changes it to current if None
    
    returns None
    '''
    user_id = str(message.from_user.id)
    phone_number = str(message.contact.phone_number)
    user = session_of_users.query(Users).filter_by(user_id = user_id).first()
    if user:
        user.phone_number = phone_number
        session_of_users.commit()
    return


async def return_phone_number_or_none(user_id: str) -> str | None:
    '''
    Returns phone number
    requires user_id to find user data in table "users" and returns phone number if exists
    in case of phone number = None or user not exists returns None
    '''
    user = session_of_users.query(Users).filter_by(user_id = user_id).first()
    if user:
        return user.phone_number
    return


async def delete_phone_number(user_id: str) -> None:
    '''
    Delete user.phone_number from table "users"
    requires user_id to find user data in table "users" and deletes phone number if exists
    
    returns None
    '''
    user = session_of_users.query(Users).filter_by(user_id = user_id).first()
    if user:
        user.phone_number = None
        session_of_users.commit()
    return
