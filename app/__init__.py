from flask import Flask
from config import Config
from flask_mail import Mail
from flask_cors import CORS

app = Flask(__name__)
app.config.from_object(Config)
mail = Mail(app)
CORS(app)

from app import routes