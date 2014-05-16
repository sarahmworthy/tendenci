from django.db import models
from zinnia.models.entry import Entry
from zinnia.models.category import Category
from zinnia_threaded_comments.models import ThreadedComment

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


class BlogComment(ThreadedComment):
    class Meta:
        proxy = True
        verbose_name = "Comment"
        verbose_name_plural = "Comments"
