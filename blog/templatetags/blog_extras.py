from django import template

register = template.Library()


@register.simple_tag(takes_context=True)
def get_poster_display(context, user):
    if user == context['user']:
        return 'vous'
    return user.username


@register.filter
def range_filter(value):
    return range(1, value + 1)