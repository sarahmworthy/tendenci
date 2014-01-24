from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.safestring import mark_safe
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType

from tendenci.core.perms.object_perms import ObjectPermission
from tagging.fields import TagField
from tendenci.core.files.models import File
from tendenci.core.perms.models import TendenciBaseModel
from tendenci.libs.abstracts.models import OrderingBaseModel
from tendenci.apps.boxes.managers import BoxManager
from tinymce import models as tinymce_models


class Box(OrderingBaseModel, TendenciBaseModel):
    title = models.CharField(max_length=500, blank=True)
    content = tinymce_models.HTMLField()
    tags = TagField(blank=True)

    image = models.ForeignKey(File, null=True, default=None)
    link = models.CharField(max_length=300, blank=True)
    link_title = models.CharField(max_length=300, blank=True,
        help_text=_('Would default to "Read More" if left blank.'))

    perms = generic.GenericRelation(ObjectPermission,
                                          object_id_field="object_id",
                                          content_type_field="content_type")

    objects = BoxManager()

    class Meta:
        permissions = (("view_box","Can view box"),)
        verbose_name_plural = "Boxes"
        ordering = ['position']
    
    def __unicode__(self):
        return self.title
        
    def safe_content(self):
        return mark_safe(self.content)

    def save(self, *args, **kwargs):
        model = self.__class__
        photo_upload = kwargs.pop('photo', None)
        
        if self.position is None:
            # Append
            try:
                last = model.objects.order_by('-position')[0]
                self.ordering = last.ordering + 1
            except IndexError:
                # First row
                self.ordering = 0

        super(Box, self).save(*args, **kwargs)

        if photo_upload and self.pk:
            image = File(
                content_type=ContentType.objects.get_for_model(model),
                object_id=self.pk,
                creator=self.creator,
                creator_username=self.creator_username,
                owner=self.owner,
                owner_username=self.owner_username
            )
            photo_upload.file.seek(0)
            image.file.save(photo_upload.name, photo_upload)  # save file row
            image.save()  # save image row

            if self.image:
                self.image.delete()  # delete image and file row
            self.image = image  # set image

            self.save()

