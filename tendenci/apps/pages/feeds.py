from tendenci.core.perms.utils import PUBLIC_FILTER
from tendenci.core.sitemaps import TendenciSitemap

from tendenci.apps.pages.models import Page

class PageSitemap(TendenciSitemap):
    """ Sitemap information for pages """
    changefreq = "yearly"
    priority = 0.6

    def items(self):
        items = Page.objects.filter(**PUBLIC_FILTER).order_by('-create_dt')
        return items

    def lastmod(self, obj):
        return obj.update_dt
