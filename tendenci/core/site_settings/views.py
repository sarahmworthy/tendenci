from django.shortcuts import render_to_response
from django.http import Http404, HttpResponseRedirect
from django.template import RequestContext
from django.contrib import messages

from tendenci.core.base.http import Http403
from tendenci.core.site_settings.models import Setting
from tendenci.core.site_settings.forms import build_settings_form
from tendenci.core.site_settings.utils import delete_settings_cache
from tendenci.core.perms.utils import has_perm
from tendenci.core.theme.utils import theme_options
from tendenci.core.event_logs.models import EventLog


def list(request, scope, scope_category, template_name="site_settings/list.html"):
    if not has_perm(request.user, 'site_settings.change_setting'):
        raise Http403

    settings = Setting.objects.filter(scope=scope, scope_category=scope_category).order_by('label')
    if not settings:
        raise Http404

    # check if module setting is for theme editor
    if scope_category == 'theme_editor':
        theme_setting = Setting.objects.get(name='theme')
        # no need to update input values if there is no change
        if theme_setting.input_value != theme_options():
            theme_setting.input_value = theme_options()
            theme_setting.save()
            # update queryset to include the changes done
            settings = Setting.objects.filter(scope=scope, scope_category=scope_category).order_by('label')

    if request.method == 'POST':
        form = build_settings_form(request.user, settings)(request.POST, request.FILES)
        if form.is_valid():
            # this save method is overriden in the forms.py
            form.save()
            delete_settings_cache(scope, scope_category)
            try:
                if form.cleaned_data['theme']:
                    from django.core.management import call_command
                    call_command('hide_settings', 'theme')
                    call_command('update_settings', 'themes.%s' % form.cleaned_data['theme'].lstrip())
            except:
                pass

            EventLog.objects.log()
            messages.add_message(request, messages.SUCCESS, 'Successfully saved %s settings' % scope_category.replace('_',' ').title())

            redirect_to = request.REQUEST.get('next', '')
            if redirect_to:
                return HttpResponseRedirect(redirect_to)

    else:
        form = build_settings_form(request.user, settings)()
        # Log the get so we see if someone views setting values
        EventLog.objects.log()

    return render_to_response(template_name, {'form': form, 
                                              'scope_category': scope_category }, context_instance=RequestContext(request))


def index(request, template_name="site_settings/settings.html"):
    if not has_perm(request.user,'site_settings.change_setting'):
        raise Http403
    settings = Setting.objects.values().exclude(scope='template').order_by('scope_category')
    # Do not display standard regform settings
    settings = settings.exclude(scope_category='events', name__startswith='regform_')
    EventLog.objects.log()
    return render_to_response(template_name, {'settings':settings}, context_instance=RequestContext(request))


def single_setting(request, scope, scope_category, name, template_name="site_settings/list.html"):
    if not has_perm(request.user,'site_settings.change_setting'):
        raise Http403
    
    settings = Setting.objects.filter(scope=scope, scope_category=scope_category, name=name).order_by('label')
    if not settings:
        raise Http404
    
    if request.method == 'POST':
        form = build_settings_form(request.user, settings)(request.POST, request.FILES)
        if form.is_valid():
            # this save method is overriden in the forms.py
            form.save()
            try:
                if form.cleaned_data['theme']:
                    from django.core.management import call_command
                    call_command('hide_settings', 'theme')
                    call_command('update_settings', 'themes.%s' % form.cleaned_data['theme'].lstrip())
            except:
                pass

            EventLog.objects.log()
            messages.add_message(request, messages.SUCCESS, 'Successfully saved %s settings' % name.replace('_',' ').title())

            redirect_to = request.REQUEST.get('next', '')
            if redirect_to:
                return HttpResponseRedirect(redirect_to)

    else:
        form = build_settings_form(request.user, settings)()
        
    return render_to_response(template_name, {'form': form }, context_instance=RequestContext(request))

