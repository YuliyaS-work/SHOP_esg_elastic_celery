import os
from django.db.models.signals import pre_save, post_delete, post_save
from django.dispatch import receiver
from .models import ElectroProduct, SantehProduct, GasProduct, resave_photos

MODELS = (ElectroProduct, SantehProduct, GasProduct)

def _delete_file(field):
    """Удаляет файл с диска, если он существует."""
    try:
        if field and field.path and os.path.isfile(field.path):
            os.remove(field.path)
    except Exception:
        pass


@receiver(pre_save)
def delete_old_files_on_change(sender, instance, **kwargs):
    """Удаляет старые файлы при замене photo_big/photo."""
    if sender not in MODELS or not instance.pk:
        return

    try:
        old_instance = sender.objects.get(pk=instance.pk)
    except sender.DoesNotExist:
        return

        # если photo_big было, а теперь очищено
    if old_instance.photo_big and not instance.photo_big:
        _delete_file(old_instance.photo_big)
        _delete_file(old_instance.photo)
        instance.photo = None  # очистим поле в базе

    # если заменили photo_big
    elif old_instance.photo_big and old_instance.photo_big != instance.photo_big:
        _delete_file(old_instance.photo_big)
        _delete_file(old_instance.photo)

@receiver(post_save, sender=ElectroProduct)
@receiver(post_save, sender=SantehProduct)
@receiver(post_save, sender=GasProduct)
def process_photos_after_save(sender, instance, created, **kwargs):
    if instance.photo_big:
        resave_photos(instance)
        sender.objects.filter(pk=instance.pk).update(
            photo_big=instance.photo_big.name,
            photo=instance.photo.name
        )


@receiver(post_delete, sender=ElectroProduct)
@receiver(post_delete, sender=SantehProduct)
@receiver(post_delete, sender=GasProduct)
def delete_related_photos(sender, instance, **kwargs):
    """Удаляет файлы при удалении объекта."""
    _delete_file(instance.photo_big)
    _delete_file(instance.photo)
