from django import template
from blog.models import Review

register = template.Library()


@register.simple_tag(takes_context=True)
def get_poster_display(context, user):
    """
    This function returns a personalized message based on the user.
    If the user is the same as the current user, returns "you".
    Otherwise, returns the username.

    Args:
        context: The context of the template.
        user: The user whose name we want to display.

    Returns:
        str: The personalized message for the user.
    """
    if user == context["user"]:
        return "vous"
    return user.username


@register.filter
def range_filter(value):
    """
    This filter creates a range of numbers from 1 to the given value.

    Args:
        value: The maximum value of the range.

    Returns:
        range: A range of numbers from 1 to the given value.
    """
    return range(1, value + 1)


@register.simple_tag(takes_context=True)
def is_ticket_already_reviewed(context, ticket):
    """
    Checks if a user has already written a review for a given ticket.
    Returns True if a review exists, otherwise False.

    Args:
        context: The context of the template.
        ticket: The ticket for which we want to check if a review exists.

    Returns:
        bool: True if a review exists, otherwise False.
    """
    user = context["user"]

    return Review.objects.filter(ticket=ticket, user=user).exists()
