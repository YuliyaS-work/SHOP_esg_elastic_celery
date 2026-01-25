from celery import shared_task
from decouple import config

from django.core.mail import send_mail

from ..models import Order, GasProduct, ElectroProduct, SantehProduct, GasOrder, ElectroOrder, SantehOrder
import esg_shop


@shared_task
def process_order_task(order_id, basket_cookies):
    order = Order.objects.get(pk=order_id)
    list_order = []
    cost = 0.00

    for title, value in basket_cookies.items():
        if title == "generalCost":
            order.general_cost = float(value)
            cost = float(value)
            order.save()
        elif GasProduct.objects.filter(title=title).exists():
            product = GasProduct.objects.get(title=title)
            product.counter += 1
            product.save(update_fields=['counter'])
            GasOrder.objects.create(order=order, gasproduct=product, quantity=value[0], total_cost=float(value[1]))
            list_order.append(f'{product.title} - {value[0]}шт./м, стоимость {value[1]} BYN')
        elif ElectroProduct.objects.filter(title=title).exists():
            product = ElectroProduct.objects.get(title=title)
            product.counter += 1
            product.save(update_fields=['counter'])
            ElectroOrder.objects.create(order=order, electroproduct=product, quantity=value[0], total_cost=float(value[1]))
            list_order.append(f'{product.title} - {value[0]}шт./м, стоимость {value[1]} BYN')
        elif SantehProduct.objects.filter(title=title).exists():
            product = SantehProduct.objects.get(title=title)
            product.counter += 1
            product.save(update_fields=['counter'])
            SantehOrder.objects.create(order=order, santehproduct=product, quantity=value[0], total_cost=float(value[1]))
            list_order.append(f'{product.title} - {value[0]}шт./м, стоимость {value[1]} BYN')

    # for a seller
    subject = f'Новый заказ № {order.pk}'
    message = (
            f'Заказ № {order.pk} на имя {order.first_name} {order.last_name} ({order.phone}).\n' +
            f'Товары: \n' + '\n'.join(list_order)+ '\n' +
            f'Общая стоимость: {cost} BYN'
    )
    to_email = [config('EMAIL_HOST_USER'), 'Spelbtorg@mail.ru']

    # for a client
    subject1 = f'Магазин "Электротовары"'
    message1 = (f'{order.first_name}, номер Вашего заказа {order.pk}.')

    try:
        # email to a seller
        send_mail(
            subject=subject,
            message=message,
            from_email=esg_shop.settings.DEFAULT_FROM_EMAIL,
            recipient_list=to_email,
            fail_silently=False,
        )
        # email to a client
        if order.mail and order.mail.strip():
            clean_email = order.mail.strip()
            send_mail(
                subject=subject1,
                message=message1,
                from_email=esg_shop.settings.DEFAULT_FROM_EMAIL,
                recipient_list=[clean_email],
                fail_silently=False,
            )
    except Exception as e:
        print(f' Письмо не отправлено: {e}')
