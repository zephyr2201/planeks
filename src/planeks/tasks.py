import csv
from typing import List
from pathlib import Path

from core.celery import app
from django.core.files.base import ContentFile

from .services import (
    check_characters,
    generate_fake_data,
)
from .selectors import fetch_csv


@app.task(max_retries=None, time_limit=10800)
def writer_csv(pk: int, types: List, header: List) -> None:
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
    # Create field
    with open(filename, 'rb') as f:
        csv_obj.csv_file = ContentFile(
            f.read(),
            name=f'{csv_obj.name}.csv'
        )
        csv_obj.save()
