UPLOAD_FOLDER = "./static/img/"
KEY = ".key"
DB = "sqlite:///database.sqlite3"
ALLOWED_EXTENSIONS = {'wav', 'mp3'}

class Config():
    SQLALCHEMY_DATABASE_URI = DB
    UPLOAD_FOLDER = UPLOAD_FOLDER
    CORS_HEADERS = 'Content-Type'
    # CELERY_BROKER_URL = "redis://localhost:6379/1"
    # CELERY_RESULT_BACKEND = "redis://localhost:6379/2"
    # CACHE_TYPE= 'redis'
    # CACHE_REDIS_URL= 'redis://localhost:6379/3'
    # CACHE_DEFAULT_TIMEOUT= 300