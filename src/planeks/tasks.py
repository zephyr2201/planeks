import csv
import logging
from typing import List
from pathlib import Path


from core.celery import app

from .services import (
    check_characters,
    generate_fake_data,
    send_to_file,
)
from .selectors import fetch_csv

logger = logging.getLogger(__name__)


@app.task(max_retries=None, time_limit=10800)
def writer_csv(pk: int, types: List, header: List, port: str) -> None:
    Path("csv_files").mkdir(parents=True, exist_ok=True)
    csv_obj = fetch_csv(pk)
    filename = f'/code/src/csv_files/{csv_obj.name}.csv'
    delimiter, char = check_characters(csv_obj)
    row = csv_obj.row

    # Write data in CSV file
    with open(filename, 'w', encoding='UTF8', newline='') as f:
        writer = csv.writer(f, delimiter=delimiter, quotechar=char)
        writer.writerow(header)
        for i in range(0, row):
            data = generate_fake_data(types)
            writer.writerow(data)

    with open(filename, 'rb') as f:
        send_to_file(f, pk, port)
