from flask import render_template
from . import logger
from .models import Actuals


def setup_routes(app):
    @app.route("/")
    def index():
        data = Actuals.query.all()
        logger.debug(data)
        return render_template("table.html", title="Actuals", data=data)
