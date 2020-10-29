from .models import Wallets
from django import forms


class ConvertForm(forms.Form):
    choices = (
        ('rubles', '&#8381'),
        ('euro', '&#8364'),
        ('dollars', '&#36'),
    )
    fields = ['from', 'to', 'amount']
    model = Wallets
    widgets = {
        'from': forms.ChoiceField(choices=choices),
        'to': forms.ChoiceField(choices=choices),
        'amount':forms.FloatField(min_value=0)

    }
