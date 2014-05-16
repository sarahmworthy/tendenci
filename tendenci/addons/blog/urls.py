from django.conf.urls.defaults import include, patterns, url
from tendenci.core.site_settings.utils import get_setting

urlpath = get_setting('module', 'blog', 'url')
enabled = get_setting('module', 'blog', 'enabled') or False


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