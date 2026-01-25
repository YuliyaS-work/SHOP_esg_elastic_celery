from django_elasticsearch_dsl import Document, Index, fields
from django_elasticsearch_dsl.registries import registry

from .models import ElectroProduct, GasProduct, SantehProduct


@registry.register_document
class ElectroProductDocument(Document):
    class Index:
        name = 'electroproducts'

    class Django:
        model = ElectroProduct
        fields = ['title', 'description']


@registry.register_document
class GasProductDocument(Document):
    class Index:
        name = 'gasproducts'

    class Django:
        model = GasProduct
        fields = ['title', 'description']



@registry.register_document
class SantehProductDocument(Document):
    class Index:
        name = 'santehproducts'

    class Django:
        model = SantehProduct
        fields = ['title', 'description']


