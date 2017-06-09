from django.test import TestCase, Client
from django.contrib.auth.models import User
from venue.models import Venue
from booking.models import Application
from band.models import Band
from django.utils import timezone


# Create your tests here.


class ChangeApplicationStatusTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user_venue = User.objects.create_user(
            username="username",
            password="password",
            email="email@email.ua",
            is_active=True
        )
        self.venue = Venue.objects.create(
            user=self.user_venue,
            name="venue",
            average_hourly_rate=51,
            picture="picture"
        )
        self.user_band = User.objects.create_user(
            username="band",
            password="password",
            email="email@email.com",
            is_active=True
        )
        self.band = Band.objects.create(
            user=self.user_band,
            name="band",
            average_hourly_rate=500,
            about="qergqe",
            mile_radius_willing_to_travel=3,
            picture="picture"
        )

    def test_change_status(self):
        app = Application.objects.create(
            venue=self.venue,
            band=self.band,
            status=Application.STATUS_BAND_SENT_APPLICATION_TO_VENUE,
            is_venue_invited=True,
            performance_agreement="Test agreements."
        )
        login_url, logout_url = '/accounts/login/', '/accounts/logout/'
        self.client.post(login_url, {'username': self.user_band.username, 'password': 'password'})
        self.client.post('/applicationMoveToInprogress/%s/' % app.pk)
        app = Application.objects.get(id=app.id)
        self.assertTrue(app.is_active)

        self.client.post(logout_url)
        self.client.post(login_url, {'username': self.user_venue.username, 'password': 'password'})
        app.dates.create(
            date=timezone.datetime.now()
        )
        self.venue.default_payments.create(
            kind=1,
            value=515
        )
        self.venue.default_payments.create(
            kind=2,
            value=500,
            total=50000
        )
        self.client.post('/applications/use_default/payments/%s/' % app.pk)
        self.client.post('/venue/dashboard/application/%s/status/' % app.pk,
                         {'status': Application.STATUS_VENUE_ACCEPTED_APPLICATION})
        app = Application.objects.get(id=app.id)
        self.assertTrue(app.is_use_default_payment_details)
        self.assertEqual(app.status, Application.STATUS_VENUE_ACCEPTED_APPLICATION)
        self.assertEqual(app.get_venue_application_stages()[0]['status'], 'Waiting on Band Response')
        app.messages.create(
            text='Hello, this is test!',
            author=self.user_band,
            is_read=True
        )
        self.assertEqual(app.get_venue_application_stages()[0]['status'], 'Band Responded')
