from flask import render_template, request, jsonify
from . import logger, db
from .models import Actuals
from .tasks import add
from celery.result import AsyncResult


def setup_routes(app):
    # docstrings are generated by Copilot with manual improvements
    @app.route("/", methods=["GET"])
    def index():
        """
        Handle the root endpoint.

        Retrieves all records from the 'actuals' table and renders them in an HTML template.
        If an error occurs during the query, logs the error and returns a placeholder error response.

        Returns:
            Rendered HTML page displaying the data from the 'actuals' table.
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
        Handle data insertion into the 'actuals' table.

        Expects a JSON payload containing:
        - "ts" (timestamp in ISO format, e.g. 2025-03-16 18:35:46.759)
        - "value" (float)

        Logs errors if JSON parsing or database insertion fails.

        Test:
        curl -X POST http://127.0.0.1:5000/insert \
        -H "Content-Type: application/json" \
        -d '{"ts": "'"$(date -u +"%Y-%m-%dT%H:%M:%S.%6N")"'", "value": 42.5}'

        Returns:
            JSON response indicating success or failure.
            - On success: {"message": "Inserted!"}, HTTP 200.
            - On failure: {"status": "error"}, HTTP 500.
        """
        try:
            ts, value = request.json.get("ts"), request.json.get("value")
            logger.debug(f"ts, value: {ts}, {value}")
        except Exception as e:
            logger.error(f"request.json: {request.json}")
            logger.error(e, exc_info=True)
            return jsonify({"status": "Incorrect request data"}), 400

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
        Health check endpoint.

        Test:
        curl -X POST http://127.0.0.1:5000/healthcheck

        Returns:
            JSON response indicating success.
            - On success: {"message": "Inserted!"}, HTTP 200.
        """

        return jsonify({"message": "Healthy!"}), 200

    @app.route("/minio/webhook", methods=["POST"])
    def minio_webhook():
        try:
            event_data = request.json  # MinIO sends JSON payloads
            if not event_data:
                return jsonify({"error": "No data received"}), 400
            logger.debug(f"Received MinIO event: {event_data}")
            result = add.delay(1, 2)
            logger.info(f"result_id: {result.id}")
            return jsonify({"result_id": result.id}), 200
        except Exception as e:
            logger.error(e, exc_info=True)
            return jsonify({"message": "Error handling minio webhook"}), 500

    @app.route("/result/<id>", methods=["GET"])
    def task_result(id: str) -> dict[str, object]:
        result = AsyncResult(id)
        return {
            "ready": result.ready(),
            "successful": result.successful(),
            "value": result.result if result.ready() else None,
        }
