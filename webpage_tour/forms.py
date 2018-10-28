from django import forms
from .models import Tour, TourParticipant, Participant


class TourForm(forms.ModelForm):
    start_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'text', 'class': 'datepicker', 'placeholder': 'dd.mm.yyyy'}))
    end_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'text', 'class': 'datepicker', 'placeholder': 'dd.mm.yyyy'}))
    class Meta:
        model = Tour
        fields = ('offer',)


class ParticipantForm(forms.ModelForm):
    class Meta:
        model = Participant
        fields = "__all__"
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'fill_data'}),
            'last_name': forms.TextInput(attrs={'class': 'fill_data'}),
            'phone': forms.NumberInput(attrs={'class': 'fill_data'})
        }



class TourParticipantForm(forms.ModelForm):
    class Meta:
        model = TourParticipant
        fields = ('status', )

