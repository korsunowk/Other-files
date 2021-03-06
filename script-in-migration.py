# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations


def add_performance_agreements_to_old_applications(apps, schema_editor):
    application = apps.get_model('booking', 'Application')
    for app in application.objects.all():
        if not app.performance_agreement:
            app.performance_agreement = app.venue.performance_agreement
            app.save()


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0036_application_performance_agreement'),
    ]

    operations = [
        migrations.RunPython(add_performance_agreements_to_old_applications),
    ]



# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


def update_timeout_on_venue(apps, schema_editor):
    venue_model = apps.get_model('venue', 'Venue')
    for venue in venue_model.objects.all():
        if venue.timeout_period == 2:
            venue.timeout_period = 1
        elif venue.timeout_period in range(4, 7):
            venue.timeout_period = 3
        elif venue.timeout_period in range(8, 14):
            venue.timeout_period = 7
        elif venue.timeout_period > 14:
            venue.timeout_period = 14

        venue.save()


class Migration(migrations.Migration):

    dependencies = [
        ('venue', '0030_venue_standart_booking_window'),
    ]

    operations = [
        migrations.RunPython(update_timeout_on_venue),
    ]

