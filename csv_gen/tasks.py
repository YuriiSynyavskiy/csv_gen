import csv
import json
from celery import shared_task
from datetime import datetime
from .models import Schema, Dataset
from django.conf import settings
from .fake_data import FAKE_DATA_GENERATOR
from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)
DATASET_PATH = "{path}dataset_{id}.csv"


def write_header(dataset_writer, schema):
    dataset_writer.writerow([p['name'] for p in schema.get('columns', [])])


@shared_task
def generate_csv(dataset, schema):
    logger.info(
        f"Generate {dataset['rows']} rows for {schema['name']} schema. ")
    redis = settings.REDIS_CONN
    with open(DATASET_PATH.format(
            path=str(settings.BASE_DIR)+settings.DATASETS_ROOT, id=dataset['id']), 'w') as csv_file:
        redis.set(str(dataset['id']), 0)
    
        dataset_writer = csv.writer(
            csv_file, delimiter=schema["delimeter"], quotechar=schema["quote"])

        write_header(dataset_writer, schema)
        """Write fake data"""
        for row in range(1, dataset['rows']+1):
            redis.set(str(dataset['id']), json.loads(
                redis.get(str(dataset['id']))) + 1)
            dataset_writer.writerow(
                [FAKE_DATA_GENERATOR[column['col_type']](column['col_filter'] or {}) for column in schema.get('columns', [])])

        redis.delete(str(dataset['id']))
        upd_dataset = Dataset.objects.get(id=dataset['id'])
        upd_dataset.status = "Ready"
        upd_dataset.save()
