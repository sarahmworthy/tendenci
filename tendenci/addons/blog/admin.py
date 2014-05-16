from django.contrib import admin

from zinnia.models.entry import Entry
from zinnia.models.category import Category
from zinnia.admin.entry import EntryAdmin
from zinnia.admin.category import CategoryAdmin
from zinnia_threaded_comments.models import ThreadedComment
from zinnia_threaded_comments.admin import ThreadedCommentAdmin

from .models import BlogEntry, BlogCategory, BlogComment

admin.site.unregister(Entry)
admin.site.unregister(Category)
admin.site.unregister(ThreadedComment)
admin.site.register(BlogEntry, EntryAdmin)
admin.site.register(BlogCategory, CategoryAdmin)
admin.site.register(BlogComment, ThreadedCommentAdmin)
