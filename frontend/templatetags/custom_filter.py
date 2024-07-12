# templatetags/custom_filters.py
from django import template

register = template.Library()

@register.filter
def subtract_one(value):
    return value - 1

@register.filter
def divisible_by_3(value):
    if ((value%3) == 0):
        return True
    return False
@register.filter
def divisible_by_3_g4(value):
    if ((value-1)%3 == 0) and ((value-1)>3):
        return True
    return False

@register.filter(name='is_digit')
def is_digit(value):
    return value.isdigit()

@register.filter
def eval_val(value):
    return eval(value)

@register.filter
def con_int(value):
    return (int(value))

@register.filter
def custom_range(value):
    return range(value)


@register.filter
def add_one(value):
    return (int(value)+1)

@register.filter
def multiply(value, arg):
    return value * arg

@register.filter
def grt_then(value, arg):
    return (value>arg)


