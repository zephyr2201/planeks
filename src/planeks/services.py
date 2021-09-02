import csv
import faker
import random
from typing import List
from .models import Csv
from django.core.files.base import ContentFile


fake = faker.Faker()


def generate_fake_data(types, row):
    data = []
    for j in range(0, row):
        array = []
        for i in types:
            if i == '1':
                array.append(f'{fake.first_name_nonbinary()} {fake.last_name_nonbinary()}')
            elif i == '2':
                array.append(f'{fake.job()}')
            elif i == '3':
                array.append(f'{fake.ascii_email()}')
            elif i == '4':
                array.append(f'{fake.domain_name()}')
            elif i == '5':
                array.append(f'{fake.phone_number()}')
            elif i == '6':
                array.append(f'{fake.company()}')
            elif i == '7':
                array.append(f'{fake.paragraphs(nb=5)}')
            elif i == '8':
                array.append(f'{random.randint(1,100)}')
            elif i == '9':
                array.append(f'{fake.address()}')
            elif i == '10':
                array.append(f'{fake.date()}')
        data.append(array)
    return data


def check_characters(csv_obj: Csv) -> str:
    if csv_obj.string_characters == '1':
        char = '"'
    else:
        char = '\''

    if csv_obj.column_separator == '1':
        delim = ","
    else:
        delim = ";"
    return delim, char


def writer_csv(csv_obj: Csv, data: List, header: List) -> None:
    filename = f'/code/src/csv_files/{csv_obj.name}.csv'
    delimiter, char = check_characters(csv_obj)
    with open(filename, 'w', encoding='UTF8', newline='') as f:
        writer = csv.writer(f, delimiter=delimiter, quotechar=char)
        writer.writerow(header)
        writer.writerow(data)
    with open(filename, 'rb') as f:
        csv_obj.csv_file = ContentFile(f.read(), name='ers.csv')
        csv_obj.save()
