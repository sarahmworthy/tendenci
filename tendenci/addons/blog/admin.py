from django.contrib import admin

from zinnia.models.entry import Entry
from zinnia.models.category import Category
from zinnia.admin.entry import EntryAdmin
from zinnia.admin.category import CategoryAdmin

from .models import BlogEntry, BlogCategory

admin.site.unregister(Entry)
admin.site.unregister(Category)
admin.site.register(BlogEntry, EntryAdmin)
admin.site.register(BlogCategory, CategoryAdmin)
