from django import forms
from .models import Tour, TourParticipant, Participant


class TourForm(forms.ModelForm):
    class Meta:
        model = Tour
        fields = ('offer', 'start_date', 'end_date', "open")
        widgets = {'start_date': forms.DateInput(attrs={'class': 'datepicker', 'placeholder': 'dd.mm.rrrr'}),
                   'end_date': forms.DateInput(attrs={'class': 'datepicker', 'placeholder': 'dd.mm.rrrr'}),
                   }


class ParticipantForm(forms.ModelForm):
    class Meta:
        model = Participant
        fields = "__all__"
        widgets = {'date_of_birth': forms.TextInput(attrs={'placeholder': 'rrrr-mm-dd'}),
                   }


class TourParticipantForm(forms.ModelForm):
    class Meta:
        model = TourParticipant
        fields = ('status', )


