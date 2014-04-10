import uuid
from datetime import datetime
from django.db import models
from tendenci.apps.user_groups.models import Group
from tendenci.apps.user_groups.utils import get_default_group
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes import generic

from tagging.fields import TagField
from tendenci.core.base.fields import SlugField
from timezones.fields import TimeZoneField
from timezones.utils import localtime_for_timezone
from tendenci.core.perms.models import TendenciBaseModel
from tendenci.core.perms.object_perms import ObjectPermission
from tendenci.core.categories.models import CategoryItem
from tendenci.addons.news.managers import NewsManager
from tinymce import models as tinymce_models
from tendenci.core.meta.models import Meta as MetaTags
from tendenci.addons.news.module_meta import NewsMeta
from tendenci.core.files.models import File
from tendenci.libs.boto_s3.utils import set_s3_file_permission

class News(TendenciBaseModel):
    guid = models.CharField(max_length=40)
    slug = SlugField(_('URL Path'), unique=True)
    timezone = TimeZoneField(_('Time Zone'))
    headline = models.CharField(max_length=200, blank=True)
    summary = models.TextField(blank=True)
    body = tinymce_models.HTMLField()
    source = models.CharField(max_length=300, blank=True)
    first_name = models.CharField(_('First Name'), max_length=100, blank=True)
    last_name = models.CharField(_('Last Name'), max_length=100, blank=True)
    google_profile = models.URLField(_('Add a link to your Google+ Profile'), blank=True)
    phone = models.CharField(max_length=50, blank=True)
    fax = models.CharField(max_length=50, blank=True)
    email = models.CharField(max_length=120, blank=True)
    website = models.CharField(max_length=300, blank=True)
    thumbnail = models.ForeignKey('NewsImage', default=None, null=True, help_text=_('The thumbnail image can be used on your homepage or sidebar if it is setup in your theme. The thumbnail image will not display on the news page.'))
    release_dt = models.DateTimeField(_('Release Date/Time'), null=True, blank=True)
    syndicate = models.BooleanField(_('Include in RSS feed'), default=True)
    design_notes = models.TextField(_('Design Notes'), blank=True)
    group = models.ForeignKey(Group, null=True, default=get_default_group, on_delete=models.SET_NULL)
    tags = TagField(blank=True)

    #for podcast feeds
    enclosure_url = models.CharField(_('Enclosure URL'), max_length=500, blank=True) # for podcast feeds
    enclosure_type = models.CharField(_('Enclosure Type'),max_length=120, blank=True) # for podcast feeds
    enclosure_length = models.IntegerField(_('Enclosure Length'), default=0) # for podcast feeds

    use_auto_timestamp = models.BooleanField(_('Auto Timestamp'))
        
    # html-meta tags
    meta = models.OneToOneField(MetaTags, null=True)
    
    categories = generic.GenericRelation(CategoryItem,
                                          object_id_field="object_id",
                                          content_type_field="content_type")
    
    perms = generic.GenericRelation(ObjectPermission,
                                          object_id_field="object_id",
                                          content_type_field="content_type")

    objects = NewsManager()

    class Meta:
        permissions = (("view_news","Can view news"),)
        verbose_name_plural = "News"

    def get_meta(self, name):
        """
        This method is standard across all models that are
        related to the Meta model.  Used to generate dynamic
        meta information niche to this model.
        """
        return NewsMeta().get_meta(self, name)

    @models.permalink
    def get_absolute_url(self):
        return ("news.detail", [self.slug])

    def __unicode__(self):
        return self.headline

    def save(self, *args, **kwargs):
        if not self.id:
            self.guid = str(uuid.uuid1())
        photo_upload = kwargs.pop('photo', None)
        super(News, self).save(*args, **kwargs)

        if photo_upload and self.pk:
            image = NewsImage(
                object_id=self.pk,
                creator=self.creator,
                creator_username=self.creator_username,
                owner=self.owner,
                owner_username=self.owner_username
                    )
            photo_upload.file.seek(0)
            image.file.save(photo_upload.name, photo_upload)  # save file row
            image.save()  # save image row

            if self.thumbnail:
                self.thumbnail.delete()  # delete image and file row
            self.thumbnail = image  # set image

            self.save()

        if self.thumbnail:
            if self.is_public():
                set_s3_file_permission(self.thumbnail.file, public=True)
            else:
                set_s3_file_permission(self.thumbnail.file, public=False)

    @property
    def category_set(self):
        items = {}
        for cat in self.categories.select_related('category__name', 'parent__name'):
            if cat.category:
                items["category"] = cat.category
            elif cat.parent:
                items["sub_category"] = cat.parent
        return items

    def is_public(self):
        return all([self.allow_anonymous_view,
                self.status,
                self.status_detail in ['active']])

    @property
    def release_dt_with_tz(self):
        return datetime(
                year = self.release_dt.year,
                month = self.release_dt.month,
                day = self.release_dt.day,
                hour = self.release_dt.hour,
                minute = self.release_dt.minute,
                tzinfo = self.timezone )

    @property
    def release_dt_default_tz(self):
        return localtime_for_timezone(self.release_dt_with_tz, None)

    @property
    def is_released(self):
        now = localtime_for_timezone(datetime.now(), None)
        return self.release_dt_default_tz <= now


class NewsImage(File):
    pass
