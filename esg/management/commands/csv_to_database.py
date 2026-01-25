import csv

from django.core.management import BaseCommand
from django.db import transaction
from esg.models import GasProduct, ElectroProduct, SantehProduct, Gas, Electro, Santeh

csv_path = 'products/electro.csv' # замена

class Command(BaseCommand):
    '''Переносит данные из csv-файла в базу данных postgres.'''

    def handle(self, *args, **options):

        with open(csv_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            next(reader)  # пропускаем заголовок

            with transaction.atomic():  # гарантирует целостность
                for row in reader:
                    try:
                        code = int(row[0])
                        title = row[1]
                        rubric_id = int(float(row[2]))
                        rubric = Electro.objects.get(pk=rubric_id) # замена

                        product = ElectroProduct(
                            code=code,
                            title=title,
                            rubric=rubric,
                            status_new=False,         # по умолчанию
                            status_popular=False,     # по умолчанию
                            counter=0                 # по умолчанию
                        )   # замена
                        product.save()  # вызовет транслитерацию
                    except Electro.DoesNotExist: # замена
                        print(f"Rubric с id={rubric_id} не найден. Строка пропущена.")
                    except Exception as e:
                        print(f"Ошибка при обработке строки {row}: {e}")
