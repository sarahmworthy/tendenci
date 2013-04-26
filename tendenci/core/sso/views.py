import base64

from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.views.decorators.csrf import csrf_view_exempt

from BeautifulSoup import BeautifulStoneSoup

from tendenci.apps.profiles.models import Profile
from tendenci.core.perms.decorators import is_enabled
from tendenci.core.site_settings.utils import get_setting
from tendenci.core.sso import base
from tendenci.core.sso import sso_settings
from tendenci.core.sso import xml_render
from tendenci.core.sso import xml_signing


def xml_response(request, template, tv):
    return render_to_response(template, tv, mimetype="application/xml",
        context_instance=RequestContext(request))


def _get_entity_id(request):
    entity_id = get_setting('module', 'sso', 'entity_id')
    if not entity_id:
        entity_id = request.build_absolute_uri(reverse('sso.descriptor'))
    return entity_id


def _get_email_from_assertion(assertion):
    """
    Returns the email out of the assertion.

    At present, Assertion must pass the email address as the Subject, eg.:

    <saml:Subject>
            <saml:NameID Format="urn:oasis:names:tc:SAML:2.0:nameid-format:email"
                         SPNameQualifier=""
                         >email@example.com</saml:NameID>
    """
    soup = BeautifulStoneSoup(assertion)
    subject = soup.findAll('saml:subject')[0]
    name_id = subject.findAll('saml:nameid')[0]
    email = name_id.string
    return email


def _get_user_from_assertion(assertion):
    """
    Gets info out of the assertion and locally logs in this user.
    May create a local user account first.
    Returns the user object that was created.
    """
    email = _get_email_from_assertion(assertion)
    try:
        [user] = User.objects.filter(email=email)[:1]
    except:
        user = User.objects.create_user(
            email[:30],
            email,
            sso_settings.SSO_DEFAULT_USER_PASSWORD
        )

        profile = Profile(user=user, owner=user, creator=user,
                          sso_user=True)
        profile.save()

    #NOTE: Login will fail if the user has changed his password via the local account.
    user = authenticate(username=user.username,
                        password=sso_settings.SSO_DEFAULT_USER_PASSWORD)

    return user


@is_enabled('sso')
def sso_login(request):
    """
    Replies with an XHTML SSO Request.
    """
    selected_idp_url = get_setting('module', 'sso', 'idp_login_url')
    sso_destination = request.GET.get('next', None)
    request.session['sso_destination'] = sso_destination
    acs_url = "%s%s" %(get_setting('site', 'global', 'siteurl'), reverse("sso.acs"))

    parameters = {
        'ACS_URL': acs_url,
        'DESTINATION': selected_idp_url,
        'AUTHN_REQUEST_ID': base.get_random_id(),
        'ISSUE_INSTANT': base.get_time_string(),
        'ISSUER': _get_entity_id(request),
    }

    authn_req = xml_render.get_authnrequest_xml(parameters, signed=False)
    request = base64.b64encode(authn_req)
    token = sso_destination
    tv = {
        'request_url': selected_idp_url,
        'request': request,
        'token': token,
    }
    return render_to_response('sso/sso_post_request.html', tv)


@csrf_view_exempt
def sso_response(request):
    """
    Handles a POSTed SSO Assertion and logs the user in.
    """
    sso_session = request.POST.get('RelayState', None)
    data = request.POST.get('SAMLResponse', None)
    assertion = base64.b64decode(data)

    user = _get_user_from_assertion(assertion)

    if user:
        login(request, user)
        messages.add_message(request, messages.SUCCESS, "Woohoo %s, you've successfully logged in." % user.username)
    else:
        messages.add_message(request, messages.WARNING, "User has changed the password in this site, please consider logging in using the site itself.")

    if not sso_session:
        sso_session = '/'

    return redirect(sso_session)


@is_enabled('sso')
def sso_logout(request):
    """
    Logout user from the site and from the idp.
    """
    logout(request)
    return redirect(get_setting('module', 'sso', 'idp_logout_url'))


def descriptor(request):
    """
    Replies with the XML Metadata SPSSODescriptor.
    """
    acs_url = "%s%s" %(get_setting('site', 'global', 'siteurl'), reverse("sso.acs"))
    entity_id = _get_entity_id(request)
    pubkey = xml_signing.load_cert_data(sso_settings.SSO_CERTIFICATE_FILE)
    tv = {
        'acs_url': acs_url,
        'entity_id': entity_id,
        'cert_public_key': pubkey,
    }
    return xml_response(request, 'sso/spssodescriptor.xml', tv)
