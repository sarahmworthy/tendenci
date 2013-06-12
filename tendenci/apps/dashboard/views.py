import simplejson
from datetime import datetime, timedelta
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.contrib.auth.models import User
from dateutil import parser

from tendenci.apps.dashboard.models import DashboardStat
from tendenci.core.event_logs.models import EventLog
from tendenci.core.site_settings.models import Setting
from tendenci.core.site_settings.utils import get_setting
from tendenci.core.theme.shortcuts import themed_response

@login_required
def index(request, template_name="dashboard/indexV2.html"):
    profile_redirect = get_setting('site', 'global', 'profile_redirect')
    if profile_redirect and profile_redirect != '/dashboard' and not request.user.profile.is_superuser:
        return redirect(profile_redirect)

    # self signup  free trial version
    has_paid = True
    activate_url = ''
    expired = False
    expiration_dt = ''
    if get_setting('site', 'developer', 'partner') == 'Self-Signup' \
             and  get_setting('site', 'developer', 'freepaid') == 'free':
        has_paid = False
        activate_url = get_setting('site', 'developer', 'siteactivatepaymenturl')
        site_create_dt = get_setting('site', 'developer', 'sitecreatedt')
        
        if site_create_dt:
            site_create_dt = parser.parse(site_create_dt)
        else:
            # find the site create date in user's table
            u = User.objects.get(pk=1)
            site_create_dt = u.date_joined
            
        expiration_dt = site_create_dt + timedelta(days=30)
            
        now = datetime.now()
        if now >= expiration_dt:
            expired = True

    events = simplejson.loads(
        DashboardStat.objects.get_latest('events_upcoming').value, use_decimal=True)
    forms = simplejson.loads(
        DashboardStat.objects.get_latest('forms_30_submissions').value)
    pages_traffic = simplejson.loads(
        DashboardStat.objects.get_latest('pages_30_traffic').value)
    events_traffic = simplejson.loads(
        DashboardStat.objects.get_latest('events_30_traffic').value)
    members = simplejson.loads(
        DashboardStat.objects.get_latest('memberships_30_count').value)
    corp_new = simplejson.loads(
        DashboardStat.objects.get_latest('corp_memberships_30_new').value)
    corp_renew = simplejson.loads(
        DashboardStat.objects.get_latest('corp_memberships_30_renew').value)
    corp_expired = simplejson.loads(
        DashboardStat.objects.get_latest('corp_memberships_30_expired').value)
    corp_expiring = simplejson.loads(
        DashboardStat.objects.get_latest('corp_memberships_30_expiring').value)
    corp_members = simplejson.loads(
        DashboardStat.objects.get_latest('corp_members_top').value)

    EventLog.objects.log()
    return render_to_response(template_name, {
        'has_paid': has_paid,
        'activate_url': activate_url,
        'expired': expired,
        'expiration_dt': expiration_dt,
        'events': events,
        'forms': forms,
        'pages_traffic': pages_traffic,
        'events_traffic': events_traffic,
        'members': members,
        'corp_new': corp_new,
        'corp_renew': corp_renew,
        'corp_expired': corp_expired,
        'corp_expiring': corp_expiring,
        'corp_members': corp_members,
    }, context_instance=RequestContext(request))
