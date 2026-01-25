from celery import shared_task
from decouple import config

from django.core.mail import send_mail

from ..models import Feedback
import esg_shop


@shared_task
def process_feedback_task(feedback_id):
    feedback = Feedback.objects.get(pk=feedback_id)
    subject = f'Обратная связь № {feedback.pk}'
    message_subject_from_client = f'\nТема: \n' + f'{feedback.subject}' if feedback.subject else ''
    message = (f'Обратная связь № {feedback.pk} от {feedback.name} ({feedback.phone}).' +
               f'{message_subject_from_client}\n' +
               f'Сообщение: \n' + f'{feedback.message}'
    )
    to_email = [config('EMAIL_HOST_USER'), 'Spelbtorg@mail.ru']
    try:
        send_mail(
            subject=subject,
            message=message,
            from_email=esg_shop.settings.DEFAULT_FROM_EMAIL,
            recipient_list=to_email,
            fail_silently=False,
        )
    except Exception as e:
        print(f'❌ Письмо не отправлено: {e}')