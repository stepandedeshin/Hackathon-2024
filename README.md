# Hackathon-2024
Case solution
# To start the application download the source code and unpack it.
Use any directory you want
# Create venv and .env files in the root. 
Create venv by python -m venv .venv or use python3 -m venv .venv in case of error
Create .env 
# Install required libraries
See required libraries in requirements.txt or use 
  1. "venv_file_name"\Scripts\Activate
visit https://gist.github.com/2ik/3ddbef3263dee8e76b63a391e2ffe5d0 in case of "выполнение сценариев запрещено в этой системе"
  2. pip install aiogram sqlalchemy psycopg2 requests pydantic pydantic_settings
use pip3 install aiogram sqlalchemy psycopg2 requests pydantic pydantic_settings in case of error
# Enter the config credentials to ".env".
See required credentials in config.py
# Database connection
We prefer to use postgresql+psycopg2 connection to database but sqlalchemy allows to connect a lot of database types
