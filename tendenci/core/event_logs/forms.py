from datetime import datetime, timedelta
from django.utils.translation import ugettext_lazy as _
from django import forms

from .models import EventLog
from tendenci.core.base.fields import SplitDateTimeField
from form_utils.forms import BetterForm

INITIAL_START_DT = datetime.now() - timedelta(weeks=4)
INITIAL_END_DT = datetime.now()
ACTION_CHOICES = [(i, i) for i in EventLog.objects.values_list('action', flat=True).distinct().order_by('action')]
ACTION_CHOICES = [('','---------------')] + ACTION_CHOICES
REQUEST_CHOICES = [('all', 'ALL',), ('post', 'POST',), ('get', 'GET',)]


class EventsFilterForm(forms.Form):
    event_id = forms.IntegerField(required=False)
    ip = forms.CharField(max_length=16, required=False)
    user_id = forms.IntegerField(required=False)
    session_id = forms.CharField(max_length=40, required=False)

    def process_filter(self, queryset):
        cd = self.cleaned_data
        if cd['event_id']:
            queryset = queryset.filter(event_id=cd['event_id'])
        if cd['ip']:
            queryset = queryset.filter(user_ip_address=cd['ip'])
        if cd['user_id']:
            queryset = queryset.filter(user__pk=cd['user_id'])
        if cd['session_id']:
            queryset = queryset.filter(session_id=cd['session_id'])
        return queryset


class EventLogSearchForm(BetterForm):
    start_dt = SplitDateTimeField(
        label=_('Start Date/Time'),
        initial=INITIAL_START_DT,
        required=False
    )
    end_dt = SplitDateTimeField(
        label=_('End Date/Time'),
        initial=INITIAL_END_DT,
        required=False
    )
    request_method = forms.ChoiceField(
        required=False,
        choices=REQUEST_CHOICES,
        help_text='GET = whether a page/item was viewed. POST = an item was edited or added'
    )

    object_id = forms.CharField(
        required=False,
        help_text="This is the ID Tendenci uses for all objects. "
        "This is the number you sometimes see in URLs. For example, "
        "for the event at http://tendenci.com/events/173/, the object ID is 173.")

    user_ip_address = forms.CharField(required=False)
    user_id = forms.IntegerField(required=False)
    user_name = forms.CharField(required=False)
    application = forms.CharField(
        required=False,
        help_text="These are the different modules like Pages or Articles.")

    action = forms.ChoiceField(
      required=False,
      choices=ACTION_CHOICES,
      help_text="These are the actions within the python commands at view.py. "
      "Some examples of actions are search and edit, for example."
      )

    class Meta:
        fields = (
            'start_dt',
            'end_dt',
            'request_method',
            'object_id'
            'user_ip_address',
            'user_id',
            'user_name',
            'application',
            'action',
            )

        fieldsets = [('',
            {
              'fields': ['start_dt',
                         'end_dt',
                         'request_method',
                         ],
              'legend': ''
              }),
            ('Advanced Options',
            {
              'fields': ['user_id',
                         'user_name',
                         'user_ip_address',
                         'object_id',
                         'application',
                         'action'
                         ],
              'legend': 'Advanced Options'
              }),
        ]