from django import forms
from .models import Tour, TourParticipant, Participant


class TourForm(forms.ModelForm):
    class Meta:
        model = Tour
        fields = ('offer', 'start_date', 'end_date',)
        widgets = {'start_date': forms.DateInput(attrs={'class': 'datepicker', 'placeholder': 'dd/mm/yyyy'}),
                   'end_date': forms.DateInput(attrs={'class': 'datepicker', 'placeholder': 'dd/mm/yyyy'}),
                   }


class ParticipantForm(forms.ModelForm):
    class Meta:
        model = Participant
        fields = "__all__"
        widgets = {
            #'first_name': forms.TextInput(attrs={'class': 'fill_data'}),
            'last_name': forms.TextInput(attrs={'class': 'fill_name'}),
            #'phone': forms.NumberInput(attrs={'class': 'fill_data'})
        }



class TourParticipantForm(forms.ModelForm):
    class Meta:
        model = TourParticipant
        fields = ('status', )

