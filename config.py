import os 
from datetime import timedelta


basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = 'secret key string'
    SQLALCHEMY_DATABASE_URI = "sqlite:///db.sqlite"
    JWT_SECRET_KEY = "super-secret"
    ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
    UPLOAD_FOLDER = os.path.join(basedir, "training_dataset")
    DEBUG = True
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(days=30)
