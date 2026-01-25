import os

from django.core.management import BaseCommand
from django.db import transaction
from esg.models import GasProduct, ElectroProduct, SantehProduct
from esg_shop import settings

# out_folder = os.path.join(settings.BASE_DIR, "media_clear", "electro")
# out_folder = os.path.join(settings.BASE_DIR, "media_clear", "gas")
out_folder = os.path.join(settings.BASE_DIR, "media_clear", "santeh")

class Command(BaseCommand):
    '''Загружает картинки в базу'''
    def handle(self, *args, **options):

        # # для електропродуктов
        # with transaction.atomic():
        #     for image in os.listdir(out_folder):
        #         try:
        #             code_image = os.path.splitext(image)[0]
        #             product = ElectroProduct.objects.get(code=code_image[5:])
        #             if code_image[:3] == '300':
        #                 product.photo.name = f"electro/{image}"
        #                 product.save(update_fields=["photo"])
        #             elif code_image[:3] == '800':
        #                 product.photo_big.name = f"electro/{image}"
        #                 product.save(update_fields=["photo_big"])
        #
        #         except ElectroProduct.DoesNotExist:
        #             print(f"❌ Продукт с кодом {code_image} не найден")
        #         except Exception as e:
        #             print(f"⚠️ Ошибка при обработке {image}: {e}")
        #             raise

        # # для продуктов газификации
        # with transaction.atomic():
        #     for image in os.listdir(out_folder):
        #         try:
        #             code_image = os.path.splitext(image)[0]
        #             product = GasProduct.objects.get(code=code_image[5:])
        #             if code_image[:3] == '300':
        #                 product.photo.name = f"gas/{image}"
        #                 product.save(update_fields=["photo"])
        #             elif code_image[:3] == '800':
        #                 product.photo_big.name = f"gas/{image}"
        #                 product.save(update_fields=["photo_big"])
        #
        #         except GasProduct.DoesNotExist:
        #             print(f"❌ Продукт с кодом {code_image} не найден")
        #         except Exception as e:
        #             print(f"⚠️ Ошибка при обработке {image}: {e}")
        #             raise


        # для сантехпродуктов
        with transaction.atomic():
            for image in os.listdir(out_folder):
                try:
                    code_image = os.path.splitext(image)[0]
                    product = SantehProduct.objects.get(code=code_image[5:])
                    if code_image[:3] == '300':
                        product.photo.name = f"santeh/{image}"
                        product.save(update_fields=["photo"])
                    elif code_image[:3] == '800':
                        product.photo_big.name = f"santeh/{image}"
                        product.save(update_fields=["photo_big"])

                except SantehProduct.DoesNotExist:
                    print(f"❌ Продукт с кодом {code_image} не найден")
                except Exception as e:
                    print(f"⚠️ Ошибка при обработке {image}: {e}")
                    raise