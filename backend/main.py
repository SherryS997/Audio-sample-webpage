from flask import Flask
from flask_cors import CORS
from application.config import Config
from application.database import db

app = Flask(__name__)
CORS(app)
app.config.from_object(Config)
db.init_app(app)
app.app_context().push()

from application.routes import *
from application.models import *

if __name__ == '__main__':
    app.run(debug=True, port=1234)