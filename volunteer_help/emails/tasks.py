from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags


@shared_task
def send_response_notification_task(needy_email, needy_name, task_title, volunteer_name, volunteer_rating,
                                    volunteer_email, task_id):
    """Асинхронная отправка уведомления о новом отклике"""
    subject = f'Новый отклик на заявку "{task_title}"'

    context = {
        'needy_name': needy_name,
        'task_title': task_title,
        'volunteer_name': volunteer_name,
        'volunteer_rating': volunteer_rating,
        'volunteer_email': volunteer_email,
        'site_url': 'http://127.0.0.1:8000',
        'task_id': task_id,
    }

    html_content = render_to_string('email/response_notification.html', context)
    text_content = strip_tags(html_content)

    send_mail(
        subject=subject,
        message=text_content,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[needy_email],
        html_message=html_content,
        fail_silently=False,
    )


@shared_task
def send_accept_notification_task(volunteer_email, volunteer_name, task_title, task_address, needy_name, needy_email,
                                  task_id):
    """Асинхронная отправка уведомления о принятом отклике"""
    subject = f'Ваш отклик принят! "{task_title}"'

    context = {
        'volunteer_name': volunteer_name,
        'task_title': task_title,
        'task_address': task_address,
        'needy_name': needy_name,
        'needy_email': needy_email,
        'site_url': 'http://127.0.0.1:80',
        'task_id': task_id,
    }

    html_content = render_to_string('email/accept_notification.html', context)
    text_content = strip_tags(html_content)

    send_mail(
        subject=subject,
        message=text_content,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[volunteer_email],
        html_message=html_content,
        fail_silently=False,
    )


@shared_task
def send_completion_notification_task(needy_email, needy_name, task_title, volunteer_name, task_id):
    """Уведомление нуждающемуся, что волонтёр отметил выполнение"""
    subject = f'Волонтёр завершил вашу задачу "{task_title}"'

    html_content = f"""
    <h3>Здравствуйте, {needy_name}!</h3>
    <p>Волонтёр <strong>{volunteer_name}</strong> отметил, что выполнил вашу задачу.</p>
    <p>Пожалуйста, подтвердите выполнение или отклоните его.</p>
    <p><a href="http://127.0.0.1:8000/my-tasks/">Перейти к задачам</a></p>
    """

    send_mail(
        subject=subject,
        message=strip_tags(html_content),
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[needy_email],
        html_message=html_content,
        fail_silently=False,
    )