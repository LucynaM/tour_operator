from django import forms
from .models import Tour, TourParticipant, Participant


class TourForm(forms.ModelForm):
    start_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    end_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    class Meta:
        model = Tour
        fields = ('offer',)


class ParticipantForm(forms.ModelForm):
    class Meta:
        model = Participant
        fields = "__all__"