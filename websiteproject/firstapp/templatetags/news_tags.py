from django import template

from firstapp.models import Category

register = template.Library()

@register.simple_tag()
def find_category():
    return Category.objects.all()