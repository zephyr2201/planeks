from .models import Csv
from django.contrib.auth.models import User


def fetch_csv(pk: int) -> User:
    try:
        return Csv.objects.get(pk=pk)
    except Csv.DoesNotExist as e:
        raise e
