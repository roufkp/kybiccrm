from django import template
from leads.models import Lead

register = template.Library()

@register.filter(name='get_category_count')
def get_category_count(category, leads):
    return leads.filter(category=category).count()
