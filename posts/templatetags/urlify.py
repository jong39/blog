# from urllib import quote_plus
from django import template

register = template.Library()

@register.filter
def urlify(value):
	new_str = value.replace( ' ', '+')
	return new_str