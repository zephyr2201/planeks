import faker
import random
from typing import List

from .models import Csv


fake = faker.Faker()


def generate_fake_data(types: List) -> List:
    data = []
    for i in types:
        if i == '1':
            data.append(f'{fake.first_name_nonbinary()} {fake.last_name_nonbinary()}')
        elif i == '2':
            data.append(fake.job())
        elif i == '3':
            data.append(fake.ascii_email())
        elif i == '4':
            data.append(fake.domain_name())
        elif i == '5':
            data.append(fake.phone_number())
        elif i == '6':
            data.append(fake.company())
        elif i == '7':
            data.append(fake.paragraphs(nb=1)[0])
        elif i == '8':
            data.append(random.randint(1, 100))
        elif i == '9':
            data.append(fake.address())
        elif i == '10':
            data.append(fake.date())
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
