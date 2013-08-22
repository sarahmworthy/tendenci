from BeautifulSoup import BeautifulSoup
from django.db.models import ForeignKey, TextField
from django.template import Library
from tinymce.models import HTMLField

from tendenci.core.files.models import File
from tendenci.core.site_settings.utils import get_setting


register = Library()


@register.inclusion_tag("meta/og_image.html")
def meta_og_image(obj, field_name):
    base_url = get_setting('site', 'global', 'siteurl')
    try:
        field = obj._meta.get_field_by_name(field_name)[0]
        image_list = []

        if isinstance(field, HTMLField) or isinstance(field, TextField):
            content = getattr(obj, field_name)
            soup = BeautifulSoup(content)
            for image in soup.findAll("img"):
                image_url = base_url + image["src"]
                image_list.append(image_url)

        elif isinstance(field, ForeignKey):
            image = getattr(obj, field_name)
            if isinstance(image, File):
                image_list.append(base_url + image.get_absolute_url())

        return {'obj_id': obj.id,
                'app': obj._meta.app_label,
                'field': field_name,
                'urls': image_list}
    except Exception:
        return {}
