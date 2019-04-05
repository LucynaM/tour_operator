from django import forms
from .models import Offer, News

class AddOfferForm(forms.ModelForm):
    class Meta:
        model = Offer
        exclude = ('category', 'descr', 'selected', 'selected_sort', 'recommended', 'recommended_sort', 'withdrawn')
        widgets = {
            'direction': forms.Textarea(attrs={'rows': 4}),
            'places': forms.Textarea(attrs={'rows': 4}),
            'short_descr': forms.Textarea(attrs={'rows': 4, 'class': 'counter'}),
            'price': forms.NumberInput(attrs={'step': 0.01})
        }


class EditOfferForm(forms.ModelForm):

    class Meta:
        model = Offer
        exclude = ('selected', 'descr', 'selected_sort', 'recommended', 'recommended_sort')
        widgets = {
            'direction': forms.Textarea(attrs={'rows': 4, }),
            'places': forms.Textarea(attrs={'rows': 4}),
            'short_descr': forms.Textarea(attrs={'rows': 4, 'class': 'counter'}),
            'schedule': forms.Textarea(attrs={'rows': 20, }),
            'price': forms.NumberInput(attrs={'step': 0.01})
        }

class AddHolidayForm(forms.ModelForm):
    class Meta:
        model = Offer
        exclude = ('category', 'selected', 'selected_sort', 'recommended', 'recommended_sort', 'withdrawn')
        widgets = {
            'direction': forms.Textarea(attrs={'rows': 4, }),
            'places': forms.Textarea(attrs={'rows': 4}),
            'short_descr': forms.Textarea(attrs={'rows': 4, 'class': 'counter'}),
            'descr': forms.Textarea(attrs={'rows': 5, }),
            'schedule': forms.Textarea(attrs={'rows': 20, }),
        }

class EditHolidayForm(forms.ModelForm):
    class Meta:
        model = Offer
        exclude = ('selected', 'selected_sort', 'recommended', 'recommended_sort')
        widgets = {
            'direction': forms.Textarea(attrs={'rows': 4, }),
            'places': forms.Textarea(attrs={'rows': 4, }),
            'short_descr': forms.Textarea(attrs={'rows': 4, 'class': 'counter'}),
            'descr': forms.Textarea(attrs={'rows': 5, }),
            'schedule': forms.Textarea(attrs={'rows': 20, }),
        }


class NewsForm(forms.ModelForm):
    class Meta:
        model = News
        exclude = ('entry_date',)
        widgets = {
            'short_descr': forms.Textarea(attrs={'rows': 4, 'class': 'counter'}),
            'entry': forms.Textarea(attrs={'rows': 20, }),
        }