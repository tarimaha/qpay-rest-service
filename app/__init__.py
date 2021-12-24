from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate




app = Flask(__name__)

app.config.from_object('config.Config')

api = Api(app)
db = SQLAlchemy(app)
migrate = Migrate(app,db)
jwt = JWTManager(app)

from . import resources
from . import urls
