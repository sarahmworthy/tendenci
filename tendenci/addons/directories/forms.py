import imghdr
from datetime import datetime
from os.path import splitext, basename

from django import forms
from django.forms.util import ErrorList
from tinymce.widgets import TinyMCE
from tendenci.core.perms.forms import TendenciBaseForm
from tendenci.core.base.fields import SplitDateTimeField
from django.template.defaultfilters import filesizeformat
from django.utils.translation import ugettext_lazy as _
from django.utils.safestring import mark_safe
from django.core.urlresolvers import reverse
from django.contrib.contenttypes.models import ContentType
from tendenci.core.categories.forms import CategoryField
from tendenci.core.categories.models import CategoryItem
from tendenci.addons.directories.models import Directory, DirectoryPricing
from tendenci.addons.directories.utils import (get_payment_method_choices,
    get_duration_choices)
from tendenci.addons.directories.choices import (DURATION_CHOICES, ADMIN_DURATION_CHOICES,
    STATUS_CHOICES)
from tendenci.core.base.fields import EmailVerificationField, CountrySelectField
from tendenci.core.files.utils import get_max_file_upload_size
from tendenci.core.site_settings.utils import get_setting

ALLOWED_LOGO_EXT = (
    '.jpg',
    '.jpeg',
    '.gif',
    '.png'
)

request_duration_defaults = {
    'label': _('Requested Duration'),
    'help_text': mark_safe('<a href="%s" id="add_id_pricing">Add Pricing Options</a>' % '/directories/pricing/add/'),
}

SEARCH_CATEGORIES_ADMIN = (
    ('', '-- SELECT ONE --' ),
    ('id', 'Directory ID'),
    ('body__icontains', 'Body'),
    ('headline__icontains', 'Headline'),
    ('city__icontains', 'City'),
    ('state__iexact', 'State'),
    ('tags__icontains', 'Tags'),
    ('tags__contains', 'Tags (case sensitive)'),

    ('creator__id', 'Creator Userid(#)'),
    ('creator__username', 'Creator Username'),
    ('owner__id', 'Owner Userid(#)'),
    ('owner__username', 'Owner Username'),

    ('status_detail__icontains', 'Status Detail'),
)

SEARCH_CATEGORIES = (
    ('', '-- SELECT ONE --' ),
    ('id', 'Directory ID'),
    ('body__icontains', 'Body'),
    ('headline__icontains', 'Headline'),
    ('city__icontains', 'City'),
    ('state__iexact', 'State'),
    ('tags__icontains', 'Tags'),
    ('tags__contains', 'Tags (case sensitive)'),
)

class DirectorySearchForm(forms.Form):
    search_category = forms.ChoiceField(choices=SEARCH_CATEGORIES_ADMIN, required=False)
    category = CategoryField(label=_('Category'), choices=[], required=False)
    sub_category = CategoryField(label=_('Sub Category'), choices=[], required=False)
    q = forms.CharField(required=False)

    def __init__(self, *args, **kwargs):
        is_superuser = kwargs.pop('is_superuser', None)
        super(DirectorySearchForm, self).__init__(*args, **kwargs)

        if not is_superuser:
            self.fields['search_category'].choices = SEARCH_CATEGORIES

        categories, sub_categories = Directory.objects.get_categories()

        categories = [(cat.pk, cat) for cat in categories]
        sub_categories = [(cat.pk, cat) for cat in sub_categories]

        self.fields['category'].choices = categories
        self.fields['sub_category'].choices = sub_categories


    def clean(self):
        cleaned_data = self.cleaned_data
        q = self.cleaned_data.get('q', None)
        cat = self.cleaned_data.get('search_category', None)

        if cat is None or cat == "" :
            if not (q is None or q == ""):
                self._errors['search_category'] =  ErrorList(['Select a category'])

        if cat in ('id', 'owner__id', 'creator__id') :
            try:
                x = int(q)
            except ValueError:
                self._errors['q'] = ErrorList(['ID must be a number.'])

        return cleaned_data


class DirectoryForm(TendenciBaseForm):
    body = forms.CharField(required=False,
        widget=TinyMCE(attrs={'style':'width:100%'},
        mce_attrs={'storme_app_label':Directory._meta.app_label,
        'storme_model':Directory._meta.module_name.lower()}))

    logo = forms.FileField(
      required=False,
      help_text=_('Company logo. Only jpg, gif, or png images.'))

    status_detail = forms.ChoiceField(
        choices=(('active','Active'),('inactive','Inactive'), ('pending','Pending'),))

    list_type = forms.ChoiceField(initial='regular', choices=(('regular','Regular'),
                                                              ('premium', 'Premium'),))
    payment_method = forms.CharField(error_messages={'required': 'Please select a payment method.'})

    activation_dt = SplitDateTimeField(initial=datetime.now())
    expiration_dt = SplitDateTimeField(initial=datetime.now())

    email = EmailVerificationField(label=_("Email"), required=False)
    email2 = EmailVerificationField(label=_("Email 2"), required=False)
    country = CountrySelectField(label=_("Country"), required=False)
    
    pricing = forms.ModelChoiceField(queryset=DirectoryPricing.objects.filter(status=True).order_by('duration'),
                    **request_duration_defaults)

    class Meta:
        model = Directory
        fields = (
            'headline',
            'slug',
            'summary',
            'body',
            'logo',
            'source',
            'timezone',
            'first_name',
            'last_name',
            'address',
            'address2',
            'city',
            'state',
            'zip_code',
            'country',
            'phone',
            'phone2',
            'fax',
            'email',
            'email2',
            'website',
            'tags',
            'pricing',
            'list_type',
            'payment_method',
            'activation_dt',
            'expiration_dt',
            'allow_anonymous_view',
            'allow_user_view',
            'allow_user_edit',
            'syndicate',
            'user_perms',
            'member_perms',
            'group_perms',
            'status_detail',
        )

        fieldsets = [('Directory Information', {
                      'fields': ['headline',
                                 'slug',
                                 'summary',
                                 'body',
                                 'logo',
                                 'tags',
                                 'source',
                                 'timezone',
                                 'activation_dt',
                                 'pricing',
                                 'expiration_dt',
                                 ],
                      'legend': ''
                      }),
                      ('Payment', {
                      'fields': ['list_type',
                                 'payment_method'
                                 ],
                        'classes': ['payment_method'],
                      }),
                      ('Contact', {
                      'fields': ['first_name',
                                 'last_name',
                                  'address',
                                  'address2',
                                  'city',
                                  'state',
                                  'zip_code',
                                  'country',
                                  'phone',
                                  'phone2',
                                  'fax',
                                  'email',
                                  'email2',
                                  'website'
                                 ],
                        'classes': ['contact'],
                      }),
                      ('Permissions', {
                      'fields': ['allow_anonymous_view',
                                 'user_perms',
                                 'member_perms',
                                 'group_perms',
                                 ],
                      'classes': ['permissions'],
                      }),
                     ('Administrator Only', {
                      'fields': ['syndicate',
                                 'status_detail'],
                      'classes': ['admin-only'],
                    })]

    def clean_logo(self):
        logo = self.cleaned_data['logo']
        if logo:
            try:
                extension = splitext(logo.name)[1]

                # check the extension
                if extension.lower() not in ALLOWED_LOGO_EXT:
                    raise forms.ValidationError('The logo must be of jpg, gif, or png image type.')

                # check the image header
                image_type = '.%s' % imghdr.what('', logo.read())
                if image_type not in ALLOWED_LOGO_EXT:
                    raise forms.ValidationError('The logo is an invalid image. Try uploading another logo.')

                max_upload_size = get_max_file_upload_size()
                if logo.size > max_upload_size:
                    raise forms.ValidationError(_('Please keep filesize under %s. Current filesize %s') % (filesizeformat(max_upload_size), filesizeformat(logo.size)))
            except IOError:
                logo = None

        return logo

    def __init__(self, *args, **kwargs):
        super(DirectoryForm, self).__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields['body'].widget.mce_attrs['app_instance_id'] = self.instance.pk
            if self.user.profile.is_superuser:
                self.fields['status_detail'].choices = (('active','Active'),
                                                        ('inactive','Inactive'),
                                                        ('pending','Pending'),
                                                        ('paid - pending approval', 'Paid - Pending Approval'),)
        else:
            self.fields['body'].widget.mce_attrs['app_instance_id'] = 0

        if self.instance.logo:
            self.initial['logo'] = self.instance.logo

        if not self.user.profile.is_superuser:
            if 'status_detail' in self.fields: self.fields.pop('status_detail')

        if self.fields.has_key('payment_method'):
            self.fields['payment_method'].widget = forms.RadioSelect(choices=get_payment_method_choices(self.user))
        if self.fields.has_key('pricing'):
            self.fields['pricing'].choices = get_duration_choices(self.user)

        self.fields['timezone'].initial = get_setting('site', 'global', 'defaulttimezone')

        # expiration_dt = activation_dt + requested_duration
        fields_to_pop = ['expiration_dt']
        if not self.user.profile.is_superuser:
            fields_to_pop += [
                'slug',
                'entity',
                'allow_anonymous_view',
                'user_perms',
                'member_perms',
                'group_perms',
                'post_dt',
                'activation_dt',
                'syndicate',
                'status_detail'
            ]

        for f in list(set(fields_to_pop)):
            if f in self.fields:
                self.fields.pop(f)

    def save(self, *args, **kwargs):
        from tendenci.core.files.models import File
        directory = super(DirectoryForm, self).save(*args, **kwargs)

        content_type = ContentType.objects.get(
                app_label=Directory._meta.app_label,
                model=Directory._meta.module_name)

        if self.cleaned_data.has_key('pricing'):
            directory.requested_duration = self.cleaned_data['pricing'].duration

        if self.cleaned_data['logo']:
            file_object, created = File.objects.get_or_create(
                file=self.cleaned_data['logo'],
                defaults={
                    'name': self.cleaned_data['logo'].name,
                    'content_type': content_type,
                    'object_id': directory.pk,
                    'is_public': directory.allow_anonymous_view,
                    'tags': directory.tags,
                })

            directory.logo_file = file_object
            directory.save(log=False)

        # clear logo; if box checked
        if self.cleaned_data['logo'] is False:
          directory.logo_file = None
          directory.save(log=False)
          File.objects.filter(
            content_type=content_type,
            object_id=directory.pk).delete()

        return directory


class DirectoryPricingForm(forms.ModelForm):
    status = forms.ChoiceField(initial=1, choices=STATUS_CHOICES, required=False)

    class Meta:
        model = DirectoryPricing
        fields = ('duration',
                  'regular_price',
                  'premium_price',
                  'regular_price_member',
                  'premium_price_member',
                  'show_member_pricing',
                  'status',)

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(DirectoryPricingForm, self).__init__(*args, **kwargs)
        if user and user.profile.is_superuser:
            self.fields['duration'] = forms.ChoiceField(initial=14, choices=ADMIN_DURATION_CHOICES)
        else:
            self.fields['duration'] = forms.ChoiceField(initial=14, choices=DURATION_CHOICES)

class DirectoryRenewForm(TendenciBaseForm):
    list_type = forms.ChoiceField(initial='regular', choices=(('regular','Regular'),
                                                              ('premium', 'Premium'),))
    payment_method = forms.CharField(error_messages={'required': 'Please select a payment method.'})

    pricing = forms.ModelChoiceField(label=_('Requested Duration'),
                    queryset=DirectoryPricing.objects.filter(status=True).order_by('duration'))

    class Meta:
        model = Directory
        fields = (
            'pricing',
            'list_type',
            'payment_method',
        )

        fieldsets = [('Payment', {
                      'fields': ['list_type',
                                 'pricing',
                                 'payment_method'
                                 ],
                        'classes': ['payment_method'],
                    })]

    def __init__(self, *args, **kwargs):
        super(DirectoryRenewForm, self).__init__(*args, **kwargs)

        if self.fields.has_key('payment_method'):
            self.fields['payment_method'].widget = forms.RadioSelect(choices=get_payment_method_choices(self.user))
        if self.fields.has_key('pricing'):
            self.fields['pricing'].choices = get_duration_choices(self.user)

    def save(self, *args, **kwargs):
        directory = super(DirectoryRenewForm, self).save(*args, **kwargs)
        if self.cleaned_data.has_key('pricing'):
            directory.requested_duration = self.cleaned_data['pricing'].duration
        return directory


class DirectoryExportForm(forms.Form):

    STATUS_DETAIL_CHOICES = (
        ('', 'Export All Directories'),
        ('active', ' Export Active Directories'),
        ('pending', 'Export Pending Directories'),
        ('inactive', 'Export Inactive Directories'),
    )

    EXPORT_FIELD_CHOICES = (
        ('main_fields', 'Export Main Fields (fastest)'),
        ('all_fields', 'Export All Fields'),
    )

    export_format = forms.CharField(widget=forms.HiddenInput(), initial='csv')
    export_status_detail = forms.ChoiceField(choices=STATUS_DETAIL_CHOICES, required=False)
    export_fields = forms.ChoiceField(choices=EXPORT_FIELD_CHOICES)

