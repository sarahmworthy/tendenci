'''
Created on 28-02-2011

@author: hpolloni
'''
import subprocess

from django.contrib.sites.models import get_current_site
from django.core.paginator import EmptyPage, PageNotAnInteger
from django.http import Http404
from django.template.response import TemplateResponse

from django.conf import settings
from django.core.cache import cache
from tendenci.core.sitemaps import TendenciSitemap
from tendenci.core.site_settings.utils import get_setting


_sitemap_cache = []
def get_all_sitemaps():
    for app in settings.INSTALLED_APPS:
        _try_import(app + '.feeds')
    sitemaps = []
    # only include sitemaps whose module is enabled
    for sitemap in TendenciSitemap.__subclasses__():
        if check_enabled(sitemap):
            sitemaps.append(sitemap)
    return sitemaps

def check_enabled(value):
    ''' 
    Format for module is <packages>.<app_label>.feeds
    We first get the app_label to be passed to the get_setting function
    '''
    module = value.__module__.split('.')
    app = module[(len(module)-2)]
    # Only check if it's false since other packages may not use our settings
    if get_setting('module', app, 'enabled') == False:
        return False
    return True

def _try_import(module):
    try:
        __import__(module)
    except ImportError, e:
        pass


def create_sitemap(request):
    sitemap_classes = get_all_sitemaps()
    sitemaps = dict([(cls.__name__, cls) for cls in sitemap_classes])
    return sitemap(request, sitemaps)


def sitemap(request, sitemaps, section=None,
            template_name='sitemap.xml', mimetype='application/xml'):
    req_protocol = 'https' if request.is_secure() else 'http'
    req_site = get_current_site(request)

    if section is not None:
        if section not in sitemaps:
            raise Http404("No sitemap available for section: %r" % section)
        maps = [sitemaps[section]]
    else:
        maps = sitemaps.values()
    page = request.GET.get("p", 1)

    urls = []
    cached = False
    for site in maps:
        try:
            if callable(site):
                site = site()
                site_key = site.__class__.__name__
            else:
                site_key = site.__name__
            # Cache the sitemap urls
            sitemap_cache_key = '.'.join([settings.SITE_CACHE_KEY, 'sitemap_cache', site_key])
            site_urls = cache.get(sitemap_cache_key)
            if not isinstance(site_urls, list):
                if not cached:
                    subprocess.Popen(['python', 'manage.py', 'sitemap_cache'])
                    cached = True
                site_urls = site.get_urls(page=page, site=req_site,
                                          protocol=req_protocol)
                cache.set(sitemap_cache_key, list(site_urls), 86400)
            urls.extend(site_urls)
        except EmptyPage:
            raise Http404("Page %s empty" % page)
        except PageNotAnInteger:
            raise Http404("No page '%s'" % page)
    return TemplateResponse(request, template_name, {'urlset': urls},
                            content_type=mimetype)
