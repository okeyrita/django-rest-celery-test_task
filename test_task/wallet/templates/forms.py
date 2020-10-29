from .models import Wallets
from django import forms


class ConvertForm(forms.Form):
    class Meta:
        model = Wallets
        choicess = (
            ('rubles', '&#8381'),
            ('euro', '&#8364'),
            ('dollars', '&#36'),
        )
        fields = ['from', 'to', 'amount']
        
        widgets = {
            'from': forms.ChoiceField(choices=choicess),
            'to': forms.ChoiceField(choices=choicess),
            'amount': forms.IntegerField(min_value=0)

        }
