from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import timedelta
import warnings

warnings.filterwarnings("ignore", category=DeprecationWarning)
warnings.filterwarnings("ignore", category=FutureWarning)

app = Flask(__name__)
app.secret_key = 'artifymeappdev'

app.config['SQLALCHEMY_ECHO'] = True

app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(minutes=30)

app.config['SQLALCHEMY_MAX_OVERFLOW'] = 0

app.config['SQLALCHEMY_DATABASE_URI'] = \
    'mysql+pymysql://root:root@localhost:3306/artifymedb'

db = SQLAlchemy(app)

input_files = r"base\static\input_images"
output_files = r"base\static\output_images"

app.config['INPUT_FILES'] = input_files
app.config['OUTPUT_FILES'] = output_files

from base.com import controller
