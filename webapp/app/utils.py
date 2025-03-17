from .models import Actuals
import pandas as pd
from io import BytesIO
from datetime import datetime as dt
from . import logger, db


def insert_actuals_from_stream(stream: BytesIO):
    try:
        df = pd.read_csv(stream)

        for _, row in df.iterrows():
            ts = dt.strptime(row["ts"], "%Y-%m-%dT%H:%M:%S.%f")
            value = row["value"]
            actual = Actuals(ts=ts, value=value)
            db.session.add(actual)
        db.session.commit()
    except Exception as e:
        logger.error(e, exc_info=True)
        raise
