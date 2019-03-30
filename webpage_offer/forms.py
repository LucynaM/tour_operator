from django import forms
from .models import Offer, News

class AddOfferForm(forms.ModelForm):
    class Meta:
        model = Offer
        exclude = ('category', 'descr', 'selected', 'selected_sort', 'recommended', 'recommended_sort', 'withdrawn')
        widgets = {
            'directions': forms.Textarea(attrs={'rows': 4, 'cols': 80, }),
            'short_descr': forms.Textarea(attrs={'rows': 4, 'cols': 80, 'class': 'counter'}),
            'price': forms.NumberInput(attrs={'step': 0.01})
        }


class EditOfferForm(forms.ModelForm):
    class Meta:
        model = Offer
        exclude = ('selected', 'descr', 'selected_sort', 'recommended', 'recommended_sort')
        widgets = {
            'directions': forms.Textarea(attrs={'rows': 4, 'cols': 80, }),
            'short_descr': forms.Textarea(attrs={'rows': 4, 'cols': 80, 'class': 'counter'}),
            'price': forms.NumberInput(attrs={'step': 0.01})
        }

class AddHolidayForm(forms.ModelForm):
    class Meta:
        model = Offer
        exclude = ('category', 'selected', 'selected_sort', 'recommended', 'recommended_sort', 'withdrawn')
        widgets = {
            'directions': forms.Textarea(attrs={'rows': 4, 'cols': 80, }),
            'short_descr': forms.Textarea(attrs={'rows': 4, 'cols': 80, 'class': 'counter'}),
        }

class EditHolidayForm(forms.ModelForm):
    class Meta:
        model = Offer
        exclude = ('selected', 'selected_sort', 'recommended', 'recommended_sort')
        widgets = {
            'directions': forms.Textarea(attrs={'rows': 4, 'cols': 80, }),
            'short_descr': forms.Textarea(attrs={'rows': 4, 'cols': 80, 'class': 'counter'}),
        }


class NewsForm(forms.ModelForm):
    class Meta:
        model = News
        exclude = ('entry_date',)
        widgets = {
            'short_descr': forms.Textarea(attrs={'rows': 4, 'cols': 80, 'class': 'counter'}),
        }