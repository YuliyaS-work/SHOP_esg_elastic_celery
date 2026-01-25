import re

from django.core.management import BaseCommand
from transliterate import translit

from esg.models import *


class Command(BaseCommand):
    '''
    Транслитерация русских названий.
    В моделях прописаны методы транслитерации при создании нового экземпляра.
    Данный скрипт подходит при необходимости транслитерации или перетранслитерации.
    '''
    def handle(self, *args, **options):
        rubrics = Rubric.objects.all()
        for rubric in rubrics:
            transliterated_name = translit(rubric.rubric_name.lower(), 'ru', reversed=True)
            rubric.name_translit = transliterated_name
            rubric.save(update_fields=['name_translit'])

        electro = Electro.objects.all()
        for rubric in electro:
            transliterated_name = translit(rubric.title.lower(), 'ru', reversed=True)
            cleaned_name = re.sub(r'[^\w\s\-]+', "", transliterated_name)
            translist = re.split(r'\s*,\s*|\s+i\s+|\s+dlja\s+|\s+' , cleaned_name)
            translit_sp = [word for word in translist if word]
            transliterated_title = ('-').join(translit_sp)
            rubric.title_translit = transliterated_title
            rubric.save(update_fields=['title_translit'])

        gas = Gas.objects.all()
        for rubric in gas:
            transliterated_name = translit(rubric.title.lower(), 'ru', reversed=True)
            cleaned_name = re.sub(r'[^\w\s\-]+', "", transliterated_name)
            translist = re.split(r'\s*,\s*|\s+i\s+|\s+dlja\s+|\s+', cleaned_name)
            translit_sp = [word for word in translist if word]
            transliterated_title = ('-').join(translit_sp)
            rubric.title_translit = transliterated_title
            rubric.save(update_fields=['title_translit'])

        santeh = Santeh.objects.all()
        for rubric in santeh:
            transliterated_name = translit(rubric.title.lower(), 'ru', reversed=True)
            cleaned_name = re.sub(r'[^\w\s\-]+', "", transliterated_name)
            translist = re.split(r'\s*,\s*|\s+i\s+|\s+dlja\s+|\s+', cleaned_name)
            translit_sp = [word for word in translist if word]
            transliterated_title = ('-').join(translit_sp)
            rubric.title_translit = transliterated_title
            rubric.save(update_fields=['title_translit'])

        electroproducts = ElectroProduct.objects.all()
        for product in electroproducts:
            transliterated_name = translit(product.title.lower(), 'ru', reversed=True)
            cleaned_name = re.sub(r',', "i", transliterated_name)
            cleaned_name = re.sub(r'[^\w\s\-]+', "", cleaned_name)
            translist = re.split(r'\s*,\s*|\s+', cleaned_name)
            translit_sp = [word for word in translist if word]
            transliterated_title = ('-').join(translit_sp)
            if ElectroProduct.objects.filter(title_translit=transliterated_title).exists():
                transliterated_title_code = transliterated_title + f'{product.code}'
                product.title_translit = transliterated_title_code
                product.save(update_fields=['title_translit'])
            else:
                product.title_translit = transliterated_title
                product.save(update_fields=['title_translit'])

        gasproducts = GasProduct.objects.all()
        for product in gasproducts:
            transliterated_name = translit(product.title.lower(), 'ru', reversed=True)
            cleaned_name = re.sub(r',', "i", transliterated_name)
            cleaned_name = re.sub(r'[^\w\s\-]+', "", cleaned_name)
            translist = re.split(r'\s*,\s*|\s+', cleaned_name)
            translit_sp = [word for word in translist if word]
            transliterated_title = ('-').join(translit_sp)
            if GasProduct.objects.filter(title_translit=transliterated_title).exists():
                transliterated_title_code = transliterated_title + f'{product.code}'
                product.title_translit = transliterated_title_code
                product.save(update_fields=['title_translit'])
            else:
                product.title_translit = transliterated_title
                product.save(update_fields=['title_translit'])

        santehproducts = SantehProduct.objects.all()
        for product in santehproducts:
            transliterated_name = translit(product.title.lower(), 'ru', reversed=True)
            cleaned_name = re.sub(r',', "i", transliterated_name)
            cleaned_name = re.sub(r'[^\w\s\-]+', "", cleaned_name)
            translist = re.split(r'\s*,\s*|\s+', cleaned_name)
            translit_sp = [word for word in translist if word]
            transliterated_title = ('-').join(translit_sp)
            if SantehProduct.objects.filter(title_translit=transliterated_title).exists():
                transliterated_title_code = transliterated_title + f'{product.code}'
                product.title_translit = transliterated_title_code
                product.save(update_fields=['title_translit'])
            else:
                product.title_translit = transliterated_title
                product.save(update_fields=['title_translit'])
