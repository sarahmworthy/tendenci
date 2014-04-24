from django.conf import settings
from django.conf.urls.defaults import patterns, url
from django.contrib import admin
from django.core.urlresolvers import reverse
from django.shortcuts import redirect, render
from django.http import HttpResponse

from tendenci.core.perms.admin import TendenciBaseModelAdmin
from tendenci.core.files.models import File, MultipleFile
from tendenci.core.files.forms import FileForm, MultiFileForm, FilewithCategoryForm


class FileAdmin(TendenciBaseModelAdmin):
    list_display = ['file_preview', 'name', 'file_path', 'owner_link', 'admin_perms', 'admin_status']
    list_filter = ['status', 'owner_username']
    prepopulated_fields = {}
    search_fields = ['file', 'tags']
    fieldsets = (
        ('File Information', {
            'fields': ('file',
                       'name',
                       'tags',
                       'group',
                       )
        }),
        ('Category', {'fields': ('category', 'sub_category')}),
        ('Permissions', {'fields': ('allow_anonymous_view',)}),
        ('Advanced Permissions', {'classes': ('collapse',), 'fields': (
            'user_perms',
            'member_perms',
            'group_perms',
        )}),
    )
    form = FilewithCategoryForm
    ordering = ['-update_dt']

    class Media:
        js = (
            '%sjs/jquery-1.7.2.min.js' % settings.STATIC_URL,
            '%sjs/categories.js' % settings.STATIC_URL,
        )

    def file_preview(self, obj):
        if obj.type() == "image":
            if obj.file:
                args = [obj.pk]
                args.append("100x50")
                args.append("crop")
                return '<img alt="%s" src="%s" />' % (obj, reverse('file', args=args))
            else:
                return ""
        elif obj.icon():
            return '<img alt="%s" src="%s" />' % (obj.type(), obj.icon())
        else:
            return obj.type()
    file_preview.allow_tags = True
    file_preview.short_description = 'Preview'

    def file_path(self, obj):
        return obj.file
    file_path.short_description = "File Path"

admin.site.register(File, FileAdmin)

class MultipleFileAdmin(admin.ModelAdmin):

    def get_urls(self):
        """
        Add the export view to urls.
        """
        urls = super(MultipleFileAdmin, self).get_urls()
        extra_urls = patterns("",
            url("^add",
                self.admin_site.admin_view(self.add_multiple_file_view),
                name="multiplefile_add"),
        )
        return extra_urls + urls

    def add_multiple_file_view(self, request):
        form = MultiFileForm(user=request.user)

        if request.method == 'POST':
            form = MultiFileForm(request.POST, request.FILES, user=request.user)
            if form.is_valid():
                form.save()
                return redirect(reverse('admin:files_file_changelist'))
        return render(request,
            'admin/files/file/multiple_file_upload.html',{
            'adminform': form
        });

    def changelist_view(self, request, extra_context=None):
        return redirect(reverse('admin:multiplefile_add'))


admin.site.register(MultipleFile, MultipleFileAdmin)
