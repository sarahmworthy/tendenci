from django import forms

from tendenci.core.payments.models import PaymentGateway

class PaymentGatewayForm(forms.Form):
    gateway = forms.ModelChoiceField(queryset=PaymentGateway.objects.all())
