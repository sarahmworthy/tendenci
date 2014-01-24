import imghdr
from os.path import splitext, basename

from django.utils.translation import ugettext_lazy as _
from django.template.defaultfilters import filesizeformat

from tendenci.apps.boxes.models import Box
from tendenci.core.files.utils import get_max_file_upload_size
from tendenci.core.perms.forms import TendenciBaseForm
from django import forms
from tinymce.widgets import TinyMCE


ALLOWED_LOGO_EXT = (
    '.jpg',
    '.jpeg',
    '.gif',
    '.png' 
)


class BoxForm(TendenciBaseForm):
    content = forms.CharField(required=False,
        widget=TinyMCE(attrs={'style':'width:100%'}, 
        mce_attrs={'storme_app_label':Box._meta.app_label, 
        'storme_model':Box._meta.module_name.lower()}))
    photo_upload = forms.FileField(label=_('Photo'), required=False)
    remove_photo = forms.BooleanField(label=_('Remove the current photo'), required=False)

    status_detail = forms.ChoiceField(
        choices=(('active','Active'),('inactive','Inactive'),))

    class Meta:
        model = Box
        fields = (
            'title',
            'content',
            'photo_upload',
            'link',
            'link_title',
            'tags',
            'allow_anonymous_view',
            'user_perms',
            'member_perms',
            'group_perms',
            'status_detail',
            )

    def __init__(self, *args, **kwargs): 
        super(BoxForm, self).__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields['content'].widget.mce_attrs['app_instance_id'] = self.instance.pk
        else:
            self.fields['content'].widget.mce_attrs['app_instance_id'] = 0

        if self.instance.image:
            self.fields['photo_upload'].help_text = '<input name="remove_photo" id="id_remove_photo" type="checkbox"/> Remove current image: <a target="_blank" href="/files/%s/">%s</a>' % (self.instance.image.pk, basename(self.instance.image.file.name))
        else:
            self.fields.pop('remove_photo')

    def clean_photo_upload(self):
        photo_upload = self.cleaned_data['photo_upload']
        if photo_upload:
            extension = splitext(photo_upload.name)[1]
            
            # check the extension
            if extension.lower() not in ALLOWED_LOGO_EXT:
                raise forms.ValidationError('The photo must be of jpg, gif, or png image type.')
            
            # check the image header
            image_type = '.%s' % imghdr.what('', photo_upload.read())
            if image_type not in ALLOWED_LOGO_EXT:
                raise forms.ValidationError('The photo is an invalid image. Try uploading another photo.')

            max_upload_size = get_max_file_upload_size()
            if photo_upload.size > max_upload_size:
                raise forms.ValidationError(_('Please keep filesize under %s. Current filesize %s') % (filesizeformat(max_upload_size), filesizeformat(photo_upload.size)))

        return photo_upload

    def save(self, *args, **kwargs):
        box = super(BoxForm, self).save(*args, **kwargs)
        if self.cleaned_data.get('remove_photo'):
            box.image = None
        return box

