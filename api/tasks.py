from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings

@shared_task
def send_order_update_email(order_id, user_email, status):
    subject = f"Order #{order_id} Status Update"
    message = f"Hi! Your order #{order_id} status has changed to '{status}'."
    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [user_email],
        fail_silently=False,
    )
