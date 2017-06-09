from django.test import TestCase, Client
from django.contrib.auth.models import User
from venue.models import Venue
from booking.models import Application
from band.models import Band
from booking.templatetags.get_new_applications_counter import get_new_applications_counter

import re
# Create your tests here.


class GetApplicationCounterTest(TestCase):
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
            picture="qerg"
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
            picture="qerg"
        )

    def test_counter(self):
        for i in range(5):
            Application.objects.create(
                venue=self.venue,
                band=self.band,
                status=Application.STATUS_VENUE_CREATED_APPLICATION,
                is_venue_invited=True
            )

        self.client.post('/accounts/login/', {'username': self.user_band.username, 'password': 'password'})
        for find in re.findall(u'<span class="sidebar-newApplications total">[^<]+<',
                               self.client.get('/band/dashboard/open/').content.decode("utf-8")):
            self.assertEqual(Application.objects.count(), int(find[:-1].split('>')[-1]),
                             get_new_applications_counter(self.user_venue, status="open")[1])

        self.client.get('/accounts/logout')
        self.client.post('/accounts/login', {'username': self.user_venue.username, 'password': 'password'})
        for find in re.findall(u'<span class="sidebar-newApplications total">[^<]+<',
                               self.client.get('/venue/dashboard/sent/').content.decode("utf-8")):
            self.assertEqual(Application.objects.count(), int(find[:-1].split('>')[-1]),
                             get_new_applications_counter(self.user_venue, status="sent")[0])
        for app in Application.objects.all():
            app.status = Application.STATUS_CONFIRMED
            app.save()

        for find in re.findall(u'<span class="sidebar-newApplications total">[^<]+<',
                               self.client.get('/venue/dashboard/upcoming/').content.decode("utf-8")):
            self.assertEqual(Application.objects.count(), int(find[:-1].split('>')[-1]),
                             get_new_applications_counter(self.user_venue, status="booked_upcoming")[0])
        self.client.get('/accounts/logout')
        self.client.post('/accounts/login', {'username': self.user_band.username, 'password': 'password'})

        for find in re.findall(u'<span class="sidebar-newApplications total">[^<]+<',
                               self.client.get('/band/dashboard/upcoming/').content.decode("utf-8")):
            self.assertEqual(Application.objects.count(), int(find[:-1].split('>')[-1]),
                             get_new_applications_counter(self.user_venue, status="booked_upcoming")[1])
        for app in Application.objects.all():
            app.delete()

        for i in range(3):
            Application.objects.create(
                venue=self.venue,
                band=self.band,
                status=Application.STATUS_BAND_SENT_APPLICATION_TO_VENUE,
            )

        for find in re.findall(u'<span class="sidebar-newApplications total">[^<]+<',
                               self.client.get('/band/dashboard/sent/').content.decode("utf-8")):
            self.assertEqual(Application.objects.count(), int(find[:-1].split('>')[-1]),
                             get_new_applications_counter(self.user_venue, status="sent")[1])

        for app in Application.objects.all():
            app.status = Application.STATUS_BAND_CONFIRMED
            app.save()

        for find in re.findall(u'<span class="sidebar-newApplications total">[^<]+<',
                               self.client.get('/band/dashboard/in-progress/').content.decode("utf-8")):
            self.assertEqual(Application.objects.count(), int(find[:-1].split('>')[-1]),
                             get_new_applications_counter(self.user_venue, status="inprogress")[1])

        self.client.get('/accounts/logout')
        self.client.post('/accounts/login', {'username': self.user_venue.username, 'password': 'password'})
        for find in re.findall(u'<span class="sidebar-newApplications total">[^<]+<',
                               self.client.get('/venue/dashboard/in-progress/').content.decode("utf-8")):
            self.assertEqual(Application.objects.count(), int(find[:-1].split('>')[-1]),
                             get_new_applications_counter(self.user_venue, status="inprogress")[0])
