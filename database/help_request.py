from aiogram import Router
import psycopg2
from sqlalchemy import Column, String, Integer, create_engine, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session


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
    thread_id = Column(Integer, primary_key = True)
    user_id = Column(String, nullable = False)
    date_of_conversation = Column(Date, nullable = False)
    
base_of_users.metadata.create_all(engine_of_users)