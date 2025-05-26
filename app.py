import os
import logging
from flask import Flask
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
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "dev-secret-key-change-in-production")
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

# Configure the database
# Load environment variables from .env file
load_dotenv()

DATA_CONFIG = {
    "db_host": os.environ.get("DB_HOST","127.0.0.1"),
    "db_port": os.environ.get("DB_PORT","3306"),
    "db_user": os.environ.get("DB_USER","root"),
    "db_password": os.environ.get("DB_PASSWORD","123456"),
    "db_name": os.environ.get("DB_NAME","tft_app"),
}

CONFIG = {
    "db_host": "127.0.0.1",
    "db_port": "3306",
    "db_user": "root",
    "db_password": "123456",
    "db_name": "tft_app",
}

# Create MySQL database URL from config
if all(CONFIG.values()):
    mysql_url = f"mysql+pymysql://{DATA_CONFIG['db_user']}:{DATA_CONFIG['db_password']}@{DATA_CONFIG['db_host']}:{DATA_CONFIG['db_port']}/{DATA_CONFIG['db_name']}"
else:
    mysql_url = None


app.config["SQLALCHEMY_DATABASE_URI"] = mysql_url or "sqlite:///tft_analyzer.db"
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "pool_recycle": 300,
    "pool_pre_ping": True,
    "pool_size": 10,
    "max_overflow": 5,
    "pool_timeout": 30
}

# Initialize the app with the extension
db.init_app(app)

with app.app_context():
    # Import models and routes
    import models
    import routes
    
    # Create all tables
    db.create_all()
    
    # Initialize sample data if database is empty
    try:
        from sample_data import initialize_sample_data
        if models.User.query.count() == 0:
            logging.info("Initializing sample data...")
            initialize_sample_data()
        
        # Load additional data from MySQL if available
        if mysql_url:
            logging.info("Loading data from MySQL database...")
            # You can add specific data loading logic here
            # For example, sync data from another MySQL source
    except Exception as e:
        logging.error(f"Error initializing sample data: {e}")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
