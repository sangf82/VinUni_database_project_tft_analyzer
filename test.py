from sqlalchemy import create_engine, text
import os
from dotenv import load_dotenv
load_dotenv()

CONFIG = {
    "db_host": os.getenv("DB_HOST"),
    "db_port": os.getenv("DB_PORT"),
    "db_user": os.getenv("DB_USER"),
    "db_password": os.getenv("DB_PASSWORD"),
    "db_name": os.getenv("DB_NAME"),
}

def take_url(CONFIG):
    url = f"mysql+pymysql://{CONFIG['db_user']}:{CONFIG['db_password']}@{CONFIG['db_host']}:{CONFIG['db_port']}/{CONFIG['db_name']}"
    
    return url

url = take_url(CONFIG)

try:
    engine = create_engine(url)
    with engine.connect() as conn:
        result = conn.execute(text("SELECT * FROM `user` LIMIT 1;"))
        print("Connection successful:", result.scalar() == 1)
except Exception as e:
    print("Connection failed:", e)

beevtt