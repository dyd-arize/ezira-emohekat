from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.DEBUG if os.getenv("DEBUG") == "True" else logging.INFO
)

load_dotenv()

db = SQLAlchemy()


def create_app():
    app = Flask(__name__)

    # init db
    app.config["SQLALCHEMY_DATABASE_URI"] = (
        "postgresql://{user}:{password}@{host}/{db}".format(
            user=os.getenv("POSTGRES_USER"),
            password=os.getenv("POSTGRES_PASSWORD"),
            host=os.getenv("POSTGRES_HOST"),
            db=os.getenv("POSTGRES_DB"),
        )
    )
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)

    # provision tables
    from . import models

    with app.app_context():
        db.create_all()

    # add routes
    from .routes import setup_routes

    setup_routes(app)

    return app
