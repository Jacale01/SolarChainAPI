import os

from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


def get_database_url():
    return os.getenv("DATABASE_URL", "sqlite:///pji2.db")


def init_db(app):
    app.config.setdefault("SQLALCHEMY_DATABASE_URI", get_database_url())
    app.config.setdefault("SQLALCHEMY_TRACK_MODIFICATIONS", False)
    app.config.setdefault("JWT_SECRET_KEY", os.getenv("JWT_SECRET_KEY", "pji2-dev-secret-key-1234567890"))
    db.init_app(app)


