from django.dispatch import receiver
from django.db.models.signals import post_save
from booking.models import Invite
from django.core.mail import send_mail
from django.template.loader import render_to_string
from sonum import settings


@receiver(post_save, sender=Invite)
def send_invite_email(sender, instance, created, *args, **kwargs):
    if created:
        message = render_to_string('booking/email/venue/invite-non-register-band-to-neon-music.html',
                                   context=dict(
                                       invite=instance,
                                       link='%s' % settings.DOMAIN
                                   ))
        send_mail(
            subject='You\'re invited to join Neon Music!',
            message=message,
            from_email=settings.EMAIL_FROM,
            recipient_list=[instance.email],
            fail_silently=False,
            html_message=message

        )
