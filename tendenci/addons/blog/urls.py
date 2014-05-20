from django.conf.urls.defaults import include, patterns, url
from tendenci.core.site_settings.utils import get_setting

from zinnia.sitemaps import TagSitemap
from zinnia.sitemaps import EntrySitemap
from zinnia.sitemaps import CategorySitemap
from zinnia.sitemaps import AuthorSitemap

urlpath = get_setting('module', 'blog', 'url')
enabled = get_setting('module', 'blog', 'enabled') or False

sitemaps = {'tags': TagSitemap,
            'blog': EntrySitemap,
            'authors': AuthorSitemap,
            'categories': CategorySitemap,}


urlpatterns = patterns('',
    url(r'^%s/comments/' % urlpath, include('django.contrib.comments.urls')),
)

if enabled:
    urlpatterns += patterns('',
        url(r'^%s/' % urlpath, include('zinnia.urls'))
    )
else:
    urlpatterns += patterns('',
        url(r'^%s/' % urlpath, 'tendenci.addons.blog.views.blog_disabled')
    )

urlpatterns += patterns(
    'django.contrib.sitemaps.views',
    url(r'^sitemap.xml$', 'index',
        {'sitemaps': sitemaps}),
    url(r'^sitemap-(?P<section>.+)\.xml$', 'sitemap',
        {'sitemaps': sitemaps}),)