from django.forms.widgets import MultiWidget, DateInput, TextInput
from django.utils.safestring import mark_safe
from time import strftime

from tendenci.core.site_settings.utils import get_setting


class SplitDateTimeWidget(MultiWidget):
    def __init__(self, attrs={}, date_format=None, time_format=None):
        if 'date_class' in attrs:
            date_class = attrs['date_class']
            del attrs['date_class']
        else:
            date_class = 'datepicker'
        
        if 'time_class' in attrs:
            time_class = attrs['time_class'] 
            del attrs['time_class']
        else:
            time_class = 'timepicker'
            
        time_attrs = attrs.copy()
        time_attrs['class'] = time_class
        date_attrs = attrs.copy()
        date_attrs['class'] = date_class

        widgets = (DateInput(attrs=date_attrs, format=date_format),
                   TextInput(attrs=time_attrs))

        super(SplitDateTimeWidget, self).__init__(widgets, attrs)

    def decompress(self, value):
        if value:
            date = strftime("%Y-%m-%d", value.timetuple())
            time = strftime("%I:%M %p", value.timetuple())
            return (date, time)
        else:
            return (None, None)

    def format_output(self, rendered_widgets):
        """
        Given a list of rendered widgets (as strings), it inserts an HTML
        linebreak between them.

        Returns a Unicode string representing the HTML for the whole lot.
        """
        return "%s&nbsp;%s" % (rendered_widgets[0], rendered_widgets[1])


class EmailVerificationWidget(MultiWidget):
    def __init__(self, attrs={}):
        if 'email_class_0' in attrs:
            email_class_0 = attrs['email_class_0']
            del attrs['email_class_0']
        else:
            email_class_0 = 'email-verification-0'
        
        if 'email_class_1' in attrs:
            email_class_1 = attrs['email_class_1'] 
            del attrs['email_class_1']
        else:
            email_class_1 = 'email-verification-1'
            
        email0_attrs = attrs.copy()
        email0_attrs['class'] = email_class_0
        email0_attrs['maxlength'] = 75
        email0_attrs['title'] = 'Email'
        email1_attrs = attrs.copy()
        email1_attrs['class'] = email_class_1
        email1_attrs['maxlength'] = 75
        email1_attrs['title'] = 'Confirm Email'

        widgets = (TextInput(attrs=email0_attrs),
                   TextInput(attrs=email1_attrs))

        super(EmailVerificationWidget, self).__init__(widgets, attrs)

    def decompress(self, value):
        if value:
            email = value
            return (email, email)
        else:
            return (None, None)

    def format_output(self, rendered_widgets):
        """
        Given a list of rendered widgets (as strings), it inserts an HTML
        linebreak between them.

        Returns a Unicode string representing the HTML for the whole lot.
        """
        label = "<label generated='true' style='display:none; color:red; margin-left: 5px;' class='email-verfication-error'>Please enter the same email address.</label>"
        return "%s%s<br>%s" % (rendered_widgets[0], label, rendered_widgets[1])


class PriceWidget(TextInput):
    def render(self, name, value, attrs=None):
        currency_symbol = get_setting('site', 'global', 'currencysymbol') or '$'
        html = super(PriceWidget, self).render(name, value, attrs)
        return mark_safe("%s %s" %(currency_symbol, html))

