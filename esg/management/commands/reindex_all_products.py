from elasticsearch import Elasticsearch

from django.core.management.base import BaseCommand

from esg.documents import ElectroProductDocument, GasProductDocument, SantehProductDocument
from esg.models import ElectroProduct, GasProduct, SantehProduct


class Command(BaseCommand):
    '''Удаляет и пересоздаёт все индексы, затем индексирует данные. '''

    def handle(self, *args, **options):
        es = Elasticsearch(
            hosts=["ELASTICSEARCH_HOST"],
            basic_auth=("ELASTICSEARCH_USER", "ELASTICSEARCH_PASSWORD"),
            verify_certs=False
        )

        # Удаление старых индексов
        for index_name in ["electroproducts", "gasproducts", "santehproducts"]:
            if es.indices.exists(index=index_name):
                es.indices.delete(index=index_name)
                self.stdout.write(self.style.WARNING(f"Удалён индекс: {index_name}"))
            else:
                self.stdout.write(f"Индекс {index_name} не найден — пропущено")

        # Инициализация новых индексов
        ElectroProductDocument.init()
        GasProductDocument.init()
        SantehProductDocument.init()
        self.stdout.write(self.style.SUCCESS("Индексы пересозданы"))

        # Индексация данных
        for product in ElectroProduct.objects.all():
            ElectroProductDocument().update(product)
        for product in GasProduct.objects.all():
            GasProductDocument().update(product)
        for product in SantehProduct.objects.all():
            SantehProductDocument().update(product)

        self.stdout.write(self.style.SUCCESS("Все данные успешно проиндексированы"))
