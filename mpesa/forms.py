from django import forms


class MpesaForm(forms.Form):
    PhoneNumber = forms.CharField(label='Enter Phone Number e.g 254702822379')
    Amount = forms.IntegerField(label='Amount')


class QueryForm(forms.Form):
    Query = forms.CharField(label='Enter Phone Number or Transaction ID to Query payments')
