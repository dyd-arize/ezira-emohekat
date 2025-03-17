from flask import render_template, jsonify, request
from . import logger, db
from .models import Actuals
from .tasks import ingest_csv, async_add
from celery.result import AsyncResult


def setup_routes(app):
    @app.route("/", methods=["GET"])
    def index():
        """
        Fetches all records from the Actuals table and renders them in a template.

        Returns:
            str: Rendered HTML template containing the actuals data.
        """
        try:
            data = Actuals.query.all()
        except Exception as e:
            logger.error(e, exc_info=True)
            data = [{"date:": "error", "value": "error"}]
        logger.debug(f"Size of data: {len(data)}")
        # logger.debug(data)
        return render_template("table.html", title="Actuals", data=data)

    @app.route("/insert", methods=["POST"])
    def insert():
        """
        Inserts a new actual record into the database.
        ts (str): Timestamp of the actual record.
        value (str): Value of the actual record.

        Returns:
            tuple[dict, int]: JSON response message and HTTP status code.
        """
        try:
            ts, value = request.json.get("ts"), request.json.get("value")
        except Exception as e:
            logger.error(e, exc_info=True)
            return jsonify({"status": "Error parsing JSON"}), 400

        try:
            actual = Actuals(ts, value)
            db.session.add(actual)
            db.session.commit()
        except Exception as e:
            logger.error(f"trying to insert actual: {actual}")
            logger.error(e, exc_info=True)
            return jsonify({"status": "Error inserting an actual"}), 500

        return jsonify({"message": "Inserted!"}), 200

    @app.route("/healthcheck", methods=["GET"])
    def health_check():
        """
        Health check endpoint to verify if the service is running.

        Returns:
            tuple[dict, int]: JSON response indicating health status and HTTP status code.
        """
        return jsonify({"message": "Healthy!"}), 200

    @app.route("/minio/webhook", methods=["POST"])
    def minio_webhook():
        """
        Handles webhook events from MinIO and triggers CSV ingestion.

        Returns:
            tuple[dict, int]: JSON response containing the task result ID or error message.
        """
        try:
            event_data = request.json
            if not event_data:
                return jsonify({"error": "No JSON data in request"}), 400
            if "Records" not in event_data:
                return jsonify({"error": "Missing 'Records' key"}), 400
            if len(event_data["Records"]) == 0:
                return jsonify({"error": "No records in the event"}), 400

            logger.debug(f"Received MinIO event: {event_data}")
            for record in event_data["Records"]:
                bucket = record["s3"]["bucket"]["name"]
                key = record["s3"]["object"]["key"]
                logger.debug(f"Bucket: {bucket}, Key: {key}")
                result = ingest_csv.delay(bucket, key)
            return jsonify({"result_id": result.id}), 200
        except Exception as e:
            logger.error(e, exc_info=True)
            return jsonify({"message": "Error handling minio webhook"}), 500

    @app.route("/add", methods=["GET"])
    def add():
        """
        Adds two numbers asynchronously using a Celery task.
        x (int): First number to add.
        y (int): Second number to add.

        Returns:
            dict: Dictionary containing the task ID.
        """
        x = request.args.get("x", type=int)
        y = request.args.get("y", type=int)
        result = async_add.delay(x, y)
        return {"task_id": result.id}

    @app.route("/result/<id>", methods=["GET"])
    def task_result(id: str):
        """
        Fetches the status and result of an asynchronous task.

        Args:
            id (str): Task ID to fetch the result.

        Returns:
            dict: Dictionary containing task status and result if available.
        """
        result = AsyncResult(id)
        return {
            "ready": result.ready(),
            "successful": result.successful(),
            "value": result.result if result.ready() else None,
        }
