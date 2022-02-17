from django import template
from django.db.models import *

from firstapp.models import Category, News

register = template.Library()

@register.simple_tag()
def find_category():
    allCategories = Category.objects.all()
    categories = Category.objects.annotate(cnt=Count('news')).filter(cnt__gt=0)
    return categories

@register.inclusion_tag('firstapp/list_categories.html')
def show_categories():
    categories = Category.objects.all()

    return {"categories":categories}
    