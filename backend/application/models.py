from flask_sqlalchemy import SQLAlchemy
from application.database import db

class Sample(db.Model):
    __tablename__ = "samples"
    sample_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    section_id = db.Column(db.Integer, nullable=False)
    sample_dir = db.Column(db.String, nullable=False)
    transcript = db.Column(db.String)
    transliteration = db.Column(db.String)

class Post(db.Model):
    __tablename__ = "post"
    post_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String, nullable=False)
    description = db.Column(db.String)
    date = db.Column(db.DateTime, nullable=False, default=db.func.now())
    author = db.Column(db.String, nullable=False)
    
class Section(db.Model):
    __tablename__ = "section"
    section_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    post_id = db.Column(db.Integer, nullable=False)
    section_name = db.Column(db.String, nullable=False)
    description = db.Column(db.String)
    language = db.Column(db.String, nullable=False)
    gender = db.Column(db.String, nullable=False)
    category = db.Column(db.String, nullable=False)