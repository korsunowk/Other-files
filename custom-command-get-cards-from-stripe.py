from django.core.management import BaseCommand

from venue.models import Venue
from sonum import settings

import stripe


class Command(BaseCommand):

    def handle(self, *args, **options):
        for venue in Venue.objects.filter(subscription__contains='cus_'):
            if not venue.cards.exists():
                venue_customer = stripe.Customer.retrieve(api_key=settings.STRIPE_KEYS['secret'],
                                                          id=venue.subscription)
                for card in venue_customer.sources:
                    venue.cards.create(
                        card_id=card['id'],
                        card_country=card['country'],
                        last_4=card['last4'],
                        card_brand=card['brand'],
                        active=True if venue_customer.default_source == card['id'] else False
                    )
