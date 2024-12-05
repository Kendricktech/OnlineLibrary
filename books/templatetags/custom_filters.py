# In yourapp/templatetags/custom_filters.py
from django import template

register = template.Library()

@register.filter
def get_model_name(value):
    if value.get('book_id'):
        return "Books"
    if value.get('author_id'):
        return "Authors"
    if value.get('genre_id'):
        return "Genres"
    if value.get('category_id'):
        return "Categories"
    return "Unknown"
