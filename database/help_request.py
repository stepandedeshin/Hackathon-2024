import psycopg2
from aiogram import Router
from sqlalchemy import Column, Date, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, sessionmaker

from config import settings

DatabaseHelpRequestsRouter = Router()


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
session_of_help_requests = Session()
    
class HelpRequests(base_of_users):
    __tablename__ = f"help_requests"
    user_id = Column(String, primary_key = True)
    thread_id = Column(Integer, nullable = False)
    date_of_conversation = Column(Date, nullable = False)
    
base_of_users.metadata.create_all(engine_of_users)


async def add_thread(data: dict) -> None:
    '''
    Adding user info when user starting a conversation with an admin
    user info contains user_id, thread_id, date of conversation request
    thread_id helps bot to initialize right admin chat with user to connect each other
    if user not exists in table "help_requests" the func adds a new user to table, else just changing thread_id and date of last conversation

    returns None
    '''
    user_id = data["user_id"]
    thread_id = data["thread_id"]
    date = data["date"]
    user = session_of_help_requests.query(HelpRequests).filter_by(user_id = user_id).first()
    if not user:
        new_user = HelpRequests(thread_id = thread_id, user_id = user_id, date_of_conversation = date)
        session_of_help_requests.add(new_user)
        session_of_help_requests.commit()
    else:
        user.thread_id = thread_id
        user.date_of_conversation = date
        session_of_help_requests.commit()
    return


async def return_user_by_thread_id(thread_id: int) -> list:
    '''
    returns user by finding user info with thread_id
    user_id and thread_id are unique and right info easy can be finded by them
    requires thread_id to find user_info

    returns list of user data

    in case of user not exists returns none
    '''
    user = session_of_help_requests.query(HelpRequests).filter_by(thread_id = thread_id).first()
    if user:
        return [user.user_id, user.thread_id, user.date_of_conversation]
    return

async def return_user_by_user_id(user_id: str) -> list:
    '''
    returns user by finding user info with user_id
    user_id and thread_id are unique and right info easy can be finded by them
    requires user_id to find user_info

    returns list of user data

    in case of user not exists returns none
    '''
    user = session_of_help_requests.query(HelpRequests).filter_by(user_id = user_id).first()
    if user:
        return [user.user_id, user.thread_id, user.date_of_conversation]
    return