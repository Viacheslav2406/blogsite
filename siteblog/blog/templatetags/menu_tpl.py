from django import template
from blog.models import Tag, Category
from django.db.models import Count

register = template.Library()


@register.inclusion_tag('blog/list_categories.html')
def show_categories():
    categories = Category.objects.annotate(cnt=Count('posts'))
    return {
        'categories': categories
    }


@register.inclusion_tag('blog/list_tags.html')
def show_tags():
    tags = Tag.objects.annotate(cnt=Count('posts'))
    return {
        'tags': tags
    }