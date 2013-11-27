from django.conf.urls import patterns
from tendenci.core.sitemaps import views

urlpatterns = patterns('',
    (r'^$', views.create_sitemap)
)
