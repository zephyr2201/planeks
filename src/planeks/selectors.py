from .models import Csv


def fetch_csv(pk):
    try:
        return Csv.objects.get(pk=pk)
    except Csv.DoesNotExist as e:
        raise e
