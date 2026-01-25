from django.core.management.base import BaseCommand

from esg.documents import ElectroProductDocument, GasProductDocument, SantehProductDocument
from esg.models import ElectroProduct, GasProduct, SantehProduct


class Command(BaseCommand):
    '''Индексирует все продукты. '''

    def handle(self, *args, **kwargs):
        ElectroProductDocument.init()
        GasProductDocument.init()
        SantehProductDocument.init()

        for product in ElectroProduct.objects.all():
            ElectroProductDocument().update(product)

        for product in GasProduct.objects.all():
            GasProductDocument().update(product)

        for product in SantehProduct.objects.all():
            SantehProductDocument().update(product)