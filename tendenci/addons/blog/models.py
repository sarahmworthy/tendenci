from django.db import models
from zinnia.models.entry import Entry
from zinnia.models.category import Category

class BlogEntry(Entry):
    class Meta:
        proxy = True
        verbose_name = "Entry"
        verbose_name_plural = "Entries"


class BlogCategory(Category):
    class Meta:
        proxy = True
        verbose_name = "Category"
        verbose_name_plural = "Categories"
