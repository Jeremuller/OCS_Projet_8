from django import template
from blog.models import Review

register = template.Library()


@register.simple_tag(takes_context=True)
def get_poster_display(context, user):
    if user == context["user"]:
        return "vous"
    return user.username


@register.filter
def range_filter(value):
    return range(1, value + 1)


@register.simple_tag(takes_context=True)
def is_ticket_already_reviewed(context, ticket):
    """
    Vérifie si un utilisateur a déjà rédigé une critique pour un ticket donné.
    Renvoie True si une critique existe, sinon False.

    """
    user = context["user"]

    return Review.objects.filter(ticket=ticket, user=user).exists()
