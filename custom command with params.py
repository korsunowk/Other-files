from django.core.management import BaseCommand
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils import timezone

from sonum import settings
from venue.models import Venue
from band.models import Band

from datetime import timedelta


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument(
            '--minutes',
            action='store',
            dest='Minutes',
            default=15,
        )

    def handle(self, *args, **options):
        emails = list()
        for venue in Venue.objects.all():
            for app in venue.applications.all():
                if app.messages.filter(date__range=(timezone.now() - timedelta(minutes=int(options['Minutes'])),
                                                    timezone.now()), is_read=False, author=app.band.user).count():
                    html_content = render_to_string('booking/email/venue/5a-band-has-sent-you-a-message.html',
                                                    {
                                                        'application': app,
                                                        'link': "{}{}".format(settings.DOMAIN,
                                                                              reverse('venue:application_inprogress'))
                                                    })
                    emails.append(
                        {
                            'subject': '%s Has Sent You a Message' %
                                       app.band.primary_contact_name if app.band.primary_contact_name
                            else app.band.name, 'html_content': html_content,
                            'recipient': [one_email.email for one_email in app.venue.emails.all()]
                        }
                    )
        for band in Band.objects.all():
            for app in band.applications.all():
                if app.messages.filter(date__range=(timezone.now() - timedelta(minutes=int(options['Minutes'])),
                                                    timezone.now()), is_read=False, author=app.venue.user).count():
                    html_content = render_to_string('booking/email/band/5a-venue-has-sent-you-a-message.html',
                                                    {
                                                        'application': app,
                                                        'link': "{}{}".format(settings.DOMAIN,
                                                                              reverse('band:application_inprogress'))
                                                    })
                    emails.append(
                        {
                            'subject': '%s Has Sent You a Message' %
                                       app.venue.name,
                            'html_content': html_content,
                            'recipient': [app.band.email]
                        }
                    )
        for email in emails:
            send_mail(
                subject=email['subject'],
                message=email['html_content'],
                from_email=settings.EMAIL_FROM,
                fail_silently=False,
                html_message=email['html_content'],
                recipient_list=email['recipient']
            )
