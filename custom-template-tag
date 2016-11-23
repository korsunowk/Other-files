from sonum import settings
from django import template

register = template.Library()


@register.assignment_tag
def is_subscribed_user(user):
    try:
        data = dict()
        data['key'] = settings.STRIPE_KEYS['public']
        data['amount'] = settings.STRIPE_PLAN['amount']
        data['email'] = user.email
        if user.venue and user.venue.subscribed:
            return True, data
        return False, data
    except:
        return True,




from django import template
from venue.models import Venue

register = template.Library()


@register.simple_tag
def get_unread_message(user, application):
    try:
        return application.venue_unread_messages \
            if Venue.objects.filter(user=user).exists() else application.band_unread_messages
    except Exception as e:
        print(e)
        return False


{% load get_unread_message %}
{% get_unread_message request.user application as unread %}
{% if unread %}
...
{% endif %}
