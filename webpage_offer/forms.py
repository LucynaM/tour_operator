from django import forms
from .models import Offer, Holiday, News

class AddOfferForm(forms.ModelForm):
    class Meta:
        model = Offer
        exclude = ('selected', 'selected_sort', 'recommended', 'recommended_sort', 'withdrawn')
        widgets = {
            'short_descr': forms.Textarea(attrs={'rows': 4, 'cols': 80, 'class': 'counter'}),
            'price': forms.NumberInput(attrs={'step': 0.01})
        }


class EditOfferForm(forms.ModelForm):
    class Meta:
        model = Offer
        exclude = ('selected', 'selected_sort', 'recommended', 'recommended_sort')
        widgets = {
            'short_descr': forms.Textarea(attrs={'rows': 4, 'cols': 80, 'class': 'counter'}),
            'price': forms.NumberInput(attrs={'step': 0.01})
        }

class AddHolidayForm(forms.ModelForm):
    class Meta:
        model = Holiday
        exclude = ('withdrawn',)
        widgets = {
            'short_descr': forms.Textarea(attrs={'rows': 4, 'cols': 80, 'class': 'counter'}),
        }

class EditHolidayForm(forms.ModelForm):
    class Meta:
        model = Holiday
        fields = '__all__'
        widgets = {
            'short_descr': forms.Textarea(attrs={'rows': 4, 'cols': 80, 'class': 'counter'}),
        }


class NewsForm(forms.ModelForm):
    class Meta:
        model = News
        exclude = ('entry_date',)
        widgets = {
            'short_descr': forms.Textarea(attrs={'rows': 4, 'cols': 80, 'class': 'counter'}),
        }