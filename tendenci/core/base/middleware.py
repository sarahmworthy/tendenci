from datetime import datetime, timedelta

from django.conf import settings
from django.contrib.auth.models import AnonymousUser
from django.core.cache import cache
from django.db.utils import DatabaseError
from django.template import RequestContext

from tracking import utils
from tracking.models import Visitor, UntrackedUserAgent

from tendenci.core.base.http import Http403, render_to_403, MissingApp, render_to_missing_app


class Http403Middleware(object):
    def process_exception(self, request, exception):
        from django.contrib.auth.views import redirect_to_login
        if isinstance(exception, Http403):
            if request.user.is_anonymous():
                return redirect_to_login(request.path)
            return render_to_403(context_instance=RequestContext(request))


class MissingAppMiddleware(object):
    def process_exception(self, request, exception):
        if isinstance(exception, MissingApp):
            return render_to_missing_app(context_instance=RequestContext(request))


class VisitorTrackingMiddleware(object):
    """
    Keeps track of your active users.  Anytime a visitor accesses a valid URL,
    their unique record will be updated with the page they're on and the last
    time they requested a page.

    Records are considered to be unique when the session key and IP address
    are unique together.  Sometimes the same user used to have two different
    records, so I added a check to see if the session key had changed for the
    same IP and user agent in the last 5 minutes

    Custom version of the original tracking.middleware.VisitorTrackingMiddleware
    to instead have the pages we need to track as prefixes, since currently we only
    track page edit views
    """

    @property
    def prefixes(self):
        """Returns a list of URL prefixes that we should track"""

        if not hasattr(self, '_prefixes'):
            self._prefixes = getattr(settings, 'TRACKING_PREFIXES', [])

            if not getattr(settings, '_FREEZE_TRACKING_PREFIXES', False):
                settings.TRACKING_PREFIXES = self._prefixes
                settings._FREEZE_TRACKING_PREFIXES = True

        return self._prefixes

    def process_request(self, request):
        # don't process AJAX requests
        if request.is_ajax(): return

        # create some useful variables
        ip_address = utils.get_ip(request)
        user_agent = unicode(request.META.get('HTTP_USER_AGENT', '')[:255], errors='ignore')

        # retrieve untracked user agents from cache
        ua_key = '_tracking_untracked_uas'
        untracked = cache.get(ua_key)
        if untracked is None:
            untracked = UntrackedUserAgent.objects.all()
            cache.set(ua_key, untracked, 3600)

        # see if the user agent is not supposed to be tracked
        for ua in untracked:
            # if the keyword is found in the user agent, stop tracking
            if user_agent.find(ua.keyword) != -1:
                return

        if hasattr(request, 'session') and request.session.session_key:
            # use the current session key if we can
            session_key = request.session.session_key
        else:
            # otherwise just fake a session key
            session_key = '%s:%s' % (ip_address, user_agent)
            session_key = session_key[:40]

        # ensure that the request.path begin with any of the prefixes
        prefix_found = False
        for prefix in self.prefixes:
            if request.path.startswith(prefix):
                prefix_found = True

        if not prefix_found:
            return

        # if we get here, the URL needs to be tracked
        # determine what time it is
        now = datetime.now()

        attrs = {
            'session_key': session_key,
            'ip_address': ip_address
        }

        # for some reason, Visitor.objects.get_or_create was not working here
        try:
            visitor = Visitor.objects.get(**attrs)
        except Visitor.DoesNotExist:
            # see if there's a visitor with the same IP and user agent
            # within the last 5 minutes
            cutoff = now - timedelta(minutes=5)
            visitors = Visitor.objects.filter(
                ip_address=ip_address,
                user_agent=user_agent,
                last_update__gte=cutoff
            )

            if len(visitors):
                visitor = visitors[0]
                visitor.session_key = session_key
            else:
                # it's probably safe to assume that the visitor is brand new
                visitor = Visitor(**attrs)
        except:
            return

        # determine whether or not the user is logged in
        user = request.user
        if isinstance(user, AnonymousUser):
            user = None

        # update the tracking information
        visitor.user = user
        visitor.user_agent = user_agent

        # if the visitor record is new, or the visitor hasn't been here for
        # at least an hour, update their referrer URL
        one_hour_ago = now - timedelta(hours=1)
        if not visitor.last_update or visitor.last_update <= one_hour_ago:
            visitor.referrer = utils.u_clean(request.META.get('HTTP_REFERER', 'unknown')[:255])

            # reset the number of pages they've been to
            visitor.page_views = 0
            visitor.session_start = now

        visitor.url = request.path
        visitor.page_views += 1
        visitor.last_update = now
        try:
            visitor.save()
        except DatabaseError:
            pass
