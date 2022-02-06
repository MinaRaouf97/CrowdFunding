from django import template

register = template.Library()

@register.filter(name='to_range')
def to_range(value):
    return [i for i in range(value)]

@register.filter(name='sub')
def sub(old, value):
    sub = old-value
    return sub

