from django.conf.urls.defaults import *

urlpatterns = patterns('tendenci.core.sso.views',
    url(r'^acs/$', 'sso_response', name="sso.acs"),
    url(r'^login/$', 'sso_login', name="sso.login"),
    url(r'^logout/$', 'sso_logout', name="sso.logout"),
    url(r'^metadata/', 'descriptor', name="sso.descriptor"),
)
