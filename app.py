import os
import logging
from flask import Flask, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from werkzeug.middleware.proxy_fix import ProxyFix
from dotenv import load_dotenv

# Set up logging
logging.basicConfig(level=logging.DEBUG)

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)

# Create the app
app = Flask(__name__, static_folder='static', template_folder='templates')
app.secret_key = os.environ.get("SESSION_SECRET", "dev-secret-key-change-in-production")
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

# Configure the database
# Load environment variables from .env file
load_dotenv()

DATA_CONFIG = {
    "db_host": os.getenv("CD_HOST"),
    "db_port": os.getenv("CD_PORT"),
    "db_user": os.getenv("CD_USER"),
    "db_password": os.getenv("CD_PASSWORD"),
    "db_name": os.getenv("CD_NAME"),
}

CONFIG = {
    "db_host": "127.0.0.1",
    "db_port": "3306",
    "db_user": "root",
    "db_password": "080204",
    "db_name": "tft_app",
}

def get_database_url(config_dict):
    if all(config_dict.values()):
        return f"mysql+pymysql://{config_dict['db_user']}:{config_dict['db_password']}@{config_dict['db_host']}:{config_dict['db_port']}/{config_dict['db_name']}"
    return None

def configure_database(app, config):
    
    mysql_url = get_database_url(config)
    
    if not mysql_url:
        raise ValueError("Invalid database configuration provided")
    
    app.config["SQLALCHEMY_DATABASE_URI"] = mysql_url
    app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
        "pool_recycle": 300,
        "pool_pre_ping": True,
    }


configure_database(app, CONFIG)

# Initialize the app with the extension
db.init_app(app)

with app.app_context():
    # Import models and routes
    import models
    import routes
    
    # Create tables only if they don't exist
    try:
        db.create_all()
        logging.info("Database tables verified/created successfully.")
    except Exception as e:
        logging.warning(f"Database table creation skipped or failed: {e}")
    
@app.route('/static/<path:filename>')
def static_files(filename):
    response = send_from_directory('static', filename)
    response.cache_control.no_cache = True
    response.cache_control.no_store = True
    response.cache_control.must_revalidate = True
    return response

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
