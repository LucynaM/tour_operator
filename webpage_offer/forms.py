from django import forms
from .models import Offer, Holiday

class AddOfferForm(forms.ModelForm):
    class Meta:
        model = Offer
        exclude = ('selected', 'selected_sort', 'recommended', 'recommended_sort', 'withdrawn')
        widgets = {
            'short_descr': forms.Textarea(attrs={'rows': 4, 'cols': 80, 'class': 'counter'}),
            'duration_in_days': forms.NumberInput(attrs={'min': 1}),
            'price': forms.NumberInput(attrs={'step': 0.01})
        }


class EditOfferForm(forms.ModelForm):
    class Meta:
        model = Offer
        exclude = ('selected', 'selected_sort', 'recommended', 'recommended_sort')
        widgets = {
            'short_descr': forms.Textarea(attrs={'rows': 4, 'cols': 80, 'class': 'counter'}),
            'duration_in_days': forms.NumberInput(attrs={'step': 1}),
            'price': forms.NumberInput(attrs={'step': 0.01})
        }

class HolidayForm(forms.ModelForm):
    class Meta:
        model = Holiday
        fields = '__all__'