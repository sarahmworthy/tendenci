from haystack import indexes
from haystack import site

from django.utils.html import strip_tags, strip_entities

from tendenci.apps.pages.models import Page
from tendenci.core.perms.indexes import TendenciBaseSearchIndex
from tendenci.core.categories.models import Category


class PageIndex(TendenciBaseSearchIndex):
    title = indexes.CharField(model_attr='title')
    content = indexes.CharField(model_attr='content')

    # categories
    category = indexes.CharField()
    sub_category = indexes.CharField()

    def prepare_content(self, obj):
        content = obj.content
        content = strip_tags(content)
        content = strip_entities(content)
        return content

    def prepare_category(self, obj):
        category = Category.objects.get_for_object(obj, 'category')
        if category:
            return category.name
        return ''

    def prepare_sub_category(self, obj):
        category = Category.objects.get_for_object(obj, 'sub_category')
        if category:
            return category.name
        return ''

site.register(Page, PageIndex)
