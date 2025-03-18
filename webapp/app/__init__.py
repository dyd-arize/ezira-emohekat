from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os
import logging
from celery import Celery, Task

logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.DEBUG if os.getenv("WEBAPP_DEBUG") == "True" else logging.INFO
)

load_dotenv()

db = SQLAlchemy()


def create_app() -> Flask:
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

    logger.debug("Loading {}...".format(models.__name__))
    with app.app_context():
        # need to run gunicorn with --preload to prevent race condition
        db.create_all()

    # add routes
    from .routes import setup_routes

    setup_routes(app)

    # init celery
    app.config.from_mapping(
        CELERY=dict(
            broker_url="amqp://{}:{}@{}:5672/".format(
                os.getenv("RABBITMQ_DEFAULT_USER"),
                os.getenv("RABBITMQ_DEFAULT_PASS"),
                os.getenv("RABBITMQ_HOST"),
            ),
            result_backend="redis://{}:6379/0".format(os.getenv("REDIS_HOST")),
        ),
    )
    celery_init_app(app)

    return app


def celery_init_app(app: Flask) -> Celery:
    class FlaskTask(Task):
        def __call__(self, *args: object, **kwargs: object) -> object:
            with app.app_context():
                return self.run(*args, **kwargs)

    celery_app = Celery(app.name, task_cls=FlaskTask)
    celery_app.config_from_object(app.config["CELERY"])
    celery_app.set_default()
    app.extensions["celery"] = celery_app
    return celery_app
