from app import create_app

flask_app = create_app()
celery_app = flask_app.extensions["celery"]
celery_app.conf.update(broker_connection_retry_on_startup=True)

if __name__ == "__main__":
    celery_app.start()
