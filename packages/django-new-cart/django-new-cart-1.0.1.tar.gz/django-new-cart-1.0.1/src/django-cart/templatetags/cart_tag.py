from hashlib import md5
from django import template
from ..cart import Cart
register = template.Library()


@register.filter()
def multiply(value, arg):
    return float(value) * float(arg)

@register.filter()
def get_sum_of(cart: Cart, key):
    return sum(map(lambda x: float(x[key]), cart.all()))

@register.filter()
def paginate(array: list, amount: int):
    return range(0, len(array), amount)

@register.filter()
def week_to_str(isoweek: int):
    if isoweek == 0:
        return "Mon"
    elif isoweek == 1:
        return "Tue"
    elif isoweek == 2:
        return "Wed"
    elif isoweek == 3:
        return "Thu"
    elif isoweek == 4:
        return "Fri"
    elif isoweek == 5:
        return "Sat"
    elif isoweek == 6:
        return "Sun"

@register.filter
def str_md5(value:str):
    return md5(value.encode()).hexdigest()

@register.filter()
def get_values(data: dict, key: str):
    return data[key]

@register.filter()
def firsts(array: list, amount: int):
    return array[:amount]

@register.filter()
def lasts(array: list, amount: int):
    return array[-amount:]