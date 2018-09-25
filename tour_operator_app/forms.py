from django import forms
from .models import Offer

class AddOfferForm(forms.ModelForm):
    class Meta:
        model = Offer
        exclude = ('selected', 'selected_sort', 'recommended', 'recommended_sort', 'withdrawn')
        widget = {
            'short_descr': forms.Textarea(attrs={'rows': 4, 'cols': 80, 'class': 'form-control'}),
            'schedule': forms.Textarea(attrs={'rows': 4, 'cols': 80, 'class': 'form-control'}),
        }