from celery import shared_task, states
from minio import Minio
import os
from io import BytesIO
from . import logger
from .utils import insert_actuals_from_stream


@shared_task()
def async_add(x, y) -> int:
    return x + y


@shared_task(bind=True)
def ingest_csv(self, bucket: str, key: str) -> dict[str, str]:
    try:
        # Get the object from MinIO
        minio_client = Minio(
            "{}:9000".format(os.getenv("MINIO_HOST")),
            # TODO - not using the root user
            access_key=f"{os.getenv('MINIO_ROOT_USER')}",
            secret_key=f"{os.getenv('MINIO_ROOT_PASSWORD')}",
            # TODO - should use HTTPS
            secure=False,
        )
        obj = minio_client.get_object(bucket, key)
        insert_actuals_from_stream(BytesIO(obj.read()))
        logger.info(f"Successfully ingested {bucket}/{key}.")
        return {"bucket": bucket, "key": key, "status": "success"}

    except Exception as e:
        self.update_state(state=states.FAILURE)
        logger.error(f"Failed to ingest {bucket}/{key}.")
        logger.error(e, exc_info=True)
        raise e
