import os
import re
from phonenumber_field.modelfields import PhoneNumberField
from transliterate import translit
from PIL import Image, ImageOps

from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError

from django.db import models

from esg_shop import settings


VALID_EXTENSIONS = [".jpg", ".jpeg", ".png", ".webp"]

def validate_image_extension(value):
    '''Для загрузки файлов определенного типа'''
    ext = os.path.splitext(value.name)[1].lower()
    valid_extensions = VALID_EXTENSIONS
    if ext not in valid_extensions:
        raise ValidationError(f"Недопустимое расширение файла: {ext}. Разрешены только {', '.join(valid_extensions)}.")


def resave_photos(instance):
    '''Обрабатывает фото при загрузке'''
    image_field1 = getattr(instance, 'photo_big')
    if image_field1 and os.path.exists(image_field1.path):
        ext = os.path.splitext(image_field1.name)[1].lower()  # расширение файла
        if ext in VALID_EXTENSIONS:
            try:
                img = Image.open(image_field1.path).convert("RGB")
                img_square1 = ImageOps.pad(img, (800, 800), color="white")
                img_square2 = ImageOps.pad(img, (300, 300), color="white")

                rub = instance.rubric.rubric.rubric_name
                count = ElectroProduct.objects.filter(code=instance.code).count()

                if rub == 'Электрика':
                    count = ElectroProduct.objects.filter(code=instance.code).count()
                    if count >= 2:
                        base_name = f'E{instance.code}_{instance.id}'
                    else:
                        base_name = f'E{instance.code}'
                elif rub == 'Сантехника':
                    count = SantehProduct.objects.filter(code=instance.code).count()
                    if count >= 2:
                        base_name = f'S{instance.code}_{instance.id}'
                    else:
                        base_name = f'S{instance.code}'
                elif rub == 'Газификация':
                    count = GasProduct.objects.filter(code=instance.code).count()
                    if count >= 2:
                        base_name = f'G{instance.code}_{instance.id}'
                    else:
                        base_name = f'G{instance.code}'
                dir_name = os.path.dirname(image_field1.path)

                image_field1_path = os.path.join(dir_name, "800_" + base_name + ".webp")
                image_field2_path = os.path.join(dir_name, "300_" + base_name + ".webp")

                img_square1.save(image_field1_path, format="WEBP", quality=95)
                img_square2.save(image_field2_path, format="WEBP", quality=95)

                os.remove(image_field1.path)

                instance.photo_big.name = os.path.relpath(image_field1_path, settings.MEDIA_ROOT)
                instance.photo.name = os.path.relpath(image_field2_path, settings.MEDIA_ROOT)

            except Exception as e:
                print(f"Ошибка при обработке {image_field1.path}: {e}")


class Rubric(models.Model):
    '''
    Название основных разделов.
    Газификация, сантехника, электрика.
    '''
    rubric_name = models.CharField(max_length=50, unique=True, verbose_name='Название раздела')
    name_translit = models.CharField(max_length=100, unique=True, verbose_name='Название латиницей')

    class Meta:
        verbose_name_plural = 'Разделы'
        verbose_name = 'Раздел'
        ordering= ['-rubric_name']

    def __str__(self):
        return self.rubric_name

    def save(self, *args, **kwargs):
        '''Переопределяем для автоматической транслитерации.'''
        transliterated_nam = translit(self.rubric_name.lower(), 'ru', reversed=True)
        cleaned_name = re.sub(r'[^\w\s\-]+', "", transliterated_nam)
        translist = re.split(r'\s+', cleaned_name)
        translit_sp = [word for word in translist if word]
        transliterated_name = ('-').join(translit_sp)
        if not self.pk:
            super().save(*args, **kwargs)
        if Rubric.objects.exclude(pk=self.pk).filter(name_translit=transliterated_name).exists():
            self.name_translit = transliterated_name + f'{self.pk}'
        else:
            self.name_translit = transliterated_name
        super().save(update_fields=['name_translit'])


class Subrubric(models.Model):
    """
    Абстрактный класс для подразделов: сантехника, газификация, электрика.

    Определены атрибуты классов.
    Переопределен метод __save__ с учетом транслитерации.
    """

    title = models.CharField(max_length=255, unique=True, verbose_name='Подраздел')
    title_translit = models.CharField(max_length=255, unique=True, verbose_name='Название латиницей')
    rubric = models.ForeignKey(Rubric, on_delete=models.CASCADE, verbose_name='Раздел')

    class Meta:
        abstract = True

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        '''Переопределяем для автоматической транслитерации.'''
        transliterated_name = translit(self.title.lower(), 'ru', reversed=True)
        cleaned_name = re.sub(r'[^\w\s\-]+', "", transliterated_name)
        translist = re.split(r'\s+', cleaned_name)
        translit_sp = [word for word in translist if word]
        transliterated_title = ('-').join(translit_sp)
        if not self.pk:
            super().save(*args, **kwargs)
        qs = self.__class__.objects.exclude(pk=self.pk)
        if qs.filter(title_translit=transliterated_title).exists():
            self.title_translit = transliterated_title + f'{self.pk}'
        else:
            self.title_translit = transliterated_title
        super().save(update_fields=['title_translit'])


class Electro(Subrubric):
    '''Подразделы электрики.'''

    class Meta:
        verbose_name_plural = 'Раздел "Электрика"'
        verbose_name = 'Раздел "Электрика"'
        ordering= ['title']


class Gas(Subrubric):
    '''Подразделы газификации.'''

    class Meta:
        verbose_name_plural = 'Раздел "Газификация"'
        verbose_name = 'Раздел "Газификация"'
        ordering= ['title']


class Santeh(Subrubric):
    '''Подразделы сантехники.'''

    class Meta:
        verbose_name_plural = 'Раздел "Сантехника"'
        verbose_name = 'Раздел "Сантехника"'
        ordering= ['title']


class Product(models.Model):
    """
    Абстрактный класс для товаров следующих подразделов: сантехника, газификация, электрика.

    Определены некоторые атрибуты классов наследников.
    Переопределен метод __save__ с учетом транслитерации.
    """
    title = models.CharField(max_length=255, verbose_name='Наименование товара')
    title_translit = models.CharField(max_length=255, unique=True, verbose_name='Название латиницей')
    description = models.TextField(max_length=1000, null=True, blank=True, verbose_name='Описание товара')
    price = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    code = models.PositiveIntegerField(null=True, blank=True, verbose_name='Код наименования')
    status_popular = models.BooleanField(default=False, verbose_name='Популярный товар')
    status_new = models.BooleanField(default=False, verbose_name='Новинка')
    counter = models.PositiveIntegerField(verbose_name='Количество заказов', default=0)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        '''Переопределяем для автоматической транслитерации.'''
        transliterated_name = translit(self.title.lower(), 'ru', reversed=True)
        cleaned_name = re.sub(r',', "i", transliterated_name)
        cleaned_name = re.sub(r'µ', 'm', cleaned_name)
        cleaned_name = re.sub(r'[^\w\s\-]+', "", cleaned_name)
        translist = re.split(r'\s+', cleaned_name)
        translit_sp = [word for word in translist if word]
        transliterated_title = ('-').join(translit_sp)
        qs = self.__class__.objects.exclude(pk=self.pk)
        if qs.filter(title_translit=transliterated_title).exists():
            self.title_translit = transliterated_title + f'{self.code}'
        else:
            self.title_translit = transliterated_title
        super().save(*args, **kwargs)


# Товары подразделов электрики
class ElectroProduct(Product):
    '''Товары подразделов электрики.'''
    photo_big = models.ImageField(upload_to='electro/', validators=[validate_image_extension], null=True, blank=True, verbose_name='Фото товара на странице')
    photo = models.ImageField( upload_to='electro/', validators=[validate_image_extension], null=True, blank=True, verbose_name='Фото товара на карточке')
    rubric = models.ForeignKey(Electro, on_delete = models.CASCADE, verbose_name='Электрика')
    order = models.ManyToManyField('Order', verbose_name='Заказ', through='ElectroOrder')


    class Meta:
        verbose_name_plural = 'Товары раздела "Электрика"'
        verbose_name = 'Товар раздела"Электрика"'
        ordering= ['title']


# Товары подразделов газификации
class GasProduct(Product):
    '''Товары подразделов газификации.'''
    photo_big = models.ImageField(upload_to='gas/', validators=[validate_image_extension], null=True, blank=True, verbose_name='Фото товара на странице')
    photo = models.ImageField(upload_to='gas/', validators=[validate_image_extension], null=True, blank=True, verbose_name='Фото товара на карточке')
    rubric = models.ForeignKey(Gas, on_delete = models.CASCADE, verbose_name='Газификация')
    order = models.ManyToManyField('Order', verbose_name='Заказ', through='GasOrder')

    class Meta:
        verbose_name_plural = 'Товары раздела "Газификация"'
        verbose_name = 'Товар раздела "Газификация"'
        ordering= ['title']


class SantehProduct(Product):
    '''Товары подразделов сантехники.'''
    photo_big = models.ImageField(upload_to='santeh/', validators=[validate_image_extension], null=True, blank=True, verbose_name='Фото товара на странице')
    photo = models.ImageField(upload_to='santeh/', validators=[validate_image_extension], null=True, blank=True, verbose_name='Фото товара на карточке')
    rubric = models.ForeignKey(Santeh, on_delete = models.CASCADE, verbose_name='Сантехника')
    order = models.ManyToManyField('Order', verbose_name='Заказ', through='SantehOrder')

    class Meta:
        verbose_name_plural = 'Товары раздела "Сантехника"'
        verbose_name = 'Товар раздела "Сантехника"'
        ordering= ['title']


class Order(models.Model):
    '''Заказы. Содержат данные покупателя, общую стоимость и статус заказа.'''
    first_name = models.CharField(max_length=255, verbose_name='Имя',  validators =[RegexValidator(regex='^[A-Za-zА-Яа-яЁё]+$', message='Введите только буквы.', code='invalid_name')])
    last_name = models.CharField(max_length=255, verbose_name='Фамилия',  validators =[RegexValidator(regex='^[A-Za-zА-Яа-яЁё]+$', message='Введите только буквы.', code='invalid_name')])
    phone = PhoneNumberField(region='BY', verbose_name='Телефон (+375 ХХ ХХХХХХХ)')
    mail = models.EmailField(verbose_name='Электронная почта', null=True, blank=True, default='')
    date = models.DateTimeField(auto_now_add=True, verbose_name='Дата')
    status = models.BooleanField(default=False, verbose_name='Статус заказа')
    general_cost = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True, default=0)
    agreement = models.BooleanField(verbose_name='Я даю согласие на обработку персональных данных')

    class Meta:
        verbose_name_plural = 'Заказы'
        verbose_name = 'Заказ'
        ordering= ['date']

    def __str__(self):
        return f'{self.phone}, {self.date}'


class GasOrder(models.Model):
    '''
    Промежуточная таблица между заказами и товарами раздела "Газификация".
    Содержат информацию по количеству едниниц товара и общей стоимости каждого наименования.
    '''
    order = models.ForeignKey(Order, on_delete=models.CASCADE, verbose_name='Номер заказа')
    gasproduct = models.ForeignKey(GasProduct, on_delete=models.CASCADE, verbose_name='Номер товара')
    quantity = models.PositiveIntegerField(verbose_name='Количество')
    total_cost = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True, default=0)

class ElectroOrder(models.Model):
    '''
    Промежуточная таблица между заказами и товарами раздела "Электрика".
    Содержат информацию по количеству едниниц товара и общей стоимости каждого наименования.
    '''
    order = models.ForeignKey(Order, on_delete=models.CASCADE, verbose_name='Номер заказа')
    electroproduct = models.ForeignKey(ElectroProduct, on_delete=models.CASCADE, verbose_name='Номер товара')
    quantity = models.PositiveIntegerField(verbose_name='Количество')
    total_cost = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True, default=0)

class SantehOrder(models.Model):
    '''
    Промежуточная таблица между заказами и товарами раздела "Сантехника".
    Содержат информацию по количеству едниниц товара и общей стоимости каждого наименования.
    '''
    order = models.ForeignKey(Order, on_delete=models.CASCADE, verbose_name='Номер заказа')
    santehproduct = models.ForeignKey(SantehProduct, on_delete=models.CASCADE, verbose_name='Номер товара')
    quantity = models.PositiveIntegerField(verbose_name='Количество')
    total_cost = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True, default=0)


class Feedback(models.Model):
    '''Обратная связь от потребителей.'''
    name = models.CharField(max_length=50, verbose_name='Имя', validators =[RegexValidator(regex='^[A-Za-zА-Яа-яЁё]+$', message='Введите только буквы.', code='invalid_name')])
    phone = PhoneNumberField(region='BY', verbose_name='Телефон (+375 ХХ ХХХХХХХ)')
    subject = models.CharField(max_length=50, verbose_name='Тема', null=True, blank=True, default='')
    message = models.TextField(verbose_name='Ваше сообщение')
    date = models.DateTimeField(auto_now_add=True, verbose_name='Дата')
    status = models.BooleanField(default=False, verbose_name='Статус сообщения')
    agreement = models.BooleanField(verbose_name='Согласие на обработку персональных данных', default=False)

    class Meta:
        verbose_name_plural = 'Обратная связь'
        verbose_name = 'Обратная связь'
        ordering= ['date']

    def __str__(self):
        return f'{self.name}, {self.phone}, {self.date}'